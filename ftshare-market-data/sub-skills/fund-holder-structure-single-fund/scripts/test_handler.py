#!/usr/bin/env python3
"""Tests for fund-holder-structure-single-fund handler"""
import json
import sys
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util
import os

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)

class TestFetch(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, 'safe_urlopen')
    def test_fetch_forwards_to_endpoint(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'[]'
        class Args: pass
        args = Args()
        args.fund_code = '000001'
        args.report_type = None
        args.start_date = None
        args.end_date = None
        handler.fetch(args)
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v1/market/data/fund/fund-holder-structure", url)
        self.assertIn("fund_code=", url)

class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, 'safe_urlopen')
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'[]'
        argv = ['handler.py']
        argv += ['--fund_code', '000001']
        argv += ['--report_type', '年度报告']
        with patch.object(sys, 'argv', argv):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                handler.main()
                self.assertEqual(json.loads(fake_out.getvalue()), [])

if __name__ == '__main__':
    unittest.main()
