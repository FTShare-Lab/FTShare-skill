#!/usr/bin/env python3
"""Tests for fund-index-tracking-funds handler"""
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
        args.index_code = '000300'
        args.scope = None
        handler.fetch(args)
        url = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/fund/index-fund", url)
        self.assertIn("index_code=", url)

class TestMain(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, 'safe_urlopen')
    def test_main_emits_json(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b'[]'
        argv = ['handler.py']
        argv += ['--index_code', '000300']
        argv += ['--scope', 'etf']
        with patch.object(sys, 'argv', argv):
            with patch('sys.stdout', new_callable=StringIO) as fake_out:
                handler.main()
                self.assertEqual(json.loads(fake_out.getvalue()), [])

if __name__ == '__main__':
    unittest.main()
