#!/usr/bin/env python3
"""Tests for etf-candlesticks handler"""
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
        b = handler.build_body("510300.XSHG", "Day", 1, "None", None, 1756791000000, None)
        self.assertEqual(b["symbol"], "510300.XSHG")
        self.assertEqual(b["interval_unit"], "Day")
        self.assertEqual(b["until_ts_millis"], 1756791000000)
        self.assertNotIn("interval_value", b)
        self.assertNotIn("adjust_kind", b)
        self.assertNotIn("since_ts_millis", b)
        self.assertNotIn("limit", b)

    def test_optional_fields(self):
        b = handler.build_body("510300.XSHG", "Minute", 5, "Forward",
                               1756700000000, 1756791000000, 100)
        self.assertEqual(b["interval_value"], 5)
        self.assertEqual(b["adjust_kind"], "Forward")
        self.assertEqual(b["since_ts_millis"], 1756700000000)
        self.assertEqual(b["limit"], 100)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_post_body_sent(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("510300.XSHG", "Day", 1, "None", None, 1756791000000, 5)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v1/market/data/etf-candlesticks", req.full_url)
        self.assertIsNone(req.data)
        self.assertEqual(req.full_url.split("?", 1)[1], "symbol=510300.XSHG&interval_unit=Day&until_ts_millis=1756791000000&limit=5")
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")
        self.assertEqual(req.headers.get("Content-type"), "application/json")

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch("510300.XSHG", "Day", 1, "None", None, 1756791000000, None)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'[{"open":"4.5","high":"4.6","low":"4.4","close":"4.55","ts_millis":1756710000000,'
            b'"ts_millis_open":1756690200000,"turnover":"100","volume":1000}]'
        )
        with patch.object(sys, "argv", [
            "handler.py", "--symbol", "510300.XSHG", "--interval-unit", "Day",
            "--until-ts-millis", "1756791000000", "--limit", "5"
        ]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                data = json.loads(fake_out.getvalue())
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["close"], "4.55")

    def test_main_missing_until_exits(self):
        with patch.object(sys, "argv", [
            "handler.py", "--symbol", "510300.XSHG", "--interval-unit", "Day"
        ]):
            with self.assertRaises(SystemExit):
                handler.main()


class TestSafeUrlopen(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_wrong_host(self):
        with self.assertRaises(SystemExit):
            handler.safe_urlopen("https://evil.com/api")


if __name__ == "__main__":
    unittest.main()
