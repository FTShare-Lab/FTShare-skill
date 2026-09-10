#!/usr/bin/env python3
"""Tests for futures-contract-kline handler"""
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


class TestParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_end_without_start(self):
        with self.assertRaises(SystemExit):
            _run(["--symbol", "A2605.DCE", "--end", "1756791000000"])

    @patch.object(handler, "safe_urlopen")
    def test_defaults(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--symbol", "A2605.DCE"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/futures/kline", req.full_url)
        self.assertIn("symbol=A2605.DCE", req.full_url)
        self.assertIn("interval=daily", req.full_url)
        self.assertNotIn("limit", req.full_url)
        self.assertNotIn("start", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_weekly_interval(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--symbol", "A2605.DCE", "--interval", "weekly", "--limit", "5",
              "--start", "1756431000000", "--end", "1756791000000"])
        req = mock_open.call_args[0][0]
        self.assertIn("interval=weekly", req.full_url)
        self.assertIn("limit=5", req.full_url)
        self.assertIn("start=1756431000000", req.full_url)
        self.assertIn("end=1756791000000", req.full_url)

    def test_rejects_unknown_interval(self):
        with self.assertRaises(SystemExit):
            _run(["--symbol", "A2605.DCE", "--interval", "minute"])


if __name__ == "__main__":
    unittest.main()
