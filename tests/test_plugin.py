"""Tests for infosiga-fetcher Typer plugin."""

import re

from typer.testing import CliRunner

from infosiga_fetcher.plugin import app


def test_cli_list() -> None:
    """Test quantilica infosiga list."""
    runner = CliRunner()
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "dados" in result.output
    assert "dados_infosiga" in result.output


def test_cli_convert_help() -> None:
    """Test quantilica infosiga convert --help."""
    runner = CliRunner()
    result = runner.invoke(app, ["convert", "--help"])
    assert result.exit_code == 0
    assert "--lake" in re.sub(r"\x1b\[[0-9;]*m", "", result.output)
