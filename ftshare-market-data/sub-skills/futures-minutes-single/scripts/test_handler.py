#!/usr/bin/env python3
"""Tests for futures-minutes-single handler"""
import importlib.util
import json
import os
import sys
import unittest
import urllib.parse
from io import StringIO
from unittest.mock import patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_carries_single_symbol_and_window(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        handler.fetch("A2611", "5min", 1791475200000, 1791647999000, 500)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v2/market/data/futures_minutes/single", req.full_url)
        query = urllib.parse.parse_qs(req.full_url.split("?", 1)[1])
        self.assertEqual(query["symbol"], ["A2611"])
        self.assertEqual(query["interval"], ["5min"])
        self.assertEqual(query["start"], ["1791475200000"])
        self.assertEqual(query["end"], ["1791647999000"])
        self.assertEqual(query["limit"], ["500"])
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_limit_is_omitted_when_not_given(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        handler.fetch("A2611", "1min", 1791475200000, 1791647999000, None)
        query = urllib.parse.parse_qs(mock_open.call_args[0][0].full_url.split("?", 1)[1])
        self.assertNotIn("limit", query)

    def test_rejects_cross_origin_url(self):
        opened = False

        def fail_open(*args, **kwargs):
            nonlocal opened
            opened = True
            raise AssertionError("cross-origin request reached opener")

        with patch.object(handler.SAFE_URLOPENER, "open", fail_open):
            with self.assertRaises(SystemExit):
                handler.safe_urlopen("https://example.invalid/api/v1/market/data/example")
        self.assertFalse(opened)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--symbol", "A2611", "--interval", "5min",
                 "--start", "1791475200000", "--end", "1791647999000", "--limit", "500"],
            ):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
        self.assertEqual(json.loads(out.getvalue()), {"code": 200})

    def test_main_requires_symbol_and_window(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--start", "1791475200000", "--end", "1791647999000"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_reversed_window(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--symbol", "A2611", "--start", "1791647999000", "--end", "1791475200000"],
            ):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_limit_out_of_range(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--symbol", "A2611", "--start", "1791475200000",
                 "--end", "1791647999000", "--limit", "10001"],
            ):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_requires_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--symbol", "A2611", "--start", "1791475200000", "--end", "1791647999000"],
            ):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()