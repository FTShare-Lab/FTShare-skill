#!/usr/bin/env python3
"""Tests for convertible-bond-candlesticks-batch handler"""
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

SINCE = "1786291200000"
UNTIL = "1786377599999"


class TestBuildQuery(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_required_only(self):
        body = handler.build_query(["113042.SH"], "Day", None, "None", 1786291200000, 1786377599999, None)
        self.assertEqual(body["symbols"], ["113042.SH"])
        self.assertEqual(body["interval_unit"], "Day")
        self.assertEqual(body["since_ts_millis"], 1786291200000)
        self.assertEqual(body["until_ts_millis"], 1786377599999)
        self.assertNotIn("adjust_kind", body)
        self.assertNotIn("limit", body)
        self.assertNotIn("interval_value", body)

    def test_optional_fields(self):
        body = handler.build_query(["113042.SH", "123107.SZ"], "Week", 1, "Forward",
                                   1786291200000, 1786377599999, 2)
        self.assertEqual(body["symbols"], ["113042.SH", "123107.SZ"])
        self.assertEqual(body["adjust_kind"], "forward")
        self.assertEqual(body["interval_value"], 1)
        self.assertEqual(body["limit"], 2)

    def test_rejects_too_many_symbols(self):
        with self.assertRaises(SystemExit):
            handler.parse_symbols(",".join(f"11304{i}.SH" for i in range(21)))


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_query_string_expands_symbols(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"[]"
        handler.fetch(["113042.SH", "123107.SZ"], "Day", None, "None", 1786291200000, 1786377599999, 1)
        req = mock_open.call_args[0][0]
        self.assertEqual(req.get_method(), "GET")
        self.assertIn("/api/v2/market/data/convertible-bond-candlesticks/batch", req.full_url)
        query = req.full_url.split("?", 1)[1]
        self.assertIn("symbols=113042.SH", query)
        self.assertIn("symbols=123107.SZ", query)
        self.assertIn("interval_unit=Day", query)
        self.assertIn("since_ts_millis=1786291200000", query)
        self.assertEqual(req.headers.get("X-client-name"), "ft-claw")


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"message":"success","data":[["113042.SH",'
            b'[{"open":"117.1980","close":"116.8380","ts_millis":1786345200000}]]]}'
        )
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "113042.SH,123107.SZ",
                                            "--interval-unit", "Day",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL, "--limit", "1"]):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    handler.main()
                    data = json.loads(out.getvalue())
                    self.assertEqual(data["data"][0][0], "113042.SH")

    def test_main_rejects_minute_interval(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "113042.SH",
                                            "--interval-unit", "Minute",
                                            "--since-ts-millis", SINCE,
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_requires_since(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "113042.SH",
                                            "--interval-unit", "Day",
                                            "--until-ts-millis", UNTIL]):
                with self.assertRaises(SystemExit):
                    handler.main()

    def test_main_rejects_since_after_until(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--symbols", "113042.SH",
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