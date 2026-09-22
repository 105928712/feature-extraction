# entropy.py
# 2026 Joey Manani & Anchorfish Team
# Entropy extractors

from functools import lru_cache
from urllib.parse import urlsplit

from .base import Feature
from .utils import get_host, shannon_entropy


@lru_cache(maxsize=1024)
def _split(url: str):
    try:
        return urlsplit(url)
    except ValueError:
        return None


class Entropy(Feature):
    name = "entropy"
    description = "Shannon entropy of the whole URL."

    def extract(self, url: str) -> float:
        return shannon_entropy(url)


class HostEntropy(Feature):
    name = "host_entropy"
    description = "Shannon entropy of the hostname."

    def extract(self, url: str) -> float:
        return shannon_entropy(get_host(url))


class PathEntropy(Feature):
    name = "path_entropy"
    description = "Shannon entropy of the path."

    def extract(self, url: str) -> float:
        parts = _split(url)
        return shannon_entropy(parts.path) if parts else 0.0


class QueryEntropy(Feature):
    name = "query_entropy"
    description = "Shannon entropy of the query string."

    def extract(self, url: str) -> float:
        parts = _split(url)
        return shannon_entropy(parts.query) if parts else 0.0
