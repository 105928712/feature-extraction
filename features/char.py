# char.py
# 2026 Joey Manani & Anchorfish Team
# Character feature extractor

from .base import Feature

class CharCountFeature(Feature):
    """Base for features that count occurrences of a single character."""

    char: str  # set by subclass

    def extract(self, url: str) -> int:
        return url.count(self.char)

class QuestionMarkCount(CharCountFeature):
    """Extract the number of question marks in the URL."""
    name = "question_mark_count"
    description = "The number of question marks in the URL."
    char = "?"

class AmpersandCount(CharCountFeature):
    """Extract the number of ampersands in the URL."""
    name = "ampersand_count"
    description = "The number of ampersands in the URL."
    char = "&"

class DotCount(CharCountFeature):
    """Extract the number of dots in the URL."""
    name = "dot_count"
    description = "The number of dots in the URL."
    char = "."

class SlashCount(CharCountFeature):
    """Extract the number of slashes in the URL."""
    name = "slash_count"
    description = "The number of slashes in the URL."
    char = "/"

class HyphenCount(CharCountFeature):
    """Extract the number of hyphens in the URL."""
    name = "hyphen_count"
    description = "The number of hyphens in the URL."
    char = "-"

class UnderscoreCount(CharCountFeature):
    """Extract the number of underscores in the URL."""
    name = "underscore_count"
    description = "The number of underscores in the URL."
    char = "_"
