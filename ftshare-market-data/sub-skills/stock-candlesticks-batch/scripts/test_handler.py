#!/usr/bin/env python3
"""Tests for stock-candlesticks-batch handler"""
import json
import os
import sys
import unittest
import urllib.error
from io import BytesIO, StringIO
from unittest.mock import patch
import importlib.util

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)

SINCE = "1756431000000"
UNTIL = "1756791000000"


class TestBuildBody(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_required_only(self):
        body = handler.build_body(["600519.SH"], "Day", "None", 1756431000000, 1756791000000, None)
        self.assertEqual(body["symbols"], ["600519.SH"])
        self.assertEqual(body["interval_unit"], "Day")
        self.assertEqual(body["since_ts_millis"], 1756431000000)
        self.assertNotIn("adjust_kind", body)
        self.assertNotIn("limit", body)
        self.assertNotIn("interval_value", body)

    def test_minute_not_allowed(self):
        with self.assertRaises(SystemExit):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "600519.SH",
                                            "--interval-unit", "Minute",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                handler.main()


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_get_to_stock_batch_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(["600519.SH", "000001.SZ"], "Day", "None",
                      1756431000000, 1756791000000, 2)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v2/market/data/stock-candlesticks/batch", req.full_url)
        self.assertIn("since_ts_millis=1756431000000", req.full_url)
        self.assertIsNone(req.data)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch(["600519.SH"], "Day", "None", 1756431000000, 1756791000000, None)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", [
                "handler.py", "--symbols", "600519.SH,000001.SZ",
                "--interval-unit", "Day",
                "--since-ts-millis", SINCE, "--until-ts-millis", UNTIL
            ]):
                with patch("sys.stdout", new_callable=StringIO) as fake_out:
                    handler.main()
                    self.assertEqual(json.loads(fake_out.getvalue()), [])

    def test_main_requires_since(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "600519.SH",
                                            "--interval-unit", "Day",
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_since_after_until(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "600519.SH",
                                            "--interval-unit", "Day",
                                            "--since-ts-millis", UNTIL,
                                            "--until-ts-millis", SINCE]):
                with self.assertRaises(SystemExit):
                    handler.main()

    @patch.object(handler, "safe_urlopen")
    def test_interval_unit_case_insensitive(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "600519.SH",
                                            "--interval-unit", "day",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                handler.main()
        req = mock_open.call_args[0][0]
        self.assertIn("interval_unit=Day", req.full_url)


if __name__ == "__main__":
    unittest.main()
