"""Universal Hive Parquet Lake converter for infosiga-fetcher."""

from __future__ import annotations

import codecs
import logging
import os
import re
import tempfile
import unicodedata
import zipfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path

try:
    import polars as pl
    from quantilica.analytics.lake import ConvertResult, LakeWriter
    from quantilica.core.lake import (
        DatasetDescriptor,
        composite_file_key,
        partition_types_for,
        select_current,
    )
except ImportError as exc:
    raise ImportError(
        "infosiga_fetcher.lake requer o extra 'analysis': "
        "uv add 'infosiga-fetcher[analysis]' "
        "--index https://index.quantilica.com/simple/"
    ) from exc

SOURCE_ID = "infosiga"
DATASETS = ["sinistros", "pessoas", "veiculos"]


def _norm_col(col_name: str) -> str:
    s = unicodedata.normalize("NFKD", col_name)
    s = s.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


logger = logging.getLogger(__name__)

# Todos os CSVs do INFOSIGA vem em cp1252 (Windows-1252), separados por ";".
ENCODING = "cp1252"
_CHUNK = 1 << 20
# Faixa de anos do nome do arquivo: ``veiculos_2015-2021.csv``.
_PERIODO = re.compile(r"(?<!\d)((?:19|20)\d{2})-((?:19|20)\d{2})(?!\d)")
# Colunas com a data/ano do sinistro, na ordem de preferencia. O ano de partição
# nunca vem de ``ano_fab`` (ano de fabricacao do veiculo).
_ANO_COLUMNS = ("data_sinistro", "ano_sinistro")
_ANO_MIN, _ANO_MAX = 1900, 2100


def _c1_passthrough(exc: UnicodeDecodeError) -> tuple[str, int]:
    """Bytes que o cp1252 deixa indefinidos (0x81, 0x8D, 0x8F, 0x90, 0x9D) viram o
    caractere de controle C1 de mesmo codigo (o mapeamento do latin-1): sem perda e
    sem U+FFFD. Qualquer outro erro continua sendo erro."""
    if exc.encoding.lower().replace("-", "").replace("_", "") != "cp1252":
        raise exc
    return "".join(chr(b) for b in exc.object[exc.start : exc.end]), exc.end


codecs.register_error("quantilica_c1", _c1_passthrough)


def _transcode_to_utf8(source, dest: Path) -> None:
    """Copia ``source`` (binario, cp1252) para ``dest`` em UTF-8, em blocos.

    Estrito: byte invalido levanta ``UnicodeDecodeError`` (o membro vira erro
    contado) em vez de ser trocado por U+FFFD. Memoria constante.
    """
    decoder = codecs.getincrementaldecoder(ENCODING)(errors="quantilica_c1")
    with open(dest, "w", encoding="utf-8", newline="") as out:
        while chunk := source.read(_CHUNK):
            out.write(decoder.decode(chunk))
        out.write(decoder.decode(b"", final=True))


def _csv_member_names(path: Path) -> list[str] | None:
    """Nomes dos CSVs do ZIP; ``None`` quando ``path`` nao e um ZIP."""
    with open(path, "rb") as f:
        if not f.read(4).startswith(b"PK"):
            return None
    with zipfile.ZipFile(path) as zf:
        return [
            i.filename
            for i in zf.infolist()
            if not i.is_dir() and i.filename.lower().endswith(".csv")
        ]


@contextmanager
def _member_as_utf8(path: Path, name: str | None) -> Iterator[Path]:
    """CSV de um membro (ou do proprio arquivo) em UTF-8 num diretorio temporario.

    Streaming: o membro nunca e lido inteiro na memoria. ``QUANTILICA_LAKE_SCRATCH``
    move o temporario para outro disco, como no LakeWriter.
    """
    with tempfile.TemporaryDirectory(
        dir=os.environ.get("QUANTILICA_LAKE_SCRATCH") or None
    ) as tmp:
        dest = Path(tmp) / "membro.csv"
        if name is None:
            with open(path, "rb") as fh:
                _transcode_to_utf8(fh, dest)
        else:
            with zipfile.ZipFile(path) as zf, zf.open(name) as fh:
                _transcode_to_utf8(fh, dest)
        yield dest


def _periodo(member_name: str) -> tuple[int, int] | None:
    """Faixa de anos (inicio, fim) do nome do membro, ou ``None``."""
    m = _PERIODO.search(member_name.replace("\\", "/").rsplit("/", 1)[-1])
    return (int(m.group(1)), int(m.group(2))) if m else None


def _match_table_type(filename: str) -> str | None:
    """Identify which table a file or member represents."""
    s = filename.lower()
    if "sinistro" in s:
        return "sinistros"
    if "pessoa" in s:
        return "pessoas"
    if "veiculo" in s:
        return "veiculos"
    return None


