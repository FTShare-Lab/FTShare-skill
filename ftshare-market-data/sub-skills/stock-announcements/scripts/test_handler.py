#!/usr/bin/env python3
"""Tests for stock-announcements handler"""
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)

URL_HASH = "d8d5454407980d1356b982991c6b8dbb624710f663cd7b5a400805c0cd574adf"
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


class FakeResponse:
    def __init__(self, chunks=None, url=None):
        self._chunks = list(chunks or [])
        self._url = url

    def read(self, size=-1):
        return self._chunks.pop(0) if self._chunks else b""

    def geturl(self):
        return self._url or (handler.BASE_URL + handler.DOWNLOAD_ENDPOINT.format(url_hash=URL_HASH))

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False


class TestListMode(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_by_stock_code(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run(["--stock-code", "002142.XSHE", "--page", "1", "--page-size", "10"])
        request = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/announcements/stock-announcements", request.full_url)
        self.assertIn("stock_code=002142.XSHE", request.full_url)
        self.assertIn("type=stock", request.full_url)

    def test_requires_page_and_page_size(self):
        with self.assertRaises(SystemExit):
            _run(["--stock-code", "002142.XSHE"])

    def test_requires_code_or_date(self):
        with self.assertRaises(SystemExit):
            _run(["--page", "1", "--page-size", "10"])

    def test_non_stock_type_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--stock-code", "002142.XSHE", "--page", "1", "--page-size", "10", "--type", "etf"])


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
        mock_open.return_value.__enter__.return_value = FakeResponse(chunks=[PDF[:5], PDF[5:]])
        printed = _run_capture(["--url-hash", URL_HASH])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), PDF)
        self.assertEqual(os.listdir(os.getcwd()), [URL_HASH + ".pdf"])
        self.assertEqual(printed.strip(), self.target_path())
        request = mock_open.call_args[0][0]
        self.assertEqual(
            request.full_url,
            handler.BASE_URL + "/api/v2/market/data/announcements/stock-announcements/" + URL_HASH,
        )
        self.assertEqual(request.get_header("Ftshare_api_key"), "test-key")

    @patch.object(handler, "safe_urlopen")
    def test_custom_output_name(self, mock_open):
        mock_open.return_value.__enter__.return_value = FakeResponse(chunks=[PDF])
        _run(["--url-hash", URL_HASH, "--output", "report.pdf"])
        self.assertEqual(os.listdir(os.getcwd()), ["report.pdf"])

    def test_invalid_url_hash_is_rejected(self):
        for bad in ("../../etc/passwd", "a/b", "a.b"):
            with self.assertRaises(SystemExit):
                _run(["--url-hash", bad])

    @patch.object(handler, "safe_urlopen")
    def test_output_outside_cwd_is_rejected(self, mock_open):
        mock_open.return_value.__enter__.return_value = FakeResponse(chunks=[PDF])
        with self.assertRaises(SystemExit):
            _run(["--url-hash", URL_HASH, "--output", os.path.join("..", "escape.pdf")])
        self.assertEqual(os.listdir(os.getcwd()), [])

    @patch.object(handler, "safe_urlopen")
    def test_redirect_outside_base_url_aborts(self, mock_open):
        mock_open.return_value.__enter__.return_value = FakeResponse(
            chunks=[PDF], url="https://evil.example.com/file.pdf"
        )
        with self.assertRaises(SystemExit):
            _run(["--url-hash", URL_HASH])
        self.assertEqual(os.listdir(os.getcwd()), [])


if __name__ == "__main__":
    unittest.main()
