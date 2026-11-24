#!/usr/bin/env python3
"""Tests for sector-knowledge-facts handler"""
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

    def test_keyword_requires_sector_name(self):
        with self.assertRaises(SystemExit):
            _run(["--keyword", "存储"])

    def test_keyword_and_expression_are_exclusive(self):
        with self.assertRaises(SystemExit):
            _run(["--sector-name", "A股半导体", "--keyword", "存储", "--keyword-expression", "存储"])

    def test_rejects_page_size_over_max(self):
        with self.assertRaises(SystemExit):
            _run(["--sector-name", "A股半导体", "--page-size", "201"])

    def test_rejects_invalid_sort(self):
        with self.assertRaises(SystemExit):
            _run(["--sector-name", "A股半导体", "--sort", "newest"])


class TestRequests(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_forwards_filters_and_repeatable_category(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run([
            "--sector-name", "A股半导体",
            "--fact-category", "行业供需",
            "--fact-category", "公司事件",
            "--start-date", "20260101",
            "--end-date", "20261123",
            "--sort", "latest",
        ])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v3/market/data/sector-knowledge/facts", req.full_url)
        self.assertIn("sector_name=A%E8%82%A1%E5%8D%8A%E5%AF%BC%E4%BD%93", req.full_url)
        self.assertIn("fact_category=%E8%A1%8C%E4%B8%9A%E4%BE%9B%E9%9C%80", req.full_url)
        self.assertIn("fact_category=%E5%85%AC%E5%8F%B8%E4%BA%8B%E4%BB%B6", req.full_url)
        self.assertIn("start_date=20260101", req.full_url)
        self.assertIn("sort=latest", req.full_url)


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
        second_req = mock_open.call_args_list[1][0][0]
        self.assertIn("page=2", second_req.full_url)


if __name__ == "__main__":
    unittest.main()