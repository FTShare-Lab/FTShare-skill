#!/usr/bin/env python3
"""Tests for sw-index-daily-quotes handler"""
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


def _payload(records, page=1, pages=1):
    return {
        "code": 200,
        "message": "success",
        "data": {
            "pageNum": page,
            "pageSize": 2,
            "total": len(records),
            "pages": pages,
            "records": records,
        },
    }


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_carries_filters(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(_payload([])).encode()
        params = handler.build_query("801001.SI", None, "20261101", "20261111", "市场表征", 1, 2)
        handler.fetch(params)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v1/market/data/sw-index/daily-quotes", req.full_url)
        query = urllib.parse.parse_qs(req.full_url.split("?", 1)[1])
        self.assertEqual(query["index_code"], ["801001.SI"])
        self.assertEqual(query["start_date"], ["20261101"])
        self.assertEqual(query["end_date"], ["20261111"])
        self.assertEqual(query["index_type"], ["市场表征"])
        self.assertNotIn("trade_date", query)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_fetch_all_follows_pages(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            json.dumps(_payload([{"index_code": "801001"}], page=1, pages=2)).encode(),
            json.dumps(_payload([{"index_code": "801010"}], page=2, pages=2)).encode(),
        ]
        result = handler.fetch_all({"index_code": "801001"}, 2)
        self.assertEqual([r["index_code"] for r in result["data"]["records"]], ["801001", "801010"])
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
    def test_main_range_query(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(_payload([])).encode()
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--index-code", "801001", "--start-date", "20261101", "--end-date", "20261111"],
            ):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
        self.assertEqual(json.loads(out.getvalue())["code"], 200)
        query = urllib.parse.parse_qs(mock_open.call_args[0][0].full_url.split("?", 1)[1])
        self.assertEqual(query["index_code"], ["801001"])

    def test_main_requires_range_without_trade_date(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--index-code", "801001"]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_mixed_date_modes(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--trade-date", "20261111", "--start-date", "20261101", "--end-date", "20261111"],
            ):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_page_size_above_200(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(
                sys,
                "argv",
                ["handler.py", "--trade-date", "20261111", "--page-size", "201"],
            ):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_requires_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(sys, "argv", ["handler.py", "--trade-date", "20261111"]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()