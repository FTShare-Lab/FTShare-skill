#!/usr/bin/env python3
"""Tests for futures-realtime-minute-kline handler"""
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


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_expands_symbols(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        handler.fetch(["A2611.DCE", "CU2611.SHF"])
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v4/market/data/futures_minutes/realtime", req.full_url)
        query = req.full_url.split("?", 1)[1]
        self.assertIn("symbols=A2611.DCE", query)
        self.assertIn("symbols=CU2611.SHF", query)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    def test_rejects_too_many_symbols(self):
        with self.assertRaises(SystemExit):
            handler.parse_symbols(",".join(f"A26{i:02d}.DCE" for i in range(21)))


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "A2611.DCE,CU2611.SHF"]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
                    self.assertEqual(json.loads(out.getvalue()), {"code": 200})

    def test_main_requires_symbols(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py"]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()
