#!/usr/bin/env python3
"""Tests for futures-kline-batch handler"""
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

    def test_batch_query(self):
        body = handler.build_query(["A2611.DCE", "M2611.DCE"], "daily", 1790784000000, 1791647999000, 5)
        self.assertEqual(body["symbols"], ["A2611.DCE", "M2611.DCE"])
        self.assertEqual(body["interval"], "daily")
        self.assertEqual(body["start"], 1790784000000)
        self.assertEqual(body["end"], 1791647999000)
        self.assertEqual(body["limit"], 5)

    def test_omits_optional_params(self):
        body = handler.build_query(["A2611.DCE"], "weekly", None, None, None)
        self.assertNotIn("start", body)
        self.assertNotIn("end", body)
        self.assertNotIn("limit", body)
        self.assertEqual(body["interval"], "weekly")

    def test_rejects_too_many_symbols(self):
        with self.assertRaises(SystemExit):
            handler.parse_symbols(",".join(f"A26{i:02d}.DCE" for i in range(21)))


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_expands_symbols(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        handler.fetch(["A2611.DCE", "M2611.DCE"], "daily", 1790784000000, 1791647999000, 5)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v2/market/data/futures/kline/batch", req.full_url)
        query = req.full_url.split("?", 1)[1]
        self.assertIn("symbols=A2611.DCE", query)
        self.assertIn("symbols=M2611.DCE", query)
        self.assertIn("interval=daily", query)
        self.assertIn("start=1790784000000", query)
        self.assertIn("limit=5", query)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_batch(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200}'
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "A2611.DCE,M2611.DCE",
                                            "--interval", "daily", "--limit", "5"]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
                    self.assertEqual(json.loads(out.getvalue()), {"code": 200})

    def test_main_rejects_end_without_start(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "A2611.DCE",
                                            "--end", "1791647999000"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_requires_symbols(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--interval", "daily"]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()
