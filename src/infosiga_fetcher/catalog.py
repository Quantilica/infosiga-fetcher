"""Dataset catalog for infosiga-fetcher."""

from __future__ import annotations

from typing import Any

from ._catalog_base import DatasetEntry, GroupInfo, static_dataset
from .constants import INFOSIGA_DADOS_ZIP_URL, INFOSIGA_DICIONARIO_ZIP_URL

__all__ = [
    "DatasetEntry",
    "GroupInfo",
    "GROUPS",
    "GROUP_ALIASES",
    "list_datasets",
]

GROUPS: dict[str, dict[str, Any]] = {
    "dados": GroupInfo(
        name="Dados de Sinistros de Trânsito de SP",
        entries=[
            static_dataset(
                "dados",
                id="dados_infosiga",
                name="Base Consolidada do INFOSIGA (Sinistros, Pessoas e Veículos)",
                url=INFOSIGA_DADOS_ZIP_URL,
                ext="zip",
            )
        ],
    ).to_dict(),
    "dicionario": GroupInfo(
        name="Dicionário de Dados e Metadados",
        entries=[
            static_dataset(
                "dicionario",
                id="dicionario_dados",
                name="Dicionário de Dados INFOSIGA (PDF)",
                url=INFOSIGA_DICIONARIO_ZIP_URL,
                ext="zip",
            )
        ],
    ).to_dict(),
}

GROUP_ALIASES: dict[str, str] = {
    "padrao": "dados",
    "sinistros": "dados",
    "acidentes": "dados",
    "transito": "dados",
}


def list_datasets(group: str | None = None) -> list[dict[str, Any]]:
    """List datasets for a group or all groups."""
    if group is None:
        entries: list[dict[str, Any]] = []
        for g_data in GROUPS.values():
            entries.extend(g_data["entries"])
        return entries

    canon = GROUP_ALIASES.get(group, group)
    if canon not in GROUPS:
        raise ValueError(f"Grupo desconhecido: {group!r}")
    return list(GROUPS[canon]["entries"])
