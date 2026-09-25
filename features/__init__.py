# __init__.py
# 2026 Joey Manani & Anchorfish Team

from .base import Feature
from .path import PathLevel, PathLength, DoubleSlashPath
from .query import QueryLength, NumQueryComponents
from .entropy import Entropy, HostEntropy, PathEntropy, QueryEntropy
from .scheme import Scheme
from .subdomain import HasWww, SubdomainCount, SubdomainLength, SubdomainMaxLabelLength, SubdomainEntropy, SubdomainDigitRatio, SubdomainHyphenCount, SubdomainHasPunycode, SubdomainHasEmbeddedTLD
from .tld import TLD, TLDCount, TLDLength
from .utils import normalise_url
from .sens_words import NumSensitiveWords

FEATURES = [Scheme, PathLevel, PathLength, DoubleSlashPath, QueryLength, NumQueryComponents, Entropy, HostEntropy, PathEntropy, QueryEntropy, HasWww, SubdomainCount, SubdomainLength, SubdomainMaxLabelLength, SubdomainEntropy, SubdomainDigitRatio, SubdomainHyphenCount, SubdomainHasPunycode, SubdomainHasEmbeddedTLD, TLD, TLDCount, TLDLength, NumSensitiveWords]

def extract_features(url: str) -> dict:
    """Normalise a URL and run every feature on it."""
    url = normalise_url(url)
    return {f.name: f(url).value for f in FEATURES}

# public api exports
__all__ = ["Feature", "extract_features", *[f.__name__ for f in FEATURES]]
