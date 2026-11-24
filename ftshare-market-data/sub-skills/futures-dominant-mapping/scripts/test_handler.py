#!/usr/bin/env python3
"""Tests for futures-dominant-mapping handler"""
import json
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with patch("sys.stdout", new_callable=StringIO) as out:
                handler.main()
                return json.loads(out.getvalue())


class TestValidation(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_requires_trade_date(self):
        with self.assertRaises(SystemExit):
            _run([])

    def test_rejects_invalid_trade_date(self):
        with self.assertRaises(SystemExit):
            _run(["--trade-date", "2026-11-23"])

    def test_requires_api_key(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": ""}):
            with patch.object(sys, "argv", ["handler.py", "--trade-date", "20261123"]):
                with self.assertRaises(SystemExit):
                    handler.main()


class TestRequests(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_forwards_trade_date_without_rule_version(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
            "code": 200,
            "message": "success",
            "data": [{"trade_date": "20261123", "exchange": "CFFEX", "variety": "IF", "dominant_symbol": "IF2612", "rule_version": "v1"}],
        }).encode()
        result = _run(["--trade-date", "20261123"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/futures/dominant-mapping", req.full_url)
        self.assertIn("trade_date=20261123", req.full_url)
        self.assertNotIn("rule_version", req.full_url)
        self.assertEqual(result["data"][0]["dominant_symbol"], "IF2612")

    @patch.object(handler, "safe_urlopen")
    def test_forwards_rule_version_verbatim(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200,"message":"success","data":[]}'
        _run(["--trade-date", "20261123", "--rule-version", "v4"])
        req = mock_open.call_args[0][0]
        self.assertEqual(
            req.full_url,
            handler.BASE_URL + handler.ENDPOINT + "?trade_date=20261123&rule_version=v4",
        )


if __name__ == "__main__":
    unittest.main()