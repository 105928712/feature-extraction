# 2026 Joey Manani & Anchorfish Team
# Base feature extractor


class Feature:
    """Base class for URL feature extractors."""

    name = ""
    description = ""

    def __init__(self, url: str = "") -> None:
        self.url = url

    def extract(self, url: str) -> str:
        """Extract this feature from a URL."""
        raise NotImplementedError
