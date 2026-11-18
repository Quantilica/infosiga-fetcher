"""O build do lake pula, sem ler o bruto, o que já está em dia."""

from __future__ import annotations

import builtins
import hashlib
import json
import zipfile
from pathlib import Path

import polars as pl
import pytest
import quantilica.core.manifests as manifests_mod

import infosiga_fetcher.lake as lake_mod
from infosiga_fetcher.lake import converter

_SIN = "id_sinistro;data_sinistro\n1;15/05/2022\n2;20/08/2023\n"
_PES = "id_sinistro;id_pessoa;data_sinistro\n1;1;15/05/2022\n"
_VEI = "id_sinistro;id_veiculo;ano_fab\n1;1;2010\n2;2;2011\n"


def _sidecars(raiz: Path) -> None:
    """Sidecar ``.manifest.json`` com o sha256 de cada bruto, como o fetcher grava:
    o hash do bruto sai dele, sem ler o arquivo."""
    for f in sorted(raiz.rglob("*")):
        if f.is_file() and not f.name.endswith(".manifest.json"):
            Path(f"{f}.manifest.json").write_text(
                json.dumps(
                    {
                        "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                        "size_bytes": f.stat().st_size,
                    }
                ),
                encoding="utf-8",
            )


def _bruto(tmp_path: Path) -> Path:
    raw = tmp_path / "raw"
    (raw / "dados").mkdir(parents=True)
    with zipfile.ZipFile(raw / "dados" / "dados_infosiga@20261101.zip", "w") as zf:
        zf.writestr("sinistros_2022-2024.csv", _SIN.encode("cp1252"))
        zf.writestr("pessoas_2022-2024.csv", _PES.encode("cp1252"))
        zf.writestr("veiculos_2015-2021.csv", _VEI.encode("cp1252"))
        zf.writestr("veiculos_2022-2024.csv", _VEI.encode("cp1252"))
    # Dicionário em PDF (outro grupo do catálogo) e CSV solto de outra tabela.
    (raw / "dicionario").mkdir()
    with zipfile.ZipFile(
        raw / "dicionario" / "dicionario_dados@20261101.zip", "w"
    ) as zf:
        zf.writestr("dicionario.pdf", b"%PDF-1.4")
    (raw / "dados" / "sinistros_extra@20261101.csv").write_bytes(
        _SIN.replace("1;", "9;").encode("cp1252")
    )
    _sidecars(raw)
    return raw


@pytest.fixture
def leituras(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> list[str]:
    """Registra toda abertura/leitura do bruto: ZIP, open, transcodificação, scan."""
    vistas: list[str] = []
    raiz = str(tmp_path / "raw")

    def espia(nome: str, original):  # noqa: ANN001, ANN202
        def _f(*args, **kwargs):  # noqa: ANN002, ANN003
            vistas.append(nome)
            return original(*args, **kwargs)

        return _f

    original_open = builtins.open

    def open_espiado(file, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003, ANN202
        if str(file).startswith(raiz):
            vistas.append(f"open:{file}")
        return original_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", open_espiado)
    monkeypatch.setattr(zipfile, "ZipFile", espia("zipfile", zipfile.ZipFile))
    monkeypatch.setattr(
        lake_mod, "_member_as_utf8", espia("utf8", lake_mod._member_as_utf8)
    )
    monkeypatch.setattr(
        lake_mod, "_csv_member_names", espia("nomes", lake_mod._csv_member_names)
    )
    monkeypatch.setattr(pl, "scan_csv", espia("scan_csv", pl.scan_csv))
    monkeypatch.setattr(
        manifests_mod, "sha256_file", espia("hash", manifests_mod.sha256_file)
    )
    return vistas


@pytest.mark.parametrize(
    ("dataset", "convertidos"),
    [("sinistros", 4), ("pessoas", 1), ("veiculos", 2)],
)
def test_segunda_rodada_nao_le_o_bruto(
    tmp_path: Path, leituras: list[str], dataset: str, convertidos: int
) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"

    r1 = converter.convert(raw, lake, datasets=[dataset])
    assert not r1.errors
    assert (r1.converted, r1.skipped) == (convertidos, 0)
    assert leituras  # a primeira rodada le o bruto

    leituras.clear()
    r2 = converter.convert(raw, lake, datasets=[dataset])
    assert (r2.converted, r2.skipped, r2.errors) == (0, convertidos, [])
    assert leituras == []


def test_um_dataset_nao_toca_o_bruto_de_outro(
    tmp_path: Path, leituras: list[str]
) -> None:
    """Rodada que converte so ``pessoas`` nao abre o CSV solto de sinistros."""
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    converter.convert(raw, lake, datasets=["pessoas"])
    assert not any("sinistros_extra" in v for v in leituras)
    assert not any("dicionario" in v for v in leituras)


def test_todos_os_datasets_em_dia_nao_le_o_bruto(
    tmp_path: Path, leituras: list[str]
) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    r1 = converter.convert(raw, lake)
    assert not r1.errors
    leituras.clear()

    r2 = converter.convert(raw, lake)
    assert (r2.converted, r2.skipped, r2.errors) == (0, r1.converted, [])
    assert leituras == []


def test_force_reconverte(tmp_path: Path, leituras: list[str]) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    converter.convert(raw, lake, datasets=["veiculos"])
    leituras.clear()

    r = converter.convert(raw, lake, datasets=["veiculos"], force=True)
    assert (r.converted, r.skipped, r.errors) == (2, 0, [])
    assert "utf8" in leituras


def test_bruto_novo_converte_e_o_antigo_segue_em_dia(
    tmp_path: Path, leituras: list[str]
) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    converter.convert(raw, lake, datasets=["veiculos"])

    novo = raw / "dados" / "dados_infosiga@20261201.zip"
    with zipfile.ZipFile(novo, "w") as zf:
        zf.writestr(
            "veiculos_2015-2021.csv",
            (_VEI + "3;3;2012\n").encode("cp1252"),
        )
    _sidecars(raw)
    leituras.clear()

    r = converter.convert(raw, lake, datasets=["veiculos"])
    assert not r.errors
    assert (r.converted, r.skipped) == (1, 0)
    assert "utf8" in leituras
    rows = pl.concat(
        [
            pl.read_parquet(p)
            for p in (lake / "infosiga" / "veiculos").rglob("*.parquet")
        ],
        how="diagonal",
    )
    assert "3" in rows["id_sinistro"].to_list()

    # Terceira rodada: nada mudou, nada é lido.
    leituras.clear()
    r3 = converter.convert(raw, lake, datasets=["veiculos"])
    assert (r3.converted, r3.skipped, r3.errors) == (0, 1, [])
    assert leituras == []


def test_bruto_alterado_no_lugar_reconverte(tmp_path: Path) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    converter.convert(raw, lake, datasets=["pessoas"])

    zpath = raw / "dados" / "dados_infosiga@20261101.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr(
            "pessoas_2022-2024.csv", (_PES + "2;2;20/08/2023\n").encode("cp1252")
        )

    r = converter.convert(raw, lake, datasets=["pessoas"])
    assert not r.errors
    assert r.skipped == 0
    assert r.converted == 2  # anos 2022 e 2023
