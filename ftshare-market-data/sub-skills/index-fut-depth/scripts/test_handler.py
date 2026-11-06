#!/usr/bin/env python3
"""Tests for index-fut-depth handler"""
import importlib.util
import io
import json
import os
import sys
import unittest
import urllib.parse
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _response(body):
    response = MagicMock()
    response.read.side_effect = [body, b""]
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with redirect_stdout(io.StringIO()):
                handler.main()


class TestHandler(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_no_date_requests_latest(self, mock_open):
        mock_open.return_value = _response(b'{"code":200,"data":{}}')
        _run([])
        self.assertEqual(mock_open.call_args[0][0].full_url, handler.BASE_URL + "/api/v1/market/data/index-fut/depth")

    @patch.object(handler, "safe_urlopen")
    def test_trade_date_and_code_prefix(self, mock_open):
        mock_open.return_value = _response(b'{"code":200,"data":{}}')
        _run(["--trade-date", "20261030", "--code-prefix", "if"])
        query = urllib.parse.parse_qs(mock_open.call_args[0][0].full_url.split("?", 1)[1])
        self.assertEqual(query["trade_date"], ["20261030"])
        self.assertEqual(query["code_prefix"], ["IF"])

    @patch.object(handler, "safe_urlopen")
    def test_range_query(self, mock_open):
        mock_open.return_value = _response(b'{"code":200,"data":{}}')
        _run(["--start-date", "20261030", "--end-date", "20261103"])
        query = urllib.parse.parse_qs(mock_open.call_args[0][0].full_url.split("?", 1)[1])
        self.assertEqual(query["start_date"], ["20261030"])
        self.assertEqual(query["end_date"], ["20261103"])
        self.assertNotIn("trade_date", query)

    def test_trade_date_conflicts_with_range(self):
        with self.assertRaises(SystemExit):
            _run(["--trade-date", "20261030", "--start-date", "20261030", "--end-date", "20261103"])

    def test_start_without_end_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--start-date", "20261030"])

    def test_end_before_start_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--start-date", "20261103", "--end-date", "20261030"])

    def test_non_yyyymmdd_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--trade-date", "2026-10-30"])

    def test_invalid_code_prefix_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--code-prefix", "XX"])

    @patch.object(handler, "safe_urlopen")
    def test_prints_json_payload(self, mock_open):
        mock_open.return_value = _response(b'{"code":200,"data":{"count":0}}')
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py"]):
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    handler.main()
        self.assertEqual(json.loads(buffer.getvalue()), {"code": 200, "data": {"count": 0}})


if __name__ == "__main__":
    unittest.main()
