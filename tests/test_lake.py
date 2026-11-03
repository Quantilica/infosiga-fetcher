"""Tests for infosiga-fetcher lake converter."""

from __future__ import annotations

import zipfile
from pathlib import Path

import polars as pl
from quantilica.analytics.lake import check_dataset

from infosiga_fetcher.lake import converter


def test_converter_metadata() -> None:
    assert converter.source_id == "infosiga"
    datasets = converter.datasets()
    assert "sinistros" in datasets
    assert "pessoas" in datasets
    assert "veiculos" in datasets


def test_converter_empty_dir(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    res = converter.convert(raw_dir, lake_dir)
    assert res.converted == 0
    assert not res.errors


def test_convert_infosiga_multi_year_zip(tmp_path: Path) -> None:
    """Test conversion of consolidated INFOSIGA ZIP covering multiple years."""
    raw_dir = tmp_path / "raw" / "dados"
    raw_dir.mkdir(parents=True)
    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    # 1. Sinistros with rows in 2022 and 2023
    csv_sinistros = (
        "id_sinistro;data_sinistro;hora_sinistro;tipo_via;municipio\n"
        "1001;15/05/2022;14:30;RUA;SAO PAULO\n"
        "1002;20/08/2023;18:00;RODOVIA;CAMPINAS\n"
    )

    # 2. Pessoas
    csv_pessoas = (
        "id_sinistro;id_pessoa;tipo_de_vitima;sexo;idade;data_sinistro\n"
        "1001;1;CONDUTOR;M;35;15/05/2022\n"
        "1002;2;PEDESTRE;F;28;20/08/2023\n"
    )

    # 3. Veículos
    csv_veiculos = (
        "id_sinistro;id_veiculo;tipo_veiculo;ano_fab\n"
        "1001;1;AUTOMOVEL;2020\n"
        "1002;2;MOTOCICLETA;2021\n"
    )

    zip_file = raw_dir / "dados_infosiga@20261101.zip"
    with zipfile.ZipFile(zip_file, "w") as zf:
        zf.writestr("sinistros_2022-2024.csv", csv_sinistros.encode("cp1252"))
        zf.writestr("pessoas_2022-2024.csv", csv_pessoas.encode("cp1252"))
        zf.writestr("veiculos_2022-2024.csv", csv_veiculos.encode("cp1252"))

    res = converter.convert(raw_dir.parent, lake_dir)
    assert res.converted >= 3
    assert not res.errors

    # Verify sinistros partitions
    ds_sinistros = lake_dir / "infosiga" / "sinistros"
    errors_sinistros = check_dataset(ds_sinistros)
    assert not errors_sinistros, f"errors in sinistros: {errors_sinistros}"
    assert (ds_sinistros / "ano=2022").is_dir()
    assert (ds_sinistros / "ano=2023").is_dir()

    df_2022 = pl.read_parquet(list((ds_sinistros / "ano=2022").glob("*.parquet"))[0])
    assert df_2022["id_sinistro"][0] == "1001"

    df_2023 = pl.read_parquet(list((ds_sinistros / "ano=2023").glob("*.parquet"))[0])
    assert df_2023["id_sinistro"][0] == "1002"

    # Verify pessoas
    ds_pessoas = lake_dir / "infosiga" / "pessoas"
    errors_pessoas = check_dataset(ds_pessoas)
    assert not errors_pessoas, f"errors in pessoas: {errors_pessoas}"

    # Verify veículos
    ds_veiculos = lake_dir / "infosiga" / "veiculos"
    errors_veiculos = check_dataset(ds_veiculos)
    assert not errors_veiculos, f"errors in veiculos: {errors_veiculos}"


def _rows(dataset_dir: Path) -> pl.DataFrame:
    parts = sorted(dataset_dir.rglob("*.parquet"))
    return pl.concat([pl.read_parquet(p) for p in parts], how="diagonal")


def _zip(raw_dir: Path, members: dict[str, str]) -> None:
    with zipfile.ZipFile(raw_dir / "dados_infosiga@20261103.zip", "w") as zf:
        for name, text in members.items():
            zf.writestr(name, text.encode("cp1252"))


def test_zip_com_dois_membros_do_mesmo_dataset_preserva_todas_as_linhas(
    tmp_path: Path,
) -> None:
    """Regressao A2: veiculos_2015-2021 e veiculos_2022-2024 nao se pulam."""
    raw_dir = tmp_path / "raw" / "dados"
    raw_dir.mkdir(parents=True)
    header = "id_sinistro;id_veiculo;tipo_veiculo;ano_fab\n"
    _zip(
        raw_dir,
        {
            "veiculos_2015-2021.csv": header + "1;1;AUTOMÓVEL;2010\n2;2;AUTO;2010\n",
            "veiculos_2022-2024.csv": header + "3;3;AUTO;2010\n4;4;MOTO;2010\n",
        },
    )
    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    res = converter.convert(tmp_path / "raw", lake_dir, datasets=["veiculos"])
    assert not res.errors
    assert (res.converted, res.skipped) == (2, 0)

    ds = lake_dir / "infosiga" / "veiculos"
    assert not check_dataset(ds)
    df = _rows(ds)
    assert df.height == 4
    assert sorted(df["id_sinistro"].to_list()) == ["1", "2", "3", "4"]
    assert "AUTOMÓVEL" in df["tipo_veiculo"].to_list()
    # NUNCA particionar por ano de fabricacao: todos os carros sao de 2010
    assert not (ds / "ano=2010").exists()
    assert sorted(p.name for p in ds.glob("ano=*")) == ["ano=2015", "ano=2022"]
    assert sorted(df["periodo_arquivo"].unique().to_list()) == [
        "2015-2021",
        "2022-2024",
    ]

    res2 = converter.convert(tmp_path / "raw", lake_dir, datasets=["veiculos"])
    assert (res2.converted, res2.skipped, res2.errors) == (0, 2, [])
    assert _rows(ds).height == 4


def test_ano_vem_do_sinistro_e_linha_sem_ano_vai_para_quarentena(
    tmp_path: Path,
) -> None:
    """Sem ``fill_null(2015)``: data ausente/invalida nao ganha ano inventado."""
    raw_dir = tmp_path / "raw" / "dados"
    raw_dir.mkdir(parents=True)
    _zip(
        raw_dir,
        {
            "veiculos_2015-2024.csv": (
                "id_sinistro;data_sinistro;ano_fab\n"
                "1;15/05/2022;1999\n"
                "2;;1999\n"
                "3;00/00/0000;1999\n"
                "4;20/08/2023;2001\n"
            )
        },
    )
    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    res = converter.convert(tmp_path / "raw", lake_dir, datasets=["veiculos"])
    assert not res.errors
    ds = lake_dir / "infosiga" / "veiculos"
    assert not check_dataset(ds)
    parts = sorted(p.name for p in ds.glob("ano=*"))
    assert parts == ["ano=2022", "ano=2023", "ano=__HIVE_DEFAULT_PARTITION__"]
    assert not (ds / "ano=2015").exists()
    quarentena = _rows(ds / "ano=__HIVE_DEFAULT_PARTITION__")
    assert sorted(quarentena["id_sinistro"].to_list()) == ["2", "3"]
    assert _rows(ds).height == 4


def test_sinistros_sem_data_e_erro_contado(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw" / "dados"
    raw_dir.mkdir(parents=True)
    _zip(raw_dir, {"sinistros_2022-2024.csv": "id_sinistro;municipio\n1;SAO PAULO\n"})
    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    res = converter.convert(tmp_path / "raw", lake_dir, datasets=["sinistros"])
    assert res.converted == 0
    assert len(res.errors) == 1
    assert not list(lake_dir.rglob("*.parquet"))


def test_leitura_nao_carrega_o_membro_inteiro(tmp_path: Path, monkeypatch) -> None:
    """O membro e lido em blocos (zf.open), nunca com ZipFile.read."""

    def _proibido(self, *args, **kwargs):
        raise AssertionError("ZipFile.read carrega o membro inteiro na memoria")

    monkeypatch.setattr(zipfile.ZipFile, "read", _proibido)
    raw_dir = tmp_path / "raw" / "dados"
    raw_dir.mkdir(parents=True)
    _zip(
        raw_dir,
        {"sinistros_2022-2024.csv": "id_sinistro;data_sinistro\n1;15/05/2022\n"},
    )
    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    res = converter.convert(tmp_path / "raw", lake_dir, datasets=["sinistros"])
    assert not res.errors
    assert res.converted == 1
