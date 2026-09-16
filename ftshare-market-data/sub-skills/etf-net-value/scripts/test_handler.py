#!/usr/bin/env python3
"""Tests for etf-net-value handler"""
import os
import sys
import unittest
from unittest.mock import patch
import importlib.util

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            handler.main()


class TestDateModes(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_requires_nav_date_or_range(self):
        with self.assertRaises(SystemExit):
            _run(["--etf-code", "510300", "--page", "1", "--page-size", "5"])

    def test_rejects_nav_date_with_range(self):
        with self.assertRaises(SystemExit):
            _run(["--etf-code", "510300", "--nav-date", "20260909",
                  "--start-date", "20260901", "--end-date", "20260909"])

    def test_rejects_partial_range(self):
        with self.assertRaises(SystemExit):
            _run(["--etf-code", "510300", "--start-date", "20260901"])

    @patch.object(handler, "safe_urlopen")
    def test_accepts_nav_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--etf-code", "510300", "--nav-date", "20260909"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/etf-net-value", req.full_url)
        self.assertIn("etf_code=510300", req.full_url)
        self.assertIn("nav_date=20260909", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_accepts_range(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--etf-code", "510300", "--start-date", "20260901", "--end-date", "20260909"])
        req = mock_open.call_args[0][0]
        self.assertIn("start_date=20260901", req.full_url)
        self.assertIn("end_date=20260909", req.full_url)
        self.assertNotIn("nav_date", req.full_url)


if __name__ == "__main__":
    unittest.main()
