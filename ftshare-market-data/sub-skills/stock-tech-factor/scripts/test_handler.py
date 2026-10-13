#!/usr/bin/env python3
"""Tests for stock-tech-factor handler"""
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


class TestParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_omits_optional_fields_when_absent(self):
        args = type("Args", (), {"symbol": "000001.SZ", "trade_date": None, "category": None})
        self.assertEqual(handler.build_params(args), {"symbol": "000001.SZ"})

    def test_includes_optional_fields_when_present(self):
        args = type("Args", (), {"symbol": "000001.SZ", "trade_date": "20261012", "category": "trend"})
        params = handler.build_params(args)
        self.assertEqual(params["trade_date"], "20261012")
        self.assertEqual(params["category"], "trend")


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_forwards_query(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        handler.fetch({"symbol": "000001.SZ", "trade_date": "20261012", "category": "trend"})
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/stock-factor", url)
        self.assertIn("symbol=000001.SZ", url)
        self.assertIn("trade_date=20261012", url)
        self.assertIn("category=trend", url)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200,"data":{"values":{}}}'
        result = _run(["--symbol", "000001.SZ", "--category", "trend"])
        self.assertEqual(result["data"]["values"], {})


if __name__ == "__main__":
    unittest.main()
