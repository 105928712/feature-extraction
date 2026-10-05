# test_merge.py
# 2026 Joey Manani & Anchorfish Team

import unittest

from scripts.merge_datasets import merge


class MergeDropsDuplicatesAndConflicts(unittest.TestCase):

    def test_merge(self):
        rows = [
            ("a.com", "Legitimate"),
            ("b.com/login", "Phishing"),
            ("a.com", "Legitimate"),     # duplicate from another source -> one copy kept
            ("c.com", "Legitimate"),
            ("c.com", "Phishing"),       # conflict -> both dropped
        ]
        kept, duplicates, conflicts = merge(rows)
        self.assertEqual(kept, [
            {"url": "a.com", "type": "Legitimate"},
            {"url": "b.com/login", "type": "Phishing"},
        ])
        self.assertEqual(duplicates, 1)
        self.assertEqual(conflicts, 2)
