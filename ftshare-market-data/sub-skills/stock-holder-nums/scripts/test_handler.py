#!/usr/bin/env python3
"""Tests for stock-holder-nums handler"""
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
    def test_fetch_by_stock_code(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("000001.SZ", False, None, None)
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/holder/stock-holder-nums", url)
        self.assertIn("stock_code=000001.SZ", url)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_is_last_paging(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(None, True, 1, 50)
        url = mock_open.call_args[0][0]
        self.assertIn("is_last=true", url)
        self.assertIn("page=1", url)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json_for_stock_code(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", ["handler.py", "--stock_code", "000001.SZ"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                self.assertEqual(json.loads(fake_out.getvalue()), [])

    def test_main_requires_stock_code_or_is_last(self):
        with patch.object(sys, "argv", ["handler.py"]):
            with self.assertRaises(SystemExit):
                handler.main()


if __name__ == "__main__":
    unittest.main()
