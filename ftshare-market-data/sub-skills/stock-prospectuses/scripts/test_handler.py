#!/usr/bin/env python3
"""Tests for stock-prospectuses handler"""
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


class TestModes(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_requires_code_or_date(self):
        with self.assertRaises(SystemExit):
            _run(["--page", "1", "--page-size", "5"])

    def test_rejects_page_size_over_max(self):
        with self.assertRaises(SystemExit):
            _run(["--stock-code", "600000.SH", "--page-size", "501"])

    def test_rejects_date_range(self):
        with self.assertRaises(SystemExit):
            _run(["--start-date", "20240517", "--end-date", "20240518"])

    @patch.object(handler, "safe_urlopen")
    def test_by_symbol(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run(["--stock-code", "600000.SH", "--page", "1", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/announcements/stock-prospectuses", req.full_url)
        self.assertIn("stock_code=600000.SH", req.full_url)
        self.assertIn("page=1", req.full_url)
        self.assertIn("page_size=5", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_by_single_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run(["--start-date", "20240517", "--page", "1", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("start_date=20240517", req.full_url)
        self.assertNotIn("end_date", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_symbol_wins_over_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run(["--stock-code", "600000.SH", "--start-date", "20240517"])
        req = mock_open.call_args[0][0]
        self.assertIn("stock_code=600000.SH", req.full_url)
        self.assertIn("start_date=20240517", req.full_url)


class TestFetchAll(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_pages(self, mock_open):
        page1 = {"code": 200, "data": {"records": [{"url_hash": "a"}], "pages": 2, "total": 2}}
        page2 = {"code": 200, "data": {"records": [{"url_hash": "b"}], "pages": 2, "total": 2}}
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            json.dumps(page1).encode(), json.dumps(page2).encode(),
        ]
        result = _run(["--start-date", "20240517", "--page", "1", "--page-size", "1", "--all"])
        self.assertEqual([r["url_hash"] for r in result["records"]], ["a", "b"])
        self.assertEqual(result["total"], 2)
        second_req = mock_open.call_args_list[1][0][0]
        self.assertIn("page=2", second_req.full_url)


if __name__ == "__main__":
    unittest.main()
