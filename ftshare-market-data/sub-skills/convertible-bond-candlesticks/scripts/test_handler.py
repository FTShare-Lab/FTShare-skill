#!/usr/bin/env python3
"""Tests for convertible-bond-candlesticks handler"""
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

SINCE = 1786291200000
UNTIL = 1786377599999


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_get_to_cb_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("113042.SH", "day", "none", SINCE, UNTIL, 1)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v1/market/data/convertible-bond-candlesticks", req.full_url)
        self.assertIsNone(req.data)
        self.assertIn("symbol=113042.SH", req.full_url)
        self.assertIn(f"since_ts_millis={SINCE}", req.full_url)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch("113042.SH", "day", "none", SINCE, UNTIL, None)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", [
                "handler.py", "--symbol", "113042.SH", "--interval-unit", "day",
                "--since-ts-millis", str(SINCE), "--until-ts-millis", str(UNTIL)
            ]):
                with patch("sys.stdout", new_callable=StringIO) as fake_out:
                    handler.main()
                    self.assertEqual(json.loads(fake_out.getvalue()), [])

    def test_main_requires_since(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", [
                "handler.py", "--symbol", "113042.SH", "--interval-unit", "day",
                "--until-ts-millis", str(UNTIL)
            ]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_minute_interval(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", [
                "handler.py", "--symbol", "113042.SH", "--interval-unit", "minute",
                "--since-ts-millis", str(SINCE), "--until-ts-millis", str(UNTIL)
            ]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_since_after_until(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", [
                "handler.py", "--symbol", "113042.SH", "--interval-unit", "day",
                "--since-ts-millis", str(UNTIL), "--until-ts-millis", str(SINCE)
            ]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()