class InfosigaLakeConverter:
    """Converts INFOSIGA-SP traffic collision data into Universal Hive Parquet Lake."""

    def __init__(self, source_id: str = SOURCE_ID) -> None:
        self.source_id = source_id

    def datasets(self) -> list[str]:
        """Return available dataset identifiers."""
        return list(DATASETS)

    def convert(
        self,
        input_dir: Path,
        lake_dir: Path,
        *,
        datasets: Sequence[str] | None = None,
        force: bool = False,
    ) -> ConvertResult:
        res = ConvertResult()
        input_path = Path(input_dir)
        lake_path = Path(lake_dir)

        if not input_path.exists():
            return res

        target_datasets = set(datasets or DATASETS)

        # Initialize writers with partition ["ano"]
        writers: dict[str, LakeWriter] = {}
        for ds in target_datasets:
            if ds not in DATASETS:
                continue
            descriptor = DatasetDescriptor(
                source_id=self.source_id,
                dataset_id=ds,
                alias=ds,
                partition_keys=["ano"],
                partition_types=partition_types_for(["ano"]),
            )
            writers[ds] = LakeWriter(
                lake_path / self.source_id / ds, descriptor, force=force
            )

        # Find current raw files
        all_raw_files = [f for f in input_path.rglob("*") if f.is_file()]
        active_files = select_current(all_raw_files)

        for raw_file in active_files:
            try:
                names = _csv_member_names(raw_file)
            except (OSError, zipfile.BadZipFile) as exc:
                res.errors.append(f"INFOSIGA {raw_file.name}: ZIP ilegivel: {exc}")
                continue
            if names is None:  # CSV solto, sem ZIP
                if raw_file.suffix.lower() != ".csv":
                    continue
                members: list[str | None] = [None]
            else:
                members = list(names)

            for name in members:
                label = name or raw_file.name
                table_type = _match_table_type(label)
                if not table_type or table_type not in writers:
                    continue
                writer = writers[table_type]
                # Cada membro e um arquivo de origem proprio no lake (chave composta
                # zip+membro): com a chave so do ZIP o LakeWriter tomaria os membros
                # seguintes (mesmo sha256) por ja convertidos.
                key = composite_file_key(raw_file, name).lower()
                try:
                    with _member_as_utf8(raw_file, name) as csv_path:
                        self._convert_member(
                            writer, raw_file, key, csv_path, label, table_type, res
                        )
                except Exception as exc:
                    res.errors.append(
                        f"Erro ao converter INFOSIGA {label} em {raw_file.name}: {exc}"
                    )

        return res

    def _convert_member(
        self,
        writer: LakeWriter,
        raw_file: Path,
        key: str,
        csv_path: Path,
        label: str,
        table_type: str,
        res: ConvertResult,
    ) -> None:
        """Escreve um membro, uma particao ``ano`` por vez (streaming, lazy)."""
        # Tudo como texto (convencao do lake): o esquema nao depende de quantas
        # linhas a inferencia viu e ids/codigos nao perdem zeros a esquerda.
        lf = pl.scan_csv(csv_path, separator=";", infer_schema=False, encoding="utf8")
        columns = lf.collect_schema().names()
        lf = lf.rename({c: _norm_col(c) for c in columns})
        names = [_norm_col(c) for c in columns]
        if lf.head(1).collect().height == 0:
            return

        periodo = _periodo(label)
        source = next((c for c in _ANO_COLUMNS if c in names), None)
        if source is not None:
            # Ano do sinistro, por linha. Linha sem ano valido NAO ganha ano
            # inventado: vai para a particao de quarentena (ano nulo).
            ano = (
                pl.col(source)
                .str.extract(r"(?:^|\D)(\d{4})(?:\D|$)", 1)
                .cast(pl.Int32, strict=False)
            )
            ano = pl.when(ano.is_between(_ANO_MIN, _ANO_MAX)).then(ano)
        elif table_type != "sinistros" and periodo is not None:
            # pessoas/veiculos sem data do sinistro: particao = ano inicial da faixa
            # do arquivo (periodo), registrada em ``periodo_arquivo``.
            ano = pl.lit(periodo[0], dtype=pl.Int32)
            lf = lf.with_columns(
                pl.lit(f"{periodo[0]}-{periodo[1]}").alias("periodo_arquivo")
            )
        else:
            raise ValueError(
                "sem coluna de ano do sinistro "
                f"({'/'.join(_ANO_COLUMNS)}) nem faixa de anos no nome do arquivo"
            )
        lf = lf.with_columns(ano.cast(pl.Int32).alias("ano"))

        anos = lf.select("ano").unique().collect()["ano"].to_list()
        for year in sorted(anos, key=lambda y: (y is None, y)):
            part = lf.filter(
                pl.col("ano").is_null() if year is None else pl.col("ano") == year
            )
            if year is None:
                n = part.select(pl.len()).collect().item()
                logger.warning(
                    "INFOSIGA %s: %d linha(s) sem ano valido na particao de "
                    "quarentena ano=__HIVE_DEFAULT_PARTITION__",
                    label,
                    n,
                )
            written = writer.write_polars(
                part,
                src=raw_file,
                partitions={"ano": year},
                file_key_name=key,
            )
            if written.status == "skipped":
                res.skipped += 1
            else:
                res.converted += 1


converter = InfosigaLakeConverter()
