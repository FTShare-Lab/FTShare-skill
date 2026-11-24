#!/usr/bin/env python3
"""Tests for sector-knowledge-search-options handler"""
import json
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with patch("sys.stdout", new_callable=StringIO) as out:
                handler.main()
                return json.loads(out.getvalue())


class TestRequests(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_returns_options_object(self, mock_open):
        payload = {
            "code": 200,
            "data": {
                "fact": {"category_list": [], "searchable_field_list": ["title", "content"], "keyword_match": "substring"},
                "insight": {"category_list": [], "searchable_field_list": ["title", "summary"], "keyword_match": "substring"},
                "sector_type_list": ["industry"],
                "market_list": ["CN"],
                "sort": {"fact": ["relevance"], "insight": ["relevance"]},
            },
        }
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(payload).encode()
        result = _run([])
        req = mock_open.call_args[0][0]
        self.assertEqual(req.full_url, handler.BASE_URL + handler.ENDPOINT)
        self.assertEqual(result["data"]["fact"]["keyword_match"], "substring")


if __name__ == "__main__":
    unittest.main()