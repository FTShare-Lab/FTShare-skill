#!/usr/bin/env python3
"""Tests for index-candlesticks-batch handler"""
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
        body = handler.build_query(["000300.SH"], "Day", "None", 1756431000000, 1756791000000, None)
        self.assertEqual(body["symbols"], ["000300.SH"])
        self.assertEqual(body["interval_unit"], "Day")
        self.assertEqual(body["since_ts_millis"], 1756431000000)
        self.assertNotIn("adjust_kind", body)
        self.assertNotIn("limit", body)
        self.assertNotIn("interval_value", body)

    def test_minute_not_allowed(self):
        with self.assertRaises(SystemExit):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "000300.SH",
                                            "--interval-unit", "Minute",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                handler.main()


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_targets_index_route(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"message":"success","data":[["000300.SH",[]]]}'
        )
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "000300.SH,399001.SZ",
                                            "--interval-unit", "Day",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
                    data = json.loads(out.getvalue())
                    self.assertEqual(data["data"][0][0], "000300.SH")
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/index-candlesticks/batch", req.full_url)
        self.assertIn("since_ts_millis=1756431000000", req.full_url)

    def test_main_requires_since(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "000300.SH",
                                            "--interval-unit", "Day",
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_since_after_until(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "000300.SH",
                                            "--interval-unit", "Day",
                                            "--since-ts-millis", UNTIL,
                                            "--until-ts-millis", SINCE]):
                with self.assertRaises(SystemExit):
                    handler.main()

    @patch.object(handler, "safe_urlopen")
    def test_interval_unit_case_insensitive(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "000300.SH",
                                            "--interval-unit", "day",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                handler.main()
        req = mock_open.call_args[0][0]
        self.assertIn("interval_unit=Day", req.full_url)

    def test_main_rejects_empty_symbols(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", " , ",
                                            "--interval-unit", "Day",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()


if __name__ == "__main__":
    unittest.main()
