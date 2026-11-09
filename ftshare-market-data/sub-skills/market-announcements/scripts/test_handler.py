#!/usr/bin/env python3
"""Tests for market-announcements handler"""
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.parse
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)

URL_HASH = "7d3176c830063b63dbee6e93d24c3d0b5d82714b15dd7523716023c846f8dfbc"
PDF = b"%PDF-1.4 fake body"


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with redirect_stdout(io.StringIO()):
                handler.main()


def _run_capture(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                handler.main()
            return buffer.getvalue()


def _response(body, url=None):
    response = MagicMock()
    if isinstance(body, list):
        response.read.side_effect = body
    else:
        response.read.side_effect = [body, b""]
    response.geturl.return_value = url or (handler.BASE_URL + handler.DOWNLOAD_ENDPOINT.format(url_hash=URL_HASH))
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class TestListMode(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_filters_build_query(self, mock_open):
        mock_open.return_value = _response(b'{"code":200,"data":{"records":[]}}')
        _run(["--keyword", "回购", "--category", "annual,semi_annual",
              "--start-date", "20261001", "--end-date", "20261031",
              "--plate", "sh,bj", "--column-type", "stock",
              "--page", "2", "--page-size", "50"])
        request = mock_open.call_args[0][0]
        self.assertTrue(request.full_url.startswith(handler.BASE_URL + "/api/v2/market/data/announcements/market-announcements?"))
        query = urllib.parse.parse_qs(request.full_url.split("?", 1)[1])
        self.assertEqual(query["keyword"], ["回购"])
        self.assertEqual(query["category"], ["annual,semi_annual"])
        self.assertEqual(query["start_date"], ["20261001"])
        self.assertEqual(query["end_date"], ["20261031"])
        self.assertEqual(query["plate"], ["sh,bj"])
        self.assertEqual(query["column_type"], ["stock"])
        self.assertEqual(query["page"], ["2"])
        self.assertEqual(query["page_size"], ["50"])

    def test_end_date_without_start_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--end-date", "20261031"])

    def test_page_size_upper_bound(self):
        with self.assertRaises(SystemExit):
            _run(["--page-size", "501"])

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_pages(self, mock_open):
        mock_open.side_effect = [
            _response(b'{"code":200,"data":{"pages":2,"total":3,"records":[{"url_hash":"a"}]}}'),
            _response(b'{"code":200,"data":{"pages":2,"total":3,"records":[{"url_hash":"b"},{"url_hash":"c"}]}}'),
        ]
        printed = _run_capture(["--all"])
        payload = json.loads(printed)
        self.assertEqual(payload["pages"], 2)
        self.assertEqual(payload["total"], 3)
        self.assertEqual([record["url_hash"] for record in payload["records"]], ["a", "b", "c"])
        second_url = mock_open.call_args_list[1][0][0].full_url
        self.assertIn("page=2", second_url)


class TestDownloadMode(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            spec.loader.exec_module(handler)
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def target_path(self):
        return os.path.join(os.getcwd(), URL_HASH + ".pdf")

    @patch.object(handler, "safe_urlopen")
    def test_download_writes_pdf_and_cleans_part(self, mock_open):
        mock_open.return_value = _response(PDF)
        printed = _run_capture(["--url-hash", URL_HASH])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), PDF)
        self.assertEqual(os.listdir(os.getcwd()), [URL_HASH + ".pdf"])
        self.assertEqual(printed.strip(), self.target_path())
        request = mock_open.call_args[0][0]
        self.assertEqual(
            request.full_url,
            handler.BASE_URL + "/api/v2/market/data/announcements/market-announcements/" + URL_HASH,
        )

    @patch.object(handler, "safe_urlopen")
    def test_custom_output_name(self, mock_open):
        mock_open.return_value = _response(PDF)
        _run(["--url-hash", URL_HASH, "--output", "ann.pdf"])
        self.assertEqual(os.listdir(os.getcwd()), ["ann.pdf"])

    def test_invalid_url_hash_is_rejected(self):
        for bad in ("../../etc/passwd", "a/b", URL_HASH.upper(), "abc"):
            with self.assertRaises(SystemExit):
                _run(["--url-hash", bad])

    @patch.object(handler, "safe_urlopen")
    def test_output_outside_cwd_is_rejected(self, mock_open):
        mock_open.return_value = _response(PDF)
        with self.assertRaises(SystemExit):
            _run(["--url-hash", URL_HASH, "--output", os.path.join("..", "escape.pdf")])
        self.assertEqual(os.listdir(os.getcwd()), [])

    @patch.object(handler, "safe_urlopen")
    def test_redirect_outside_base_url_aborts(self, mock_open):
        mock_open.return_value = _response(PDF, url="https://evil.example.com/file.pdf")
        with self.assertRaises(SystemExit):
            _run(["--url-hash", URL_HASH])
        self.assertEqual(os.listdir(os.getcwd()), [])


if __name__ == "__main__":
    unittest.main()
