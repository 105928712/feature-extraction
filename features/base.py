# base.py
# 2026 Joey Manani & Anchorfish Team
# Base feature extractor


class Feature:
    """Base class for URL feature extractors."""

    name = ""
    description = ""

    def __init__(self, url: str) -> None:
        self.url = url

    def extract(self, url: str):
        """Extract this feature from a URL."""
        raise NotImplementedError

    @property
    def value(self):
        """The feature extracted from self.url."""
        return self.extract(self.url)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(url={self.url!r})"
