# rootdomain.py
# 2026 Joey Manani & Anchorfish Team
# Root Domain extractor

from .base import Feature
from .utils import psl
from .utils import shannon_entropy
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

class RootDomainLength(Feature):

    name = "root_domain_length"
    description = "The length of the Root Domain"

    def extract(self, url: str) -> str:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        tld = psl.publicsuffix(host)
    
        parts = host.rsplit("." + tld, 1)[0].split('.')
        root_domain = parts[-1]
        
        return len(root_domain)

class RootDomainHasHyphen(Feature):

    name = "root_domain_has_hyphen"
    description = "Whether the Root Domain has hyphens."

    def extract(self, url: str) -> bool:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            tld = psl.publicsuffix(host)
        
            parts = host.rsplit("." + tld, 1)[0].split('.')
            root_domain = parts[-1]
            
            return "-" in root_domain

class RootDomainHyphenCount(Feature):

    name = "root_domain_hyphen_count"
    description = "How many hyphens the Root Domain has."

    def extract(self, url: str) -> int:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            tld = psl.publicsuffix(host)
        
            parts = host.rsplit("." + tld, 1)[0].split('.')
            root_domain = parts[-1]
            
            return root_domain.count('-')

class RootDomainHasNumber(Feature):

    name = "root_domain_has_number"
    description = "Whether the Root Domain has numbers."

    def extract(self, url: str) -> bool:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            tld = psl.publicsuffix(host)
        
            parts = host.rsplit("." + tld, 1)[0].split('.')
            root_domain = parts[-1]
            
            return any(label.isdigit() for label in root_domain)

class RootDomainNumberCount(Feature):

    name = "root_domain_number_count"
    description = "How many numbers the Root Domain has."

    def extract(self, url: str) -> int:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            tld = psl.publicsuffix(host)
        
            parts = host.rsplit("." + tld, 1)[0].split('.')
            root_domain = parts[-1]
            
            return sum(label.isdigit() for label in root_domain)

class RootDomainEntropy(Feature):

    name = "root_domain_entropy"
    description = "The Shannon Entropy of the Root Domain."

    def extract(self, url: str) -> float:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            tld = psl.publicsuffix(host)
        
            parts = host.rsplit("." + tld, 1)[0].split('.')
            root_domain = parts[-1]
            
            return shannon_entropy(root_domain)