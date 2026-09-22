# 2026 Joey Manani & Anchorfish Team
# Subdomain extractor

from .base import Feature


class Subdomain(Feature):
    """Extract the URL subdomain (e.g. www)."""

    name = "subdomain"
    description = "The URL subdomain (e.g. www, etc)."

    def extract(self, url: str) -> str:
        """Extract the URL subdomain (e.g. www, etc)."""
        subdomain = url.split(".")[0]
        return subdomain.split("://")[1]

    @property
    def value(self) -> str:
        """Get the value of the feature."""
        return self.extract(self.url)
