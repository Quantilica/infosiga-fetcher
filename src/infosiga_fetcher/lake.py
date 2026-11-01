"""Universal Hive Parquet Lake converter for infosiga-fetcher."""

from __future__ import annotations

import io
import re
import unicodedata
import zipfile
from collections.abc import Sequence
from pathlib import Path

try:
    import polars as pl
    from quantilica.analytics.lake import ConvertResult, LakeWriter
    from quantilica.core.lake import (
        DatasetDescriptor,
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


def _read_csv_members(path: Path) -> list[tuple[str, bytes]]:
    """Return list of (member_name, bytes) for CSVs in file (or ZIP archive)."""
    try:
        with open(path, "rb") as f:
            header = f.read(4)
        if header.startswith(b"PK"):
            results = []
            with zipfile.ZipFile(path) as zf:
                for name in zf.namelist():
                    if name.lower().endswith(".csv"):
                        results.append((name, zf.read(name)))
            return results
    except Exception:
        pass

    if path.suffix.lower() == ".csv":
        return [(path.name, path.read_bytes())]
    return []


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
            members = _read_csv_members(raw_file)
            if not members:
                continue

            for name, data_bytes in members:
                table_type = _match_table_type(name)
                if not table_type or table_type not in writers:
                    continue

                writer = writers[table_type]

                try:
                    # Encoding: cp1252, separator ;
                    text = data_bytes.decode("cp1252", errors="replace")
                    df = pl.read_csv(
                        io.StringIO(text),
                        separator=";",
                        infer_schema_length=5000,
                    )
                    if df.height == 0:
                        continue

                    # Normalize column names
                    df = df.rename({c: _norm_col(c) for c in df.columns})

                    # Derive 'ano' from date column or filename
                    if "data_sinistro" in df.columns:
                        df = df.with_columns(
                            pl.col("data_sinistro")
                            .cast(pl.Utf8)
                            .str.extract(r"(\d{4})", 1)
                            .cast(pl.Int32, strict=False)
                            .alias("ano")
                        )
                    elif "ano_fab" in df.columns:
                        df = df.with_columns(
                            pl.col("ano_fab").cast(pl.Int32, strict=False).alias("ano")
                        )
                    else:
                        m = re.search(r"(\d{4})", name)
                        fallback_year = int(m.group(1)) if m else 2015
                        df = df.with_columns(
                            pl.lit(fallback_year).cast(pl.Int32).alias("ano")
                        )

                    # Fill null years with fallback
                    df = df.with_columns(pl.col("ano").fill_null(2015))

                    # Group and write by year partition
                    unique_years = [
                        int(y) for y in df["ano"].unique().to_list() if y is not None
                    ]
                    for year in unique_years:
                        year_df = df.filter(pl.col("ano") == year)
                        if year_df.height > 0:
                            writer.write_polars(
                                year_df,
                                src=raw_file,
                                partitions={"ano": year},
                            )
                            res.converted += 1
                except Exception as exc:
                    res.errors.append(
                        f"Erro ao converter INFOSIGA {name} em {raw_file.name}: {exc}"
                    )

        return res


converter = InfosigaLakeConverter()
