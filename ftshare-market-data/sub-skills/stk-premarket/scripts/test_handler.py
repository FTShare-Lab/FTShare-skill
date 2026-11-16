#!/usr/bin/env python3
"""Tests for stk-premarket handler"""
import importlib.util
import json
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with patch("sys.stdout", new_callable=StringIO) as out:
                handler.main()
                return json.loads(out.getvalue())


def _page(items, total_pages, total_items=None):
    return b'{"code":200,"message":"success","data":{"items":' + json.dumps(items).encode() + \
           b',"total_items":' + str(total_items if total_items is not None else len(items)).encode() + \
           b',"total_pages":' + str(total_pages).encode() + b"}}"


class TestValidation(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_unpaired_dates(self):
        for argv in (["--start-date", "20260101"], ["--end-date", "20260101"]):
            with self.assertRaises(SystemExit):
                _run(argv + ["--ts-code", "600036.SH"])

    def test_rejects_trade_date_with_range(self):
        with self.assertRaises(SystemExit):
            _run(["--ts-code", "600036.SH", "--trade-date", "20261113",
                  "--start-date", "20260101", "--end-date", "20261113"])

    def test_rejects_range_without_ts_code(self):
        with self.assertRaises(SystemExit):
            _run(["--start-date", "20260101", "--end-date", "20261113"])

    def test_rejects_page_size_out_of_range(self):
        for size in ("0", "501", "1000"):
            with self.assertRaises(SystemExit):
                _run(["--ts-code", "600036.SH", "--page-size", size])

    def test_rejects_page_zero(self):
        with self.assertRaises(SystemExit):
            _run(["--ts-code", "600036.SH", "--page", "0"])

    def test_help_does_not_require_api_key(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": ""}, clear=False):
            with patch.object(sys, "argv", ["handler.py", "--help"]):
                with patch("sys.stdout", new_callable=StringIO):
                    with self.assertRaises(SystemExit) as ctx:
                        handler.main()
        self.assertEqual(ctx.exception.code, 0)


class TestQuery(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_mapping(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = _page([], 1)
        _run(["--ts-code", "600036.SH", "--start-date", "20250101",
              "--end-date", "20261116", "--page", "2", "--page-size", "20"])
        url = mock_open.call_args[0][0].full_url
        self.assertIn("/api/v2/market/data/stk-premarket", url)
        self.assertIn("ts_code=600036.SH", url)
        self.assertIn("start_date=20250101", url)
        self.assertIn("end_date=20261116", url)
        self.assertIn("page=2", url)
        self.assertIn("page_size=20", url)

    @patch.object(handler, "safe_urlopen")
    def test_pass_through_envelope(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = _page(
            [{"ts_code": "600036.SH", "trade_date": 20261116}], 1, 452)
        result = _run(["--ts-code", "600036.SH"])
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"]["total_items"], 452)


class TestFetchAll(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_items_across_pages(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            _page([{"trade_date": 20250102}], 2, 2),
            _page([{"trade_date": 20250103}], 2, 2),
        ]
        result = _run(["--ts-code", "600036.SH", "--start-date", "20250101",
                       "--end-date", "20250103", "--all"])
        self.assertEqual(len(result["data"]["items"]), 2)
        self.assertEqual(result["data"]["total_items"], 2)
        self.assertEqual(result["data"]["total_pages"], 2)
        # --all 默认 page_size=500，且从第 1 页开始
        first_url = mock_open.call_args_list[0][0][0].full_url
        self.assertIn("page=1", first_url)
        self.assertIn("page_size=500", first_url)

    @patch.object(handler, "safe_urlopen")
    def test_all_stops_at_last_page(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = _page(
            [{"trade_date": 20261116}], 1, 1)
        _run(["--trade-date", "20261116", "--all"])
        self.assertEqual(mock_open.call_count, 1)


if __name__ == "__main__":
    unittest.main()
