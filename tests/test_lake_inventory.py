"""O inventario do conversor diz a auditoria do lake o que nao vira Parquet."""

from __future__ import annotations

import zipfile
from pathlib import Path

from infosiga_fetcher.lake import converter

_SIN = "id_sinistro;data_sinistro\n1;15/05/2022\n"


def _zip(path: Path, **membros: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as zf:
        for nome, texto in membros.items():
            zf.writestr(nome, texto.encode("cp1252"))


def _plano(raw: Path) -> dict[str, tuple[str | None, str | None]]:
    return {
        p.path.relative_to(raw).as_posix(): (p.dataset, p.skip_reason)
        for p in converter.inventory(raw)
    }


def test_inventory_dicionario_nao_tabular(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _zip(raw / "dados" / "dados_infosiga@20261124.zip", **{"sinistros_2022.csv": _SIN})
    # O dicionario vem em ZIP (PDF dentro): sem dados para o lake.
    _zip(
        raw / "dicionario" / "dicionario_dados@20261124.zip", **{"dicionario.pdf": "x"}
    )

    plano = _plano(raw)

    assert plano["dicionario/dicionario_dados@20261124.zip"] == (None, "nao_tabular")
    # O ZIP de dados continua esperando Parquet (sem motivo para ignorar).
    assert plano["dados/dados_infosiga@20261124.zip"] == (None, None)


def test_inventory_versoes_antigas_e_arquivos_de_apoio(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    _zip(raw / "dados" / "dados_infosiga.zip", **{"sinistros_2022.csv": _SIN})
    _zip(raw / "dados" / "dados_infosiga@20261118.zip", **{"sinistros_2022.csv": _SIN})
    _zip(raw / "dados" / "dados_infosiga@20261124.zip", **{"sinistros_2022.csv": _SIN})
    (raw / "dados" / "dados_infosiga@20261124.zip.manifest.json").write_text("{}")
    (raw / "dados" / "LEIAME.pdf").write_bytes(b"%PDF")
    (raw / "dados" / "pessoas_2022.csv").write_text(_SIN, encoding="cp1252")
    (raw / "dados" / "outros.csv").write_text(_SIN, encoding="cp1252")

    plano = _plano(raw)

    assert "dados/dados_infosiga@20261124.zip.manifest.json" not in plano
    assert plano["dados/dados_infosiga.zip"] == (None, "superado")
    assert plano["dados/dados_infosiga@20261118.zip"] == (None, "superado")
    assert plano["dados/dados_infosiga@20261124.zip"] == (None, None)
    assert plano["dados/LEIAME.pdf"] == (None, "nao_tabular")
    assert plano["dados/pessoas_2022.csv"] == ("pessoas", None)
    # CSV de tabela desconhecida segue esperando Parquet: a auditoria o acusa.
    assert plano["dados/outros.csv"] == (None, None)


def test_inventory_sem_pasta(tmp_path: Path) -> None:
    assert converter.inventory(tmp_path / "nao-existe") == []
