#!/usr/bin/env python3
"""Tests for stock-share handler"""
import json
import sys
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util
import os

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with patch("sys.stdout", new_callable=StringIO) as out:
                handler.main()
                return json.loads(out.getvalue())


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_forwards_stock_code_and_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch({"stock_code": "000001.SZ", "date": "20260716"})
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/share/get-stock-share", url)
        self.assertIn("stock_code=000001.SZ", url)
        self.assertIn("date=20260716", url)


class TestParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def _ns(self, **overrides):
        defaults = {"stock_code": None, "date": "20260716", "date_type": None,
                    "page": 1, "page_size": 200}
        defaults.update(overrides)
        return type("Args", (), defaults)

    def test_single_stock_omits_pagination(self):
        params = handler.build_params(self._ns(stock_code="920476.BJ", date_type="end_date"))
        self.assertEqual(params["stock_code"], "920476.BJ")
        self.assertEqual(params["date"], "20260716")
        self.assertEqual(params["date_type"], "end_date")
        self.assertNotIn("page", params)
        self.assertNotIn("page_size", params)

    def test_market_wide_includes_pagination(self):
        params = handler.build_params(self._ns(stock_code=None, page=2, page_size=5))
        self.assertNotIn("stock_code", params)
        self.assertEqual(params["page"], 2)
        self.assertEqual(params["page_size"], 5)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        result = _run(["--stock_code", "000001.SZ", "--date", "20260716"])
        self.assertEqual(result, [])


class TestFetchAll(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_pages(self, mock_open):
        page1 = {"code": 200, "data": {"items": [{"stock_code": "920476.BJ"}], "total_pages": 2, "total_items": 2}}
        page2 = {"code": 200, "data": {"items": [{"stock_code": "000001.SZ"}], "total_pages": 2, "total_items": 2}}
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            json.dumps(page1).encode(), json.dumps(page2).encode(),
        ]
        result = _run(["--date", "20261012", "--page_size", "1", "--all"])
        self.assertEqual(len(result["data"]["items"]), 2)
        self.assertEqual(result["data"]["total_pages"], 2)


if __name__ == "__main__":
    unittest.main()
