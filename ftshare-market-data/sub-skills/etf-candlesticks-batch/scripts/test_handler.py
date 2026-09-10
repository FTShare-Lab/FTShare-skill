#!/usr/bin/env python3
"""Tests for etf-candlesticks-batch handler"""
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

SINCE = "1756431000000"
UNTIL = "1756791000000"


class TestBuildQuery(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_required_only(self):
        body = handler.build_query(["510300.SH"], "Day", "None", 1756431000000, 1756791000000, None)
        self.assertEqual(body["symbols"], ["510300.SH"])
        self.assertEqual(body["interval_unit"], "Day")
        self.assertEqual(body["since_ts_millis"], 1756431000000)
        self.assertEqual(body["until_ts_millis"], 1756791000000)
        self.assertNotIn("adjust_kind", body)
        self.assertNotIn("limit", body)
        self.assertNotIn("interval_value", body)

    def test_optional_fields(self):
        body = handler.build_query(["510300.SH", "159915.SZ"], "Week", "Forward",
                                   1756700000000, 1756791000000, 5)
        self.assertEqual(body["symbols"], ["510300.SH", "159915.SZ"])
        self.assertEqual(body["adjust_kind"], "Forward")
        self.assertEqual(body["limit"], 5)

    def test_minute_not_allowed(self):
        with self.assertRaises(SystemExit):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "510300.SH",
                                            "--interval-unit", "Minute",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                handler.main()


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_expands_symbols(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(["510300.SH", "159915.SZ"], "Day", "None", 1756431000000, 1756791000000, 2)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v2/market/data/etf-candlesticks/batch", req.full_url)
        query = req.full_url.split("?", 1)[1]
        self.assertIn("symbols=510300.SH", query)
        self.assertIn("symbols=159915.SZ", query)
        self.assertIn("interval_unit=Day", query)
        self.assertIn("since_ts_millis=1756431000000", query)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"message":"success","data":[["510300.SH",'
            b'[{"open":4.55,"close":4.601,"ts_millis":"1756450800000"}]]]}'
        )
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "510300.SH",
                                            "--interval-unit", "Day",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL, "--limit", "2"]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
                    data = json.loads(out.getvalue())
                    self.assertEqual(data["data"][0][0], "510300.SH")

    def test_main_requires_since(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "510300.SH",
                                            "--interval-unit", "Day",
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_since_after_until(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "510300.SH",
                                            "--interval-unit", "Day",
                                            "--since-ts-millis", UNTIL,
                                            "--until-ts-millis", SINCE]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_requires_symbols(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--interval-unit", "Day",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()
