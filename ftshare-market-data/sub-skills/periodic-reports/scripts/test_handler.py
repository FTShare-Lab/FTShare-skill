#!/usr/bin/env python3
"""Tests for periodic-reports handler"""
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

URL_HASH = "378016094c7e1577795838e837c289b1d859508e5b86afc6d7010168d8090432"
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
        _run(["--stock-code", "000637.SZ", "--report-type", "annual",
              "--report-year", "2025", "--document-variant", "full",
              "--page", "1", "--page-size", "5"])
        request = mock_open.call_args[0][0]
        self.assertTrue(request.full_url.startswith(handler.BASE_URL + "/api/v2/market/data/announcements/periodic-reports?"))
        query = urllib.parse.parse_qs(request.full_url.split("?", 1)[1])
        self.assertEqual(query["stock_code"], ["000637.SZ"])
        self.assertEqual(query["report_type"], ["annual"])
        self.assertEqual(query["report_year"], ["2025"])
        self.assertEqual(query["document_variant"], ["full"])
        self.assertEqual(query["page"], ["1"])
        self.assertEqual(query["page_size"], ["5"])

    def test_invalid_report_type_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--report-type", "monthly"])

    def test_report_year_out_of_range_rejected(self):
        with self.assertRaises(SystemExit):
            _run(["--report-year", "70000"])

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_pages(self, mock_open):
        mock_open.side_effect = [
            _response(b'{"code":200,"data":{"pages":2,"total":3,"records":[{"url_hash":"a"}]}}'),
            _response(b'{"code":200,"data":{"pages":2,"total":3,"records":[{"url_hash":"b"},{"url_hash":"c"}]}}'),
        ]
        payload = json.loads(_run_capture(["--all"]))
        self.assertEqual(payload["pages"], 2)
        self.assertEqual(payload["total"], 3)
        self.assertEqual([record["url_hash"] for record in payload["records"]], ["a", "b", "c"])
        self.assertIn("page=2", mock_open.call_args_list[1][0][0].full_url)


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
        self.assertEqual(
            mock_open.call_args[0][0].full_url,
            handler.BASE_URL + "/api/v2/market/data/announcements/periodic-reports/" + URL_HASH,
        )

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


if __name__ == "__main__":
    unittest.main()
