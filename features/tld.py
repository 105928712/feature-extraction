# tld.py
# 2026 Joey Manani & Anchorfish Team
# TLD extractor

# parsed_url = urlparse(url)
# host = parsed_url.hostname
# tld = psl.publicsuffix(host)

# print("Subdomain:", subdomain)
# print("Root Domain:", root_domain)
# print("TLD:", tld)


from .base import Feature
from .utils import psl
from urllib.parse import urlparse

COMMON_ABUSED_TLDS = frozenset({"xyz", "top", "xin", "bond", "buzz", "sbs", "cfd", "lol", "ru", "cc", "shop", "online", "net", "cn", "monster", "world", "win", "support", "vip", "icu", "pro"})

class TLD(Feature):

    name = "tld"
    description = "The top-level domain (TLD) of the URL."

    def extract(self, url: str) -> str:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        tld = psl.publicsuffix(host)

        return tld

class TLDCount(Feature):

    name = "tld_count"
    description = "The number of top-level domains (TLDs) within the URL."

    def extract(self, url:str) -> int:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        tld = psl.publicsuffix(host)
        
        return len(tld.split('.'))

class TLDLength(Feature):

    name = "tld_length"
    description = "Character length of the top-level domain (TLD)."

    def extract(self, url:str) -> int:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        tld = psl.publicsuffix(host)

        return len(tld)

class TLDCommon(Feature):

    name = "commonly_abused_tld"
    description = "If the top-level domain is one that is commonly abused"

    def extract(self, url:str) -> bool:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        tld = psl.publicsuffix(host)

        return any(label in COMMON_ABUSED_TLDS for label in tld.lower())
        
