#!/usr/bin/env python3
"""Tests for executive-holdings-changes handler"""
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


class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "fetch")
    def test_fetch_contract(self, mock_fetch):
        mock_fetch.return_value = {
            "code": 200,
            "message": "ok",
            "data": {"pages": 1, "records": []},
        }
        with patch.object(sys, "argv", [
            "handler.py",
            "--stock-code", "600848",
            "--change-direction", "增持",
            "--start-date", "20260101",
            "--end-date", "20260601",
            "--page", "2",
            "--page-size", "20",
        ]):
            handler.main()
        params = mock_fetch.call_args.args[0]
        self.assertEqual(params, {
            "stock_code": "600848",
            "change_direction": "增持",
            "start_date": "20260101",
            "end_date": "20260601",
            "page": 2,
            "page_size": 20,
        })


class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "fetch")
    def test_main_emits_json(self, mock_fetch):
        mock_fetch.return_value = {
            "code": 200,
            "message": "ok",
            "data": {"pages": 1, "records": []},
        }
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py", "--stock-code", "600848"]):
                with patch("sys.stdout", new_callable=StringIO) as fake_out:
                    handler.main()
                    self.assertEqual(json.loads(fake_out.getvalue())["code"], 200)


if __name__ == "__main__":
    unittest.main()
