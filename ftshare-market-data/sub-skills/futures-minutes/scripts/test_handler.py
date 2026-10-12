#!/usr/bin/env python3
"""Tests for futures-minutes handler"""
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


class TestBuildQuery(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_single_symbol_query(self):
        body = handler.build_query("A2611.DCE", None, "5min", 1791475200000, 1791647999000, 5)
        self.assertEqual(body["symbol"], "A2611.DCE")
        self.assertNotIn("symbols", body)
        self.assertEqual(body["interval"], "5min")
        self.assertEqual(body["start"], 1791475200000)
        self.assertEqual(body["end"], 1791647999000)
        self.assertEqual(body["limit"], 5)

    def test_batch_symbols_query(self):
        body = handler.build_query(None, ["A2611.DCE", "CU2611.SHF"], "1min", 1791475200000, 1791647999000, None)
        self.assertNotIn("symbol", body)
        self.assertEqual(body["symbols"], ["A2611.DCE", "CU2611.SHF"])
        self.assertNotIn("limit", body)

    def test_rejects_too_many_symbols(self):
        with self.assertRaises(SystemExit):
            handler.parse_symbols(",".join(f"A26{i:02d}.DCE" for i in range(21)))


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_expands_symbols(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        handler.fetch(None, ["A2611.DCE", "CU2611.SHF"], "5min", 1791475200000, 1791647999000, 5)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v2/market/data/futures_minutes", req.full_url)
        query = req.full_url.split("?", 1)[1]
        self.assertIn("symbols=A2611.DCE", query)
        self.assertIn("symbols=CU2611.SHF", query)
        self.assertIn("interval=5min", query)
        self.assertIn("start=1791475200000", query)
        self.assertIn("end=1791647999000", query)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_single_symbol_uses_symbol_key(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        handler.fetch("A2611.DCE", None, "1min", 1791475200000, 1791647999000, None)
        query = mock_open.call_args[0][0].full_url.split("?", 1)[1]
        self.assertIn("symbol=A2611.DCE", query)
        self.assertNotIn("symbols=", query)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_single_symbol(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "A2611.DCE",
                                            "--interval", "5min",
                                            "--start", "1791475200000",
                                            "--end", "1791647999000"]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
                    self.assertEqual(json.loads(out.getvalue()), {"code": 200})

    def test_main_requires_target(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py",
                                            "--start", "1791475200000",
                                            "--end", "1791647999000"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_symbol_and_symbols_together(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py",
                                            "--symbol", "A2611.DCE",
                                            "--symbols", "CU2611.SHF",
                                            "--start", "1791475200000",
                                            "--end", "1791647999000"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_requires_start_and_end(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "A2611.DCE"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_limit_out_of_range(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "A2611.DCE",
                                            "--start", "1791475200000",
                                            "--end", "1791647999000",
                                            "--limit", "1001"]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()
