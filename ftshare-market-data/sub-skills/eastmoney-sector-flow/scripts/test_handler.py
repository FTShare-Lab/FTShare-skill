#!/usr/bin/env python3
"""Tests for eastmoney-sector-flow handler (board_* parameter rename)"""
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


class TestBoardParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_board_params_sent(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--board-code", "BK0488", "--board-type", "industry",
              "--board-level", "2", "--page", "1", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/eastmoney-sector-flow", req.full_url)
        self.assertIn("board_code=BK0488", req.full_url)
        self.assertIn("board_type=industry", req.full_url)
        self.assertIn("board_level=2", req.full_url)
        self.assertNotIn("sector_code", req.full_url)
        self.assertNotIn("sector_type", req.full_url)
        self.assertNotIn("sector_level", req.full_url)

    def test_rejects_unknown_board_type(self):
        with self.assertRaises(SystemExit):
            _run(["--board-type", "unknown"])

    @patch.object(handler, "safe_urlopen")
    def test_all_params_optional(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run([])
        req = mock_open.call_args[0][0]
        self.assertTrue(req.full_url.endswith("/api/v1/market/data/eastmoney-sector-flow"))


if __name__ == "__main__":
    unittest.main()
