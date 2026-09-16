#!/usr/bin/env python3
"""Tests for index-candlesticks handler"""
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


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_get_to_index_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch("000300.XSHG", "Day", 1, "None", None, 1756791000000, 5)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v1/market/data/index-candlesticks", req.full_url)
        self.assertIsNone(req.data)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch("000300.XSHG", "Day", 1, "None", None, 1756791000000, None)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        with patch.object(sys, "argv", [
            "handler.py", "--symbol", "000300.XSHG", "--interval-unit", "Day",
            "--until-ts-millis", "1756791000000"
        ]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                self.assertEqual(json.loads(fake_out.getvalue()), [])


if __name__ == "__main__":
    unittest.main()
