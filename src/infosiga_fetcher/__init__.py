"""Coletor e conversor Lake Hive de sinistros de trânsito de SP (INFOSIGA)."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("infosiga-fetcher")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["__version__"]
