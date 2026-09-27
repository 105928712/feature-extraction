# test_bad_input.py
# 2026 Joey Manani & Anchorfish Team
# Checks that messy URLs don't crash the extractor
# Run from the repo root: python -m unittest discover tests

import unittest

import features
from features.utils import canonical_url

BAD_URLS = [
    "http://",                                                         # missing host
    "",                                                                # empty
    "https://c...content-available-to-author-only...e.org/search?q=",  # empty host labels, no public suffix
    "http://[::1/path",                                                # unclosed IPv6 bracket -> ValueError
    "abc]def.com/login",                                               # stray bracket -> ValueError
    "\x8aRybj\x18\x0f|U[\x1a\x07",                                     # binary junk
    "localhost",                                                       # localhost url
    "http://43.156.237.181/v3/signin?dsh=1",                           # ip address (old crash bug that was fixed but still worth testing)
    "зачемвыэтопереводите.рф/вход",                                    # stray russian url with kinda bad tld and unicode
]


class ExtractorSurvivesBadInput(unittest.TestCase):

    def test_no_feature_raises(self):
        for url in BAD_URLS:
            with self.subTest(url=url):
                features.extract_features(url)

    def test_ip_host_has_no_tld_or_root_domain(self):
        row = features.extract_features("http://43.156.237.181/v3/signin")
        self.assertEqual((row["tld"], row["tld_count"], row["root_domain"]), ("", 0, ""))

    def test_scheme_later_in_url_still_gets_a_host(self):
        # schemeless URL with a redirect target in the query used to parse with an empty host
        row = features.extract_features("site.com/redirect?to=http://evil.com")
        self.assertEqual(row["root_domain"], "site")

    def test_normal_url_values_unchanged(self):
        row = features.extract_features("https://login.example.co.uk/a/b?x=1&y=2")
        self.assertEqual(row["tld"], "co.uk")
        self.assertEqual(row["tld_count"], 2)
        self.assertEqual(row["root_domain"], "example")
        self.assertEqual(row["root_domain_length"], 7)
        self.assertEqual(row["path_level"], 2)
        self.assertEqual(row["num_query_components"], 2)
        self.assertEqual(row["subdomain_count"], 1)


class CanonicalUrl(unittest.TestCase):

    def test_strips_scheme_and_lone_trailing_slash(self):
        self.assertEqual(canonical_url("https://example.com/"), "example.com")
        self.assertEqual(canonical_url("  HTTP://a.com/x "), "a.com/x")
        self.assertEqual(canonical_url("example.com/"), "example.com")

    def test_keeps_meaningful_slashes(self):
        self.assertEqual(canonical_url("http://example.com/path/"), "example.com/path/")
        self.assertEqual(canonical_url("example.com/?q=1"), "example.com/?q=1")

    def test_strips_leading_www(self):
        self.assertEqual(canonical_url("https://www.example.com/"), "example.com")
        self.assertEqual(canonical_url("WWW2.a.com/x"), "a.com/x")


if __name__ == "__main__":
    unittest.main()
