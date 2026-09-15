#!/usr/bin/env python3
"""Tests for news-reaction-snapshot handler."""
import importlib.util
import json
import os
import sys
import unittest
from unittest.mock import patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            handler.main()


class TestNewsReactionSnapshot(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_forwards_required_and_optional_params(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--symbol", "600519.SH", "--start-date", "20260818", "--end-date", "20260828",
              "--lookback-hours", "48", "--page", "2", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v3/market/data/news-reaction-snapshot", req.full_url)
        self.assertIn("symbol=600519.SH", req.full_url)
        self.assertIn("start_date=20260818", req.full_url)
        self.assertIn("end_date=20260828", req.full_url)
        self.assertIn("lookback_hours=48", req.full_url)
        self.assertIn("page=2", req.full_url)
        self.assertIn("page_size=5", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_lookback_hours_omitted_when_absent(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"{}"
        _run(["--symbol", "600519.SH", "--start-date", "20260818", "--end-date", "20260828"])
        req = mock_open.call_args[0][0]
        self.assertNotIn("lookback_hours", req.full_url)

    def test_rejects_invalid_lookback_hours(self):
        with self.assertRaises(SystemExit):
            _run(["--symbol", "600519.SH", "--start-date", "20260818", "--end-date", "20260828",
                  "--lookback-hours", "12"])

    def test_rejects_out_of_range_pagination(self):
        with self.assertRaises(SystemExit):
            _run(["--symbol", "600519.SH", "--start-date", "20260818", "--end-date", "20260828",
                  "--page-size", "201"])

    def test_fetch_all_aggregates_records(self):
        pages = {
            1: {"data": {"pages": 2, "records": [{"trade_date": "20260819"}]}},
            2: {"data": {"pages": 2, "records": [{"trade_date": "20260820"}]}},
        }
        captured = []

        def fake_fetch(params):
            captured.append(params["page"])
            return pages[params["page"]]

        with patch.object(handler, "fetch", side_effect=fake_fetch):
            with patch("builtins.print") as mock_print:
                _run(["--symbol", "600519.SH", "--start-date", "20260818", "--end-date", "20260828", "--all"])
        self.assertEqual(captured, [1, 2])
        output = json.loads(mock_print.call_args[0][0])
        self.assertEqual([row["trade_date"] for row in output["data"]["records"]], ["20260819", "20260820"])


if __name__ == "__main__":
    unittest.main()
