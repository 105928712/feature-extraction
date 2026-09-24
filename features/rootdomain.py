# rootdomain.py
# 2026 Joey Manani & Anchorfish Team
# Root Domain extractor

from .base import Feature
from .utils import psl
from urllib.parse import urlparse

class RootDomain(Feature):

    name = "root_domain"
    description = "The Root Domain of the URL."

    def extract(self, url: str) -> str:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        tld = psl.publicsuffix(host)

        parts = host.rsplit("." + tld, 1)[0].split('.')
        root_domain = parts[-1]
    
        return root_domain
