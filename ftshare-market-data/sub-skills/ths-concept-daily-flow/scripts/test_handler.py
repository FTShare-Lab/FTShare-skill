#!/usr/bin/env python3
"""Tests for ths-concept-daily-flow handler (board_name parameter rename)"""
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


class TestBoardName(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_board_name_sent(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--start-date", "20260805", "--end-date", "20260805",
              "--board-name", "机器人概念", "--page", "1", "--page-size", "100"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/ths-concept-daily-flow", req.full_url)
        self.assertIn("board_name=%E6%9C%BA%E5%99%A8%E4%BA%BA%E6%A6%82%E5%BF%B5", req.full_url)
        self.assertNotIn("sector_name", req.full_url)
        self.assertNotIn("trade_date", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_all_params_optional(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run([])
        req = mock_open.call_args[0][0]
        self.assertTrue(req.full_url.endswith("/api/v1/market/data/ths-concept-daily-flow"))


if __name__ == "__main__":
    unittest.main()
