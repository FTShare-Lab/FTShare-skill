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


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_forwards_stock_code_and_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("000001.SZ", "20260716")
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/share/get-stock-share", url)
        self.assertIn("stock_code=000001.SZ", url)
        self.assertIn("date=20260716", url)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", ["handler.py", "--stock_code", "000001.SZ", "--date", "20260716"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                self.assertEqual(json.loads(fake_out.getvalue()), [])


if __name__ == "__main__":
    unittest.main()
