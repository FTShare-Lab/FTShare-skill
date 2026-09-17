#!/usr/bin/env python3
"""Tests for convertible-bond-minutes handler"""
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

SINCE = "1786291200000"
UNTIL = "1786377599999"


class TestBuildQuery(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_single_symbol_query(self):
        body = handler.build_query("113042.SH", None, None, 1786291200000, 1786377599999, 1)
        self.assertEqual(body["symbol"], "113042.SH")
        self.assertNotIn("symbols", body)
        self.assertNotIn("interval_value", body)
        self.assertEqual(body["limit"], 1)

    def test_batch_symbols_query(self):
        body = handler.build_query(None, ["113042.SH", "123107.SZ"], 5,
                                   1786291200000, 1786377599999, None)
        self.assertNotIn("symbol", body)
        self.assertEqual(body["symbols"], ["113042.SH", "123107.SZ"])
        self.assertEqual(body["interval_value"], 5)
        self.assertNotIn("limit", body)

    def test_rejects_too_many_symbols(self):
        with self.assertRaises(SystemExit):
            handler.parse_symbols(",".join(f"11304{i}.SH" for i in range(21)))


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_expands_symbols(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(None, ["113042.SH", "123107.SZ"], 1, 1786291200000, 1786377599999, 1)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v2/market/data/convertible-bond-minute-candlesticks", req.full_url)
        query = req.full_url.split("?", 1)[1]
        self.assertIn("symbols=113042.SH", query)
        self.assertIn("symbols=123107.SZ", query)
        self.assertIn("interval_value=1", query)
        self.assertIn("since_ts_millis=1786291200000", query)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_single_symbol_uses_symbol_key(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("113042.SH", None, None, 1786291200000, 1786377599999, None)
        query = mock_open.call_args[0][0].full_url.split("?", 1)[1]
        self.assertIn("symbol=113042.SH", query)
        self.assertNotIn("symbols=", query)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_single_symbol(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "113042.SH",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
                    self.assertEqual(json.loads(out.getvalue()), [])

    def test_main_requires_target(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_symbol_and_symbols_together(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py",
                                            "--symbol", "113042.SH",
                                            "--symbols", "123107.SZ",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_bad_interval_value(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "113042.SH",
                                            "--interval-value", "7",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_limit_out_of_range(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "113042.SH",
                                            "--limit", "1001",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()