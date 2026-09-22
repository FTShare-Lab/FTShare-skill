#!/usr/bin/env python3
"""Tests for etf-announcements handler"""
import json
import os
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch
import importlib.util

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)

URL_HASH = "d8d5454407980d1356b982991c6b8dbb624710f663cd7b5a400805c0cd574adf"
PDF = b"%PDF-1.4 fake body"


def _run(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with patch("sys.stdout", new_callable=StringIO) as out:
                handler.main()
                return json.loads(out.getvalue())


def _run_raw(argv):
    with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
        with patch.object(sys, "argv", ["handler.py"] + argv):
            with patch("sys.stdout", new_callable=StringIO) as out:
                handler.main()
                return out.getvalue()


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


class TestModes(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    def test_requires_code_or_date(self):
        with self.assertRaises(SystemExit):
            _run(["--page", "1", "--page-size", "5"])

    @patch.object(handler, "safe_urlopen")
    def test_by_symbol(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run(["--etf-code", "159915", "--page", "1", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("/api/v2/market/data/announcements/etf-announcements", req.full_url)
        self.assertIn("etf_code=159915", req.full_url)
        self.assertIn("page=1", req.full_url)
        self.assertIn("page_size=5", req.full_url)

    @patch.object(handler, "safe_urlopen")
    def test_by_single_date(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b'{"code":200,"data":{"records":[],"pages":1,"total":0}}'
        )
        _run(["--start-date", "20260831", "--page", "1", "--page-size", "5"])
        req = mock_open.call_args[0][0]
        self.assertIn("start_date=20260831", req.full_url)
        # end_date 不填时默认等于 start_date（服务端按区间校验，缺省会退化成到今天的跨度而报错）
        self.assertIn("end_date=20260831", req.full_url)


class TestFetchAll(unittest.TestCase):
    def setUp(self):
        spec.loader.exec_module(handler)

    @patch.object(handler, "safe_urlopen")
    def test_all_aggregates_pages(self, mock_open):
        page1 = {"code": 200, "data": {"records": [{"announcement_id": "1"}], "pages": 2, "total": 2}}
        page2 = {"code": 200, "data": {"records": [{"announcement_id": "2"}], "pages": 2, "total": 2}}
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            json.dumps(page1).encode(), json.dumps(page2).encode(),
        ]
        result = _run(["--etf-code", "159915", "--page", "1", "--page-size", "1", "--all"])
        self.assertEqual([r["announcement_id"] for r in result["records"]], ["1", "2"])
        self.assertEqual(result["total"], 2)
        second_req = mock_open.call_args_list[1][0][0]
        self.assertIn("page=2", second_req.full_url)


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
        printed = _run_raw(["--url-hash", URL_HASH]).strip()
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), PDF)
        self.assertEqual(os.listdir(os.getcwd()), [URL_HASH + ".pdf"])
        self.assertEqual(printed, self.target_path())
        request = mock_open.call_args[0][0]
        self.assertEqual(
            request.full_url,
            handler.BASE_URL + "/api/v2/market/data/announcements/etf-announcements/" + URL_HASH,
        )
        self.assertEqual(request.get_header("Ftshare_api_key"), "test-key")

    @patch.object(handler, "safe_urlopen")
    def test_custom_output_name(self, mock_open):
        mock_open.return_value.__enter__.return_value = FakeResponse(chunks=[PDF])
        _run_raw(["--url-hash", URL_HASH, "--output", "etf-report.pdf"])
        self.assertEqual(os.listdir(os.getcwd()), ["etf-report.pdf"])

    def test_invalid_url_hash_is_rejected(self):
        for bad in ("../../etc/passwd", "a/b", "a.b"):
            with self.assertRaises(SystemExit):
                _run_raw(["--url-hash", bad])

    @patch.object(handler, "safe_urlopen")
    def test_output_outside_cwd_is_rejected(self, mock_open):
        mock_open.return_value.__enter__.return_value = FakeResponse(chunks=[PDF])
        with self.assertRaises(SystemExit):
            _run_raw(["--url-hash", URL_HASH, "--output", os.path.join("..", "escape.pdf")])
        self.assertEqual(os.listdir(os.getcwd()), [])

    @patch.object(handler, "safe_urlopen")
    def test_redirect_outside_base_url_aborts(self, mock_open):
        mock_open.return_value.__enter__.return_value = FakeResponse(
            chunks=[PDF], url="https://evil.example.com/file.pdf"
        )
        with self.assertRaises(SystemExit):
            _run_raw(["--url-hash", URL_HASH])
        self.assertEqual(os.listdir(os.getcwd()), [])


if __name__ == "__main__":
    unittest.main()
