#!/usr/bin/env python3
"""Tests for kline-archives handler"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("handler", os.path.join(_dir, "handler.py"))
handler = importlib.util.module_from_spec(spec)

BODY = b"AAABBB"
SHA = hashlib.sha256(BODY).hexdigest()
ETAG = '"etag-1"'
FILENAME = "ftshare_1m_2023.tar.zst"
DOWNLOAD_URL = "/api/v2/market/data/kline-archives/2023/download"


class FakeHeaders(dict):
    def __init__(self, mapping=None):
        super().__init__((key.lower(), value) for key, value in (mapping or {}).items())

    def get(self, key, default=None):
        return super().get(key.lower(), default)


class FakeResponse:
    def __init__(self, code=200, headers=None, chunks=None, url=None):
        self._code = code
        self.headers = FakeHeaders(headers)
        self._chunks = list(chunks or [])
        self._url = url

    def getcode(self):
        return self._code

    def read(self, size=-1):
        return self._chunks.pop(0) if self._chunks else b""

    def geturl(self):
        return self._url or (handler.BASE_URL + DOWNLOAD_URL)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False


def listing_response(year=2023, size=len(BODY), sha256=SHA):
    payload = {
        "code": 200,
        "message": "success",
        "data": [{"year": year, "size_bytes": size, "last_modified": "2026-09-18T12:25:24.434+00:00", "sha256": sha256}],
    }
    return FakeResponse(chunks=[json.dumps(payload).encode()])


def header_of(request, name):
    for key, value in request.headers.items():
        if key.lower() == name.lower():
            return value
    return None


class KlineArchivesTestCase(unittest.TestCase):
    def setUp(self):
        # 模块级 _REQUEST_HEADERS 在 import 时按环境变量定型，故先注入再 exec
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            spec.loader.exec_module(handler)
        self._cwd = os.getcwd()
        self._tmp = tempfile.TemporaryDirectory()
        os.chdir(self._tmp.name)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def run_handler(self, argv):
        with patch.dict(os.environ, {"FTSHARE_API_KEY": "test-key"}):
            with patch.object(sys, "argv", ["handler.py"] + argv):
                handler.main()

    def part_path(self):
        return os.path.join(os.getcwd(), FILENAME + ".part")

    def meta_path(self):
        return self.part_path() + ".meta"

    def seed_partial(self, body=b"AAA", etag=ETAG, url=None):
        with open(self.part_path(), "wb") as handle:
            handle.write(body)
        with open(self.meta_path(), "w", encoding="utf-8") as handle:
            json.dump({"url": url or (handler.BASE_URL + DOWNLOAD_URL), "etag": etag, "size": len(body)}, handle)

    def target_path(self):
        return os.path.join(os.getcwd(), FILENAME)


class TestListingMode(KlineArchivesTestCase):
    @patch.object(handler, "safe_urlopen")
    def test_listing_prints_payload(self, mock_open):
        mock_open.return_value.__enter__.return_value = listing_response()
        self.run_handler([])
        request = mock_open.call_args[0][0]
        self.assertTrue(request.full_url.endswith("/api/v2/market/data/kline-archives"))
        self.assertEqual(header_of(request, "FTSHARE_API_KEY"), "test-key")

    @patch.object(handler, "safe_urlopen")
    def test_year_absent_from_listing_is_rejected(self, mock_open):
        mock_open.return_value.__enter__.return_value = listing_response(year=2024)
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "2023"])
        # 只发生了清单请求，没有下载请求，也没有落盘
        self.assertEqual(mock_open.call_count, 1)
        self.assertEqual(os.listdir(os.getcwd()), [])

    def test_invalid_year_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "abcd"])

    @patch.object(handler, "safe_urlopen")
    def test_output_outside_cwd_is_rejected(self, mock_open):
        mock_open.return_value.__enter__.return_value = listing_response()
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "2023", "--output", os.path.join("..", "escape.zst")])


class TestDownloadMode(KlineArchivesTestCase):
    @patch.object(handler, "safe_urlopen")
    def test_fresh_download_writes_verifies_and_cleans_up(self, mock_open):
        mock_open.side_effect = [listing_response(), FakeResponse(chunks=[b"AAA", b"BBB"])]
        self.run_handler(["--year", "2023"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), BODY)
        self.assertEqual(sorted(os.listdir(os.getcwd())), [FILENAME])
        download_request = mock_open.call_args_list[1][0][0]
        self.assertTrue(download_request.full_url.endswith(DOWNLOAD_URL))
        self.assertIsNone(header_of(download_request, "Range"))

    @patch.object(handler, "safe_urlopen")
    def test_resume_uses_range_and_if_range(self, mock_open):
        self.seed_partial()
        mock_open.side_effect = [
            listing_response(),
            FakeResponse(code=206, headers={"Content-Range": "bytes 3-5/6", "ETag": ETAG}, chunks=[b"BBB"]),
        ]
        self.run_handler(["--year", "2023"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), BODY)
        self.assertEqual(sorted(os.listdir(os.getcwd())), [FILENAME])
        download_request = mock_open.call_args_list[1][0][0]
        self.assertEqual(header_of(download_request, "Range"), "bytes=3-")
        self.assertEqual(header_of(download_request, "If-Range"), ETAG)

    @patch.object(handler, "safe_urlopen")
    def test_stale_etag_200_truncates_instead_of_appending(self, mock_open):
        self.seed_partial(etag='"stale"')
        mock_open.side_effect = [
            listing_response(size=6, sha256=hashlib.sha256(b"CCCCCC").hexdigest()),
            FakeResponse(headers={"ETag": '"fresh"'}, chunks=[b"CCCCCC"]),
        ]
        self.run_handler(["--year", "2023"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), b"CCCCCC")
        download_request = mock_open.call_args_list[1][0][0]
        self.assertEqual(header_of(download_request, "If-Range"), '"stale"')

    @patch.object(handler, "safe_urlopen")
    def test_416_restarts_from_scratch(self, mock_open):
        self.seed_partial()
        mock_open.side_effect = [
            listing_response(),
            urllib.error.HTTPError(handler.BASE_URL + DOWNLOAD_URL, 416, "Range Not Satisfiable", {}, None),
            FakeResponse(chunks=[BODY]),
        ]
        self.run_handler(["--year", "2023"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), BODY)
        self.assertEqual(sorted(os.listdir(os.getcwd())), [FILENAME])
        retry_request = mock_open.call_args_list[2][0][0]
        self.assertIsNone(header_of(retry_request, "Range"))

    @patch.object(handler, "safe_urlopen")
    def test_untraceable_partial_file_is_discarded(self, mock_open):
        self.seed_partial(url=handler.BASE_URL + "/api/v2/market/data/other/download")
        mock_open.side_effect = [listing_response(), FakeResponse(chunks=[BODY])]
        self.run_handler(["--year", "2023"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), BODY)
        self.assertIsNone(header_of(mock_open.call_args_list[1][0][0], "Range"))

    @patch.object(handler, "safe_urlopen")
    def test_content_range_mismatch_restarts(self, mock_open):
        self.seed_partial()
        mock_open.side_effect = [
            listing_response(),
            FakeResponse(code=206, headers={"Content-Range": "bytes 1-5/6"}, chunks=[b"XXXXX"]),
            FakeResponse(chunks=[BODY]),
        ]
        self.run_handler(["--year", "2023"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), BODY)

    @patch.object(handler, "safe_urlopen")
    def test_retries_after_network_error(self, mock_open):
        mock_open.side_effect = [
            listing_response(),
            urllib.error.URLError("connection reset"),
            FakeResponse(chunks=[BODY]),
        ]
        self.run_handler(["--year", "2023", "--retries", "1"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), BODY)

    @patch.object(handler, "safe_urlopen")
    def test_retries_exhausted_exits_nonzero(self, mock_open):
        mock_open.side_effect = [
            listing_response(),
            urllib.error.URLError("first"),
            urllib.error.URLError("second"),
        ]
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "2023", "--retries", "1"])

    @patch.object(handler, "safe_urlopen")
    def test_non_retryable_http_error_exits_immediately(self, mock_open):
        mock_open.side_effect = [
            listing_response(),
            urllib.error.HTTPError(handler.BASE_URL + DOWNLOAD_URL, 404, "Not Found", {}, None),
        ]
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "2023", "--retries", "3"])
        self.assertEqual(mock_open.call_count, 2)

    @patch.object(handler, "safe_urlopen")
    def test_sha256_mismatch_exits_and_removes_partial(self, mock_open):
        mock_open.side_effect = [
            listing_response(sha256=hashlib.sha256(b"different").hexdigest()),
            FakeResponse(chunks=[BODY]),
        ]
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "2023"])
        self.assertEqual(os.listdir(os.getcwd()), [])

    @patch.object(handler, "safe_urlopen")
    def test_truncated_transfer_keeps_partial_and_resumes(self, mock_open):
        # 第一次连接被掐断只收到 3 字节，第二次从第 3 字节接着传
        mock_open.side_effect = [
            listing_response(),
            FakeResponse(headers={"ETag": ETAG}, chunks=[b"AAA"]),
            FakeResponse(code=206, headers={"Content-Range": "bytes 3-5/6", "ETag": ETAG}, chunks=[b"BBB"]),
        ]
        self.run_handler(["--year", "2023"])
        with open(self.target_path(), "rb") as handle:
            self.assertEqual(handle.read(), BODY)
        self.assertEqual(sorted(os.listdir(os.getcwd())), [FILENAME])
        resume_request = mock_open.call_args_list[2][0][0]
        self.assertEqual(header_of(resume_request, "Range"), "bytes=3-")

    @patch.object(handler, "safe_urlopen")
    def test_truncated_transfer_leaves_partial_for_next_run(self, mock_open):
        # 每次都被掐断且重试耗尽：半成品必须留着，供下次直接续传
        mock_open.side_effect = [
            listing_response(),
            FakeResponse(headers={"ETag": ETAG}, chunks=[b"AAA"]),
            FakeResponse(headers={"ETag": ETAG}, chunks=[b"AAA"]),
        ]
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "2023", "--retries", "1"])
        self.assertEqual(sorted(os.listdir(os.getcwd())), [FILENAME + ".part", FILENAME + ".part.meta"])
        with open(self.part_path(), "rb") as handle:
            self.assertEqual(handle.read(), b"AAA")
        self.assertFalse(os.path.exists(self.target_path()))

    @patch.object(handler, "safe_urlopen")
    def test_oversized_response_exits_and_removes_partial(self, mock_open):
        mock_open.side_effect = [listing_response(size=6), FakeResponse(chunks=[b"AAAAAAAA"])]
        with self.assertRaises(SystemExit):
            self.run_handler(["--year", "2023"])
        self.assertEqual(os.listdir(os.getcwd()), [])

    @patch.object(handler, "safe_urlopen")
    def test_existing_verified_target_skips_download(self, mock_open):
        with open(self.target_path(), "wb") as handle:
            handle.write(BODY)
        mock_open.side_effect = [listing_response()]
        self.run_handler(["--year", "2023"])
        self.assertEqual(mock_open.call_count, 1)

    @patch.object(handler, "safe_urlopen")
    def test_force_redownloads_existing_target(self, mock_open):
        with open(self.target_path(), "wb") as handle:
            handle.write(BODY)
        mock_open.side_effect = [listing_response(), FakeResponse(chunks=[BODY])]
        self.run_handler(["--year", "2023", "--force"])
        self.assertEqual(mock_open.call_count, 2)


if __name__ == "__main__":
    unittest.main()
