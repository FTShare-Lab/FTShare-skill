#!/usr/bin/env python3
"""Tests for stock-candlesticks handler"""
import json
import sys
import unittest
import urllib.error
from io import BytesIO, StringIO
from unittest.mock import patch
import importlib.util
import os

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


class TestBuildBody(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_required_fields(self):
        b = handler.build_body("600519.SH", "Day", 1, "None", None, 1756791000000, None)
        self.assertEqual(b["symbol"], "600519.SH")
        self.assertEqual(b["interval_unit"], "Day")
        self.assertEqual(b["until_ts_millis"], 1756791000000)
        self.assertNotIn("interval_value", b)

    def test_optional_fields(self):
        b = handler.build_body("000001.SZ", "Minute", 5, "Forward",
                               1756700000000, 1756791000000, 100)
        self.assertEqual(b["interval_value"], 5)
        self.assertEqual(b["adjust_kind"], "Forward")
        self.assertEqual(b["limit"], 100)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_get_to_stock_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("600519.SH", "Day", 1, "None", None, 1756791000000, 5)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v1/market/data/stock-candlesticks", req.full_url)
        self.assertIsNone(req.data)
        self.assertIn("symbol=600519.SH", req.full_url)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch("600519.SH", "Day", 1, "None", None, 1756791000000, None)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'[{"open":"10.5","high":"10.6","low":"10.4","close":"10.55",'
            b'"ts_millis":1756710000000,"ts_millis_open":1756690200000,'
            b'"turnover":"100","volume":1000}]'
        )
        with patch.object(sys, "argv", [
            "handler.py", "--symbol", "600519.SH", "--interval-unit", "Day",
            "--until-ts-millis", "1756791000000"
        ]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                data = json.loads(fake_out.getvalue())
                self.assertEqual(data[0]["close"], "10.55")


class TestSafeUrlopen(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_wrong_host(self):
        with self.assertRaises(SystemExit):
            handler.safe_urlopen("https://evil.com/api")


if __name__ == "__main__":
    unittest.main()
