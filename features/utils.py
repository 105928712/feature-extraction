# utils.py
# 2026 Joey Manani & Anchorfish Team
# Shared helpers

def normalise_url(url: str) -> str:
    """Strip whitespace and add http:// if the URL has no scheme."""
    url = url.strip()
    if "://" not in url:
        url = "http://" + url
    return url