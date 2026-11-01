"""HTTP client for INFOSIGA-SP portal."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from quantilica.core.http import HttpClient
from quantilica.core.logging import get_logger
from quantilica.core.manifests import DownloadManifest

from .constants import (
    INFOSIGA_DADOS_ZIP_URL,
    INFOSIGA_DICIONARIO_ZIP_URL,
    INFOSIGA_MIN_MAX_DATES_URL,
)

logger = get_logger(__name__)


class InfosigaClient:
    """Client for downloading INFOSIGA-SP datasets."""

    def __init__(
        self,
        *,
        client: HttpClient | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.client = client or HttpClient()
        self.logger = logger or get_logger(__name__)

    def get_min_max_dates(self) -> dict[str, Any]:
        """Query minMaxDates endpoint to check latest data date."""
        try:
            data = self.client.get_json(INFOSIGA_MIN_MAX_DATES_URL)
            if isinstance(data, dict):
                return data
        except Exception as exc:
            self.logger.warning("Erro ao consultar minMaxDates: %s", exc)
        return {}

    def download_dados(
        self,
        dest: Path,
        *,
        manifest_path: Path | None = None,
    ) -> DownloadManifest:
        """Download dados_infosiga.zip with SHA-256 manifest."""
        return self.client.download_with_manifest(
            INFOSIGA_DADOS_ZIP_URL,
            dest,
            manifest_path=manifest_path,
        )

    def download_dicionario(
        self,
        dest: Path,
        *,
        manifest_path: Path | None = None,
    ) -> DownloadManifest:
        """Download dicionário de dados with SHA-256 manifest."""
        return self.client.download_with_manifest(
            INFOSIGA_DICIONARIO_ZIP_URL,
            dest,
            manifest_path=manifest_path,
        )
