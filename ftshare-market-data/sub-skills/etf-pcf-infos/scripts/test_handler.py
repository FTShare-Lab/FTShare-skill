#!/usr/bin/env python3
"""Tests for etf-pcf-infos handler"""
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


class TestModes(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_trade_date_with_range(self):
        with self.assertRaises(SystemExit):
            _run(["--symbol", "510300.SH", "--trade-date", "20260909",
                  "--start-date", "20260901", "--end-date", "20260909"])

    @patch.object(handler, "safe_urlopen")
    def test_single_symbol_single_day(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--symbol", "510300.SH", "--trade-date", "20260909"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/etf-pcf/etf-pcf-infos", req.full_url)
        self.assertIn("symbol=510300.SH", req.full_url)
        self.assertIn("trade_date=20260909", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_omits_unset_optionals(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--trade-date", "20260909"])
        req = mock_open.call_args[0][0]
        self.assertNotIn("symbol", req.full_url)
        self.assertNotIn("page", req.full_url)
        self.assertNotIn("page_size", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_range_mode_keeps_paging(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--symbol", "510300.SH", "--start-date", "20260901",
              "--end-date", "20260909", "--page", "2", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("start_date=20260901", req.full_url)
        self.assertIn("page=2", req.full_url)
        self.assertIn("page_size=5", req.full_url)


if __name__ == "__main__":
    unittest.main()
