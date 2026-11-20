#!/usr/bin/env python3
"""Tests for futures-daily-kline handler"""
import importlib.util
import json
import os
import sys
import unittest
import urllib.parse
from io import StringIO
from unittest.mock import patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _payload(items, total=None, page=1, page_size=2):
    return {
        "code": 200,
        "message": "success",
        "data": {
            "items": items,
            "total": len(items) if total is None else total,
            "page": page,
            "page_size": page_size,
        },
    }


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_carries_range_and_paging(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(_payload([])).encode()
        handler.fetch(handler.build_query("A9999.DCE", None, "20261101", "20261117", "v1", 1, 5))
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v1/market/data/futures/daily-kline", req.full_url)
        query = urllib.parse.parse_qs(req.full_url.split("?", 1)[1])
        self.assertEqual(query["symbol"], ["A9999.DCE"])
        self.assertEqual(query["start_date"], ["20261101"])
        self.assertEqual(query["end_date"], ["20261117"])
        self.assertEqual(query["rule_version"], ["v1"])
        self.assertEqual(query["page"], ["1"])
        self.assertEqual(query["page_size"], ["5"])
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_fetch_all_follows_pages_until_total(self, mock_open):
        pages = [
            _payload([{"symbol": "A9999", "trade_date": 20261116}, {"symbol": "A9999", "trade_date": 20261117}], total=3),
            _payload([{"symbol": "A9999", "trade_date": 20261118}], total=3),
        ]
        mock_open.return_value.__enter__.return_value.read.side_effect = [json.dumps(p).encode() for p in pages]
        result = handler.fetch_all({"symbol": "A9999.DCE", "page_size": 2})
        self.assertEqual([row["trade_date"] for row in result["data"]["items"]], [20261116, 20261117, 20261118])
        self.assertEqual(mock_open.call_count, 2)

    def test_rejects_cross_origin_url(self):
        opened = False

        def fail_open(*args, **kwargs):
            nonlocal opened
            opened = True
            raise AssertionError("cross-origin request reached opener")

        with patch.object(handler.SAFE_URLOPENER, "open", fail_open):
            with self.assertRaises(SystemExit):
                handler.safe_urlopen("https://example.invalid/api/v1/market/data/example")
        self.assertFalse(opened)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_single_day(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(_payload([])).encode()
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "AP2612.CZCE", "--trade-date", "20261117"]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
        self.assertEqual(json.loads(out.getvalue())["code"], 200)
        query = urllib.parse.parse_qs(mock_open.call_args[0][0].full_url.split("?", 1)[1])
        self.assertEqual(query["trade_date"], ["20261117"])

    def test_main_requires_date_mode(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "A9999.DCE"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_mixed_date_modes(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--symbol", "A9999.DCE", "--trade-date", "20261117",
                 "--start-date", "20261101", "--end-date", "20261117"],
            ):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_requires_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(sys, "argv", ["handler.py", "--symbol", "A9999.DCE", "--trade-date", "20261117"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_page_size_above_500(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--symbol", "A9999.DCE", "--trade-date", "20261117", "--page-size", "501"],
            ):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()