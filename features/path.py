#path.py
# 2026 Joey Manani & Anchorfish Team
# Path extractors

from urllib.parse import urlsplit
from .base import Feature

class PathLevel(Feature):
    name = "path_level"
    description = "The depth of the URL path."

    def extract(self, url: str) -> int:
        path = urlsplit(url).path.strip("/")
        if not path:
            return 0
        return len(path.split("/"))

class PathLength(Feature):
    name = "path_length"
    description = "The character length of the URL path."

    def extract(self, url: str) -> int:
        return len(urlsplit(url).path)

class DoubleSlashPath(Feature):
    name = "double_slash_path"
    description = "Whether the URL path contains a double slash (//)."

    def extract(self, url: str) -> int:
        return int("//" in urlsplit(url).path)


    
    


