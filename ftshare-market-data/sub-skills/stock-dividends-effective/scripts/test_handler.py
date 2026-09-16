#!/usr/bin/env python3
"""Tests for stock-dividends-effective handler"""
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


class TestParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_unpaired_dates(self):
        with self.assertRaises(SystemExit):
            _run(["--since-date", "2026-05-26", "--page", "1", "--page-size", "5"])
        with self.assertRaises(SystemExit):
            _run(["--until-date", "2026-05-26", "--page", "1", "--page-size", "5"])

    @patch.object(handler, "safe_urlopen")
    def test_query_mapping(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run(["--symbol", "002043.SZ", "--since-date", "2026-05-26",
              "--until-date", "2026-05-26", "--page", "1", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/stock-dividends-effective", req.full_url)
        self.assertIn("symbol=002043.SZ", req.full_url)
        self.assertIn("since_date=2026-05-26", req.full_url)
        self.assertIn("until_date=2026-05-26", req.full_url)


class TestFetchAll(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_pages(self, mock_open):
        page1 = {"code": 200, "data": {"records": [{"symbol": "600519.SH"}], "pages": 2, "total": 2}}
        page2 = {"code": 200, "data": {"records": [{"symbol": "000028.SZ"}], "pages": 2, "total": 2}}
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            json.dumps(page1).encode(), json.dumps(page2).encode(),
        ]
        result = _run(["--page", "1", "--page-size", "1", "--all"])
        self.assertEqual(len(result["records"]), 2)
        self.assertEqual(result["total"], 2)


if __name__ == "__main__":
    unittest.main()
