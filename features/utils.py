# utils.py
# 2026 Joey Manani & Anchorfish Team
# Shared helpers

import ipaddress
import re
from collections import Counter
from functools import lru_cache
from math import log2
from urllib.parse import urlsplit

from publicsuffixlist import PublicSuffixList

psl = PublicSuffixList(only_icann=True)  # ignore private suffixes (github.io etc.)
WWW_LABEL = re.compile(r"www\d*")        # www, www1, www2...


def normalise_url(url: str) -> str:
    """Strip whitespace and add http:// if the URL has no scheme."""
    url = url.strip()
    if "://" not in url:
        url = "http://" + url
    return url


def shannon_entropy(data: str) -> float:
    """H(X) = -sum(p(x) * log2(p(x)))"""
    if not data:
        return 0.0
    n = len(data)
    return -sum((c / n) * log2(c / n) for c in Counter(data).values())


def is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


@lru_cache(maxsize=1024)
def get_host(url: str) -> str:
    """Lowercase hostname, trailing dot removed, unicode converted to punycode."""
    try:
        host = urlsplit(url).hostname
    except ValueError:
        return ""
    if not host:
        return ""
    host = host.rstrip(".")
    try:
        host = host.encode("idna").decode("ascii") # convert to punycode
    except UnicodeError:
        pass
    return host


@lru_cache(maxsize=1024)
def get_subdomain_labels(url: str) -> tuple:
    """Subdomain labels, e.g. ('www', 'login') for www.login.example.com."""
    host = get_host(url)
    if not host or is_ip(host):
        return ()
    registrable = psl.privatesuffix(host)
    if not registrable or registrable == host:
        return ()
    return tuple[str, ...](host[: -len(registrable) - 1].split(".")) 
