#query.py
# 2026 Joey Manani & Anchorfish Team
# Query extractors  

from urllib.parse import urlsplit, parse_qsl
from .base import Feature

class QueryLength(Feature):
    name = "query_length"
    description = "The character length of the URL query string."

    def extract(self, url: str) -> int:
        return len(urlsplit(url).query)

class NumQueryComponents(Feature):
    name = "num_query_components"
    description = "The number of query components in the URL."

    def extract(self, url: str) -> int:
        query = urlsplit(url).query

        if not query: 
            return 0
        
        return len(parse_qsl(query, keep_blank_values=True))