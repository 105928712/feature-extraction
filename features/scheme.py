# 2026 Joey Manani & Anchorfish Team
# Scheme extractor

from .base import Feature


class Scheme(Feature):
    """Extract the URL scheme (e.g. http, https)."""

    name = "scheme"
    description = "The URL scheme (e.g. http, https)."

    def extract(self, url: str) -> str:
        """Extract the URL scheme (e.g. http, https)."""
        return url.split("://")[0]

    @property
    def value(self) -> str:
        """Get the value of the feature."""
        return self.extract(self.url)
