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
    assert df_2022["id_sinistro"][0] == 1001

    df_2023 = pl.read_parquet(list((ds_sinistros / "ano=2023").glob("*.parquet"))[0])
    assert df_2023["id_sinistro"][0] == 1002

    # Verify pessoas
    ds_pessoas = lake_dir / "infosiga" / "pessoas"
    errors_pessoas = check_dataset(ds_pessoas)
    assert not errors_pessoas, f"errors in pessoas: {errors_pessoas}"

    # Verify veículos
    ds_veiculos = lake_dir / "infosiga" / "veiculos"
    errors_veiculos = check_dataset(ds_veiculos)
    assert not errors_veiculos, f"errors in veiculos: {errors_veiculos}"
