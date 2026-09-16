#!/usr/bin/env python3
"""Tests for stock-quotes-list handler"""
import json
import sys
import unittest
import urllib.error
from http.client import IncompleteRead
from io import BytesIO, StringIO
from unittest.mock import patch

import importlib.util
import os

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


class TestBuildParams(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_page_no_mapped_to_page(self):
        p = handler.build_params(page_no=2, page_size=10)
        self.assertEqual(p["page"], 2)
        self.assertEqual(p["page_size"], 10)
        self.assertNotIn("page_no", p)  # 关键：daec 不认 page_no

    def test_no_page_when_page_no_none(self):
        self.assertNotIn("page", handler.build_params(order_by="change_rate desc"))

    def test_ob_to_order_by(self):
        self.assertEqual(handler.build_params(ob="change_rate desc"), {"order_by": "change_rate desc"})

    def test_order_by_preferred_over_ob(self):
        p = handler.build_params(order_by="close desc", ob="change_rate desc")
        self.assertEqual(p["order_by"], "close desc")

    def test_filter_masks_injected(self):
        p = handler.build_params(filter_="close != null", masks="name,close")
        self.assertEqual(p["filter"], "close != null")
        self.assertEqual(p["masks"], "name,close")

    def test_empty_filter_masks_omitted(self):
        p = handler.build_params(filter_="", masks="")
        self.assertNotIn("filter", p)
        self.assertNotIn("masks", p)


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_url_uses_daec_with_page_from_page_no(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"items":[]}'
        handler.fetch(order_by="change_rate desc", page_no=2, page_size=10)
        url = mock_open.call_args[0][0].full_url
        self.assertIn("daec/stocks", url)
        self.assertIn("page=2", url)
        self.assertNotIn("page_no", url)  # 关键
        self.assertIn("page_size=10", url)
        self.assertIn("order_by=change_rate", url)
        self.assertNotIn("/api/v2/", url)

    @patch.object(handler, "safe_urlopen")
    def test_items_ts_millis_converted(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"items":[{"symbol":"600000.XSHG","close":"9.32","ts_millis":1780300795000}],"page":1,"total_pages":1,"total_items":1}'
        )
        result = handler.fetch(order_by="change_rate desc", page_no=1, page_size=10)
        self.assertEqual(len(result["items"]), 1)
        self.assertIsInstance(result["items"][0]["ts_millis"], str)
        self.assertIn("T", result["items"][0]["ts_millis"])

    @patch.object(handler, "safe_urlopen")
    def test_http_error_exits(self, mock_open):
        mock_open.side_effect = urllib.error.HTTPError(
            "https://fake", 500, "Internal Error", {}, BytesIO(b"server error")
        )
        with self.assertRaises(SystemExit):
            handler.fetch(order_by="change_rate desc", page_no=1, page_size=10)

    @patch.object(handler, "safe_urlopen")
    def test_retries_on_incomplete_read(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            IncompleteRead(b"partial"),
            b'{"items":[],"page":1,"total_pages":1,"total_items":0}',
        ]
        handler.fetch(order_by="change_rate desc", page_no=1, page_size=10)
        self.assertEqual(mock_open.call_count, 2)


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)
        patch.object(handler.time, "sleep").start()
        self.addCleanup(patch.stopall)

    @patch.object(handler, "safe_urlopen")
    def test_main_basic(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"items":[],"page":1,"total_pages":1,"total_items":0}'
        with patch.object(sys, "argv", ["handler.py", "--order_by", "change_rate desc", "--page_no", "1", "--page_size", "10"]):
            with patch("sys.stdout", new_callable=StringIO) as fake_out:
                handler.main()
                result = json.loads(fake_out.getvalue())
                self.assertEqual(result["page"], 1)

    def test_main_missing_page_no_exits(self):
        with patch.object(sys, "argv", ["handler.py", "--order_by", "change_rate desc", "--page_size", "10"]):
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
