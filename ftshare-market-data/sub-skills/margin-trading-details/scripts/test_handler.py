#!/usr/bin/env python3
"""Tests for margin-trading-details handler"""
import json
import os
import sys
import unittest
import urllib.error
from io import BytesIO, StringIO
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("handler", os.path.join(os.path.dirname(os.path.abspath(__file__)), "handler.py"))
handler = importlib.util.module_from_spec(spec)

ENVELOPE = b'{"code":200,"message":"success","data":{"pageNum":1,"pageSize":2,"total":16,"pages":8,"records":[{"symbol":"600000.SH"}]}}'


class TestBuildParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_default_params(self):
        params = handler.build_params(1, 20, None, None, None, None)
        self.assertEqual(params, {"page": 1, "page_size": 20})

    def test_date_query(self):
        params = handler.build_params(1, 20, "20260623", None, None, None)
        self.assertEqual(params["date"], "20260623")

    def test_date_with_stock(self):
        params = handler.build_params(1, 20, "20260623", None, None, "600000.SH")
        self.assertEqual(params["date"], "20260623")
        self.assertEqual(params["stock"], "600000.SH")

    def test_range_query(self):
        params = handler.build_params(1, 20, None, "20260601", "20260623", "600000.SH")
        self.assertEqual(params["start_date"], "20260601")
        self.assertEqual(params["end_date"], "20260623")
        self.assertEqual(params["stock"], "600000.SH")
        self.assertNotIn("date", params)

    def test_rejects_date_with_range(self):
        with self.assertRaises(SystemExit):
            handler.build_params(1, 20, "20260623", "20260601", "20260623", "600000.SH")

    def test_rejects_incomplete_range(self):
        with self.assertRaises(SystemExit):
            handler.build_params(1, 20, None, "20260601", None, None)
        with self.assertRaises(SystemExit):
            handler.build_params(1, 20, None, "20260601", "20260623", None)

    def test_rejects_start_after_end(self):
        with self.assertRaises(SystemExit):
            handler.build_params(1, 20, None, "20260623", "20260601", "600000.SH")

    def test_rejects_span_over_three_years(self):
        with self.assertRaises(SystemExit):
            handler.build_params(1, 20, None, "20200101", "20260623", "600000.SH")

    def test_allows_exactly_three_years(self):
        params = handler.build_params(1, 20, None, "20230623", "20260623", "600000.SH")
        self.assertEqual(params["start_date"], "20230623")

    def test_rejects_bad_date_format(self):
        with self.assertRaises(SystemExit):
            handler.build_params(1, 20, "2026-06-23", None, None, None)

    def test_rejects_page_size_out_of_range(self):
        with self.assertRaises(SystemExit):
            handler.build_params(1, 1001, None, None, None, None)


class TestFetchPage(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_url_contains_params(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = ENVELOPE
        handler.fetch_page({"page": 2, "page_size": 200, "date": "20260623"})
        called_url = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/margin-trading-details", called_url)
        self.assertIn("page=2", called_url)
        self.assertIn("page_size=200", called_url)
        self.assertIn("date=20260623", called_url)

    @patch.object(handler, "safe_urlopen")
    def test_returns_parsed_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = ENVELOPE
        result = handler.fetch_page({"page": 1, "page_size": 2})
        self.assertEqual(result["data"]["records"][0]["symbol"], "600000.SH")
        self.assertEqual(result["data"]["pages"], 8)

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "http://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch_page({"page": 1, "page_size": 20})


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_single_page(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = ENVELOPE
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--page", "1", "--page_size", "2"]):
                with patch("sys.stdout", new_callable=StringIO) as fake_out:
                    handler.main()
                    result = json.loads(fake_out.getvalue())
                    self.assertEqual(result["code"], 200)
                    self.assertEqual(result["data"]["total"], 16)

    @patch.object(handler, "safe_urlopen")
    def test_range_query_flags(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = ENVELOPE
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--start-date", "20260601",
                                            "--end-date", "20260623", "--stock", "600000.SH"]):
                handler.main()
        called_url = mock_open.call_args[0][0]
        self.assertIn("start_date=20260601", called_url)
        self.assertIn("end_date=20260623", called_url)
        self.assertIn("stock=600000.SH", called_url)

    @patch.object(handler, "safe_urlopen")
    def test_fetch_all_pagination(self, mock_open):
        page1 = b'{"data":{"records":[{"symbol":"A"},{"symbol":"B"}],"pages":2,"total":3}}'
        page2 = b'{"data":{"records":[{"symbol":"C"}],"pages":2,"total":3}}'
        mock_open.return_value.__enter__.return_value.read.side_effect = [page1, page2]

        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--page_size", "2", "--all"]):
                with patch("sys.stdout", new_callable=StringIO) as fake_out:
                    handler.main()
                    result = json.loads(fake_out.getvalue())
                    self.assertEqual(len(result["records"]), 3)
                    self.assertEqual(result["pages"], 2)
                    self.assertEqual(result["total"], 3)

    def test_main_rejects_incomplete_range(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--start-date", "20260601"]):
                with self.assertRaises(SystemExit):
                    handler.main()


class TestSafeUrlopen(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_non_https(self):
        with self.assertRaises(SystemExit):
            handler.safe_urlopen("http://market.ft.tech/api")

    def test_rejects_wrong_host(self):
        with self.assertRaises(SystemExit):
            handler.safe_urlopen("https://evil.com/api")


if __name__ == "__main__":
    unittest.main()
