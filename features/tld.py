# from urllib.parse import urlparse
# from publicsuffixlist import PublicSuffixList

# psl = PublicSuffixList()
# url = "https://www.ooo.www.syntaxscenarios.aero/category/python"

# parsed_url = urlparse(url)
# host = parsed_url.hostname
# # 'www.syntaxscenarios.com'
# tld = psl.publicsuffix(host)
# # 'com'
# parts = host.rsplit("." + tld, 1)[0].split('.')
# subdomain = ".".join(parts[:-1])
# # 'www'
# root_domain = parts[-1]
# # 'syntaxscenarios'

# print("Subdomain:", subdomain)
# print("Root Domain:", root_domain)
# print("TLD:", tld)

# scheme.py
# 2026 Joey Manani & Anchorfish Team
# TLD extractor


from .base import Feature

class TLD(Feature):
    """Extract the top-level domain (TLD) of the URL."""

    name = "tld"
    description = "The top-level domain (TLD) of the URL."

    def extract(self, url: str) -> str:
        raise NotImplementedError
