# brand.py
# 2026 Joey Manani & Anchorfish Team
# Brand impersonation extractor

from Levenshtein import distance as levenshtein

from .base import Feature
from .utils import get_host, psl

COMMON_BRANDS = frozenset({
    "paypal", "apple", "microsoft", "google", "amazon", "facebook",
    "instagram", "netflix", "bankofamerica", "wellsfargo", "chase",
    "dhl", "fedex", "ebay", "linkedin", "whatsapp", "outlook",
    "office365", "adobe", "americanexpress", "hsbc", "icloud", "usps",
})


def _root_label(url: str) -> str:
    host = get_host(url)
    if not host:
        return ""
    registrable = psl.privatesuffix(host)
    if not registrable:
        return host
    tld = psl.publicsuffix(host)
    return registrable.rsplit("." + tld, 1)[0] if tld else registrable


class BrandEditDistance(Feature):
    """How close the root domain is to a known brand name - low distance + wrong domain = typosquatting."""
    name = "brand_edit_distance"
    description = "Smallest edit distance between the root domain and a list of commonly impersonated brand names."

    def extract(self, url: str) -> int:
        root = _root_label(url)
        return min(levenshtein(root, brand) for brand in COMMON_BRANDS)
