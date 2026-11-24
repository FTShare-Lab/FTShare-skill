#!/usr/bin/env python3
"""Tests for sector-knowledge-insights handler"""
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

    def test_requires_at_least_one_condition(self):
        with self.assertRaises(SystemExit):
            _run([])

    def test_min_confidence_requires_sector_name(self):
        with self.assertRaises(SystemExit):
            _run(["--min-confidence", "0.8"])

    def test_rejects_confidence_out_of_range(self):
        with self.assertRaises(SystemExit):
            _run(["--sector-name", "A股半导体", "--min-confidence", "1.5"])

    def test_rejects_page_size_over_max(self):
        with self.assertRaises(SystemExit):
            _run(["--sector-name", "A股半导体", "--page-size", "201"])


class TestRequests(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_forwards_confidence_and_sort(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run([
            "--sector-name", "A股半导体",
            "--insight-category", "产业景气研判",
            "--min-confidence", "0.8",
            "--sort", "confidence",
        ])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v3/market/data/sector-knowledge/insights", req.full_url)
        self.assertIn("insight_category=%E4%BA%A7%E4%B8%9A%E6%99%AF%E6%B0%94%E7%A0%94%E5%88%A4", req.full_url)
        self.assertIn("min_confidence=0.8", req.full_url)
        self.assertIn("sort=confidence", req.full_url)


class TestFetchAll(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_pages(self, mock_open):
        page1 = {"code": 200, "data": {"records": [{"title": "a"}], "pages": 2, "total": 2}}
        page2 = {"code": 200, "data": {"records": [{"title": "b"}], "pages": 2, "total": 2}}
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            json.dumps(page1).encode(), json.dumps(page2).encode(),
        ]
        result = _run(["--sector-name", "A股半导体", "--page-size", "1", "--all"])
        self.assertEqual([r["title"] for r in result["records"]], ["a", "b"])
        self.assertEqual(result["total"], 2)


if __name__ == "__main__":
    unittest.main()