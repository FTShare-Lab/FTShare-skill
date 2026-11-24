#!/usr/bin/env python3
"""Tests for sector-knowledge-sectors handler"""
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


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with patch("sys.stdout", new_callable=StringIO) as out:
                handler.main()
                return json.loads(out.getvalue())


class TestValidation(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_rejects_invalid_market(self):
        with self.assertRaises(SystemExit):
            _run(["--market", "EU"])

    def test_rejects_invalid_sector_type(self):
        with self.assertRaises(SystemExit):
            _run(["--sector-type", "theme"])


class TestRequests(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_returns_sector_list_without_pagination(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
            "code": 200,
            "data": [{"sector_name": "A股半导体", "sector_type": "industry", "market": "CN", "description": "..."}],
        }).encode()
        result = _run(["--market", "CN", "--name-keyword", "半导体"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v3/market/data/sector-knowledge/sectors", req.full_url)
        self.assertIn("market=CN", req.full_url)
        self.assertIn("name_keyword=%E5%8D%8A%E5%AF%BC%E4%BD%93", req.full_url)
        self.assertEqual(result["data"][0]["sector_name"], "A股半导体")

    @patch.object(handler, "safe_urlopen")
    def test_calls_route_without_query_when_no_filters(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'{"code":200,"data":[]}'
        _run([])
        req = mock_open.call_args[0][0]
        self.assertEqual(req.full_url, handler.BASE_URL + handler.ENDPOINT)


if __name__ == "__main__":
    unittest.main()