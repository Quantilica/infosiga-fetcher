"""Constants and endpoint definitions for infosiga-fetcher."""

from __future__ import annotations

INFOSIGA_BASE_URL = "https://infosiga.detran.sp.gov.br"
INFOSIGA_DADOS_ZIP_URL = f"{INFOSIGA_BASE_URL}/painel/download/file/dados_infosiga.zip"
INFOSIGA_DICIONARIO_ZIP_URL = (
    f"{INFOSIGA_BASE_URL}/painel/download/file/Infosiga_dicionario_dados.zip"
)
INFOSIGA_MIN_MAX_DATES_URL = f"{INFOSIGA_BASE_URL}/painel/minMaxDates"

TABLES = ["sinistros", "pessoas", "veiculos"]
