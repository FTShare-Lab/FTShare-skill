#!/usr/bin/env python3
"""Tests for sge-spot-description-all handler"""
import importlib.util
import io
import json
import os
import sys
import unittest
import urllib.parse
from contextlib import redirect_stdout
from unittest.mock import patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with redirect_stdout(io.StringIO()):
                handler.main()


class TestHandler(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_no_params_requests_full_list(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200,"data":[]}'
        _run([])
        request = mock_open.call_args[0][0]
        self.assertEqual(
            request.full_url,
            handler.BASE_URL + "/api/v1/market/data/sge-spot-description-all",
        )
        self.assertEqual(request.get_header("Ftshare_api_key"), "test-key")
        self.assertEqual(request.get_header("X-client-name"), "ft-claw")

    @patch.object(handler, "safe_urlopen")
    def test_category_and_active_only(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200,"data":[]}'
        _run(["--category", "spot_deferred", "--active-only"])
        query = urllib.parse.parse_qs(mock_open.call_args[0][0].full_url.split("?", 1)[1])
        self.assertEqual(query["category"], ["spot_deferred"])
        self.assertEqual(query["active_only"], ["true"])

    def test_invalid_category_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--category", "spot_other"])

    @patch.object(handler, "safe_urlopen")
    def test_prints_json_payload(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"message":"success","data":[]}'
        )
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py"]):
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    handler.main()
        self.assertEqual(json.loads(buffer.getvalue()), {"code": 200, "message": "success", "data": []})


if __name__ == "__main__":
    unittest.main()
