"""Tests for InfosigaClient."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from quantilica.core.manifests import DownloadManifest

from infosiga_fetcher.client import InfosigaClient


def test_client_init() -> None:
    client = InfosigaClient()
    assert client.client is not None


def test_get_min_max_dates() -> None:
    client = InfosigaClient()
    fake_data = {"minDate": "2015-01-01", "maxDate": "2026-09-30"}
    with patch.object(client.client, "get_json", return_value=fake_data):
        res = client.get_min_max_dates()
        assert res["maxDate"] == "2026-09-30"


def test_download_dados(tmp_path) -> None:
    client = InfosigaClient()
    target = tmp_path / "dados.zip"
    mock_manifest = MagicMock(spec=DownloadManifest)
    with patch.object(
        client.client, "download_with_manifest", return_value=mock_manifest
    ):
        res = client.download_dados(target)
        assert res == mock_manifest


def test_download_dicionario(tmp_path) -> None:
    client = InfosigaClient()
    target = tmp_path / "dicionario.zip"
    mock_manifest = MagicMock(spec=DownloadManifest)
    with patch.object(
        client.client, "download_with_manifest", return_value=mock_manifest
    ):
        res = client.download_dicionario(target)
        assert res == mock_manifest
