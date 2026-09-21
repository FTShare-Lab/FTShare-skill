#!/usr/bin/env python3
"""年度分K归档包（清单 + 断点续传下载）

清单：GET /api/v2/market/data/kline-archives
下载：GET /api/v2/market/data/kline-archives/{year}/download
"""
import argparse
import hashlib
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
LIST_ENDPOINT = "/api/v2/market/data/kline-archives"
DOWNLOAD_ENDPOINT = "/api/v2/market/data/kline-archives/{year}/download"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
CHUNK_SIZE = 1 << 20


class _ResponseTooLarge(Exception):
    pass


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(req_or_url, timeout=None):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base_parsed = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base_parsed.scheme or parsed.netloc != base_parsed.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    key = _require_api_key()
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    for name, value in _REQUEST_HEADERS.items():
        req_or_url.add_unredirected_header(name, value)
    req_or_url.add_unredirected_header("FTSHARE_API_KEY", key)
    return SAFE_URLOPENER.open(req_or_url, timeout=timeout)


def _unlink(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


def _safe_output_path(output):
    root = os.path.realpath(os.getcwd())
    target = os.path.realpath(os.path.join(root, output))
    if target == root or not target.startswith(root + os.sep):
        print(f"输出路径必须位于当前工作目录内: {output}", file=sys.stderr)
        raise SystemExit(2)
    return target


def _validate_year(value):
    if re.fullmatch(r"\d{4}", str(value)) is None:
        print(f"year 必须是 4 位数字: {value}", file=sys.stderr)
        raise SystemExit(2)
    return str(value)


def _content_range_start(value):
    """从 `bytes 100-200/300` 里取出起始偏移；解析不出来返回 None。"""
    if not value:
        return None
    match = re.match(r"\s*bytes\s+(\d+)-", value)
    return int(match.group(1)) if match else None


def _read_meta(path):
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (FileNotFoundError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _write_meta(path, url, etag, size):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump({"url": url, "etag": etag, "size": size}, handle)
    os.replace(tmp, path)


def _file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK_SIZE)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def fetch_listing():
    request = urllib.request.Request(
        BASE_URL + LIST_ENDPOINT,
        headers={**_REQUEST_HEADERS, "X-Client-Name": "ft-claw"},
        method="GET",
    )
    try:
        with safe_urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode(errors='replace')}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


def download_archive(year, output, retries, timeout, force):
    listing = fetch_listing()
    rows = listing.get("data") if isinstance(listing, dict) else None
    entry = next(
        (row for row in rows or [] if isinstance(row, dict) and str(row.get("year")) == year),
        None,
    )
    if entry is None:
        print(f"清单中没有 {year} 年的归档包", file=sys.stderr)
        raise SystemExit(2)

    expected_size = entry.get("size_bytes")
    expected_sha256 = entry.get("sha256")
    url = BASE_URL + DOWNLOAD_ENDPOINT.format(year=year)
    target = _safe_output_path(output)
    part = target + ".part"
    meta = part + ".meta"

    if not force and os.path.exists(target):
        size_ok = expected_size is None or os.path.getsize(target) == expected_size
        if size_ok and (expected_sha256 is None or _file_sha256(target) == expected_sha256):
            print(target)
            return target

    last_error = None
    for _ in range(retries + 1):
        offset, etag = 0, ""
        if os.path.exists(part):
            sidecar = _read_meta(meta)
            if sidecar and sidecar.get("url") == url and sidecar.get("etag"):
                etag = str(sidecar["etag"])
                offset = os.path.getsize(part)
            else:
                # 来源不明的半成品绝不续传
                _unlink(part)
                _unlink(meta)

        request_headers = {**_REQUEST_HEADERS, "X-Client-Name": "ft-claw"}
        if offset > 0:
            request_headers["Range"] = f"bytes={offset}-"
            request_headers["If-Range"] = etag
        request = urllib.request.Request(url, headers=request_headers, method="GET")

        try:
            response = safe_urlopen(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            error.read()
            if error.code == 416:
                _unlink(part)
                _unlink(meta)
                last_error = error
                continue
            if error.code == 429 or error.code >= 500:
                last_error = error
                continue
            print(f"HTTP {error.code}", file=sys.stderr)
            raise SystemExit(1)
        except urllib.error.URLError as error:
            last_error = error
            continue

        try:
            if response.getcode() == 206:
                start = _content_range_start(response.headers.get("Content-Range"))
                if start != offset:
                    _unlink(part)
                    _unlink(meta)
                    last_error = RuntimeError(
                        f"续传起点 {start} 与本地半成品 {offset} 字节不一致"
                    )
                    continue
                mode = "ab"
            else:
                # 200 表示服务端没有按 Range 返回（新版本或忽略 Range），
                # 必须截断重写，append 会把新旧数据拼成坏包。
                offset, mode = 0, "wb"
            response_etag = response.headers.get("ETag")
            if response_etag:
                _write_meta(meta, url, response_etag, offset)
            with open(part, mode) as handle:
                while True:
                    block = response.read(CHUNK_SIZE)
                    if not block:
                        break
                    handle.write(block)
                    if expected_size is not None and handle.tell() > expected_size:
                        raise _ResponseTooLarge()
        except _ResponseTooLarge:
            _unlink(part)
            _unlink(meta)
            print("响应体超过清单声明的大小", file=sys.stderr)
            raise SystemExit(1)
        except (urllib.error.URLError, http.client.HTTPException, OSError) as error:
            # 截断、连接重置、读超时：留着 .part，下一次接着传
            last_error = error
            continue
        finally:
            response.close()

        size = os.path.getsize(part)
        if expected_size is not None and size > expected_size:
            _unlink(part)
            _unlink(meta)
            print(f"响应体超过清单声明的大小: 期望 {expected_size}，实际 {size}", file=sys.stderr)
            raise SystemExit(1)
        if expected_size is not None and size < expected_size:
            # 连接被中途掐断，半成品本身是好的：留着下次接着传，整包重下代价太大
            last_error = RuntimeError(f"传输中断，仅收到 {size}/{expected_size} 字节")
            continue
        if expected_sha256:
            digest = _file_sha256(part)
            if digest != expected_sha256:
                # 已知是坏前缀，删掉，避免下次接着下还是坏的
                _unlink(part)
                _unlink(meta)
                print(f"sha256 校验失败: 期望 {expected_sha256}，实际 {digest}", file=sys.stderr)
                raise SystemExit(1)

        os.replace(part, target)
        _unlink(meta)
        print(target)
        return target

    print(f"下载失败，已重试 {retries} 次: {last_error}", file=sys.stderr)
    raise SystemExit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(
        description="年度分K归档包：不带 --year 查看清单，带 --year 下载对应年份的 zstd 归档包"
    )
    parser.add_argument("--year", default=None, help="4 位年份，如 2023；须在清单内")
    parser.add_argument("--output", default=None,
                        help="下载落盘路径，默认 ftshare_1m_<year>.tar.zst，必须在当前工作目录内")
    parser.add_argument("--retries", type=int, default=3, help="首次失败后的额外重试次数，默认 3")
    parser.add_argument("--timeout", type=int, default=60, help="单次网络读超时秒数，默认 60")
    parser.add_argument("--force", action="store_true", help="目标已存在且校验通过时也重新下载")
    args = parser.parse_args()

    if args.year is None:
        print(json.dumps(fetch_listing(), ensure_ascii=False, indent=2))
        return

    year = _validate_year(args.year)
    download_archive(
        year,
        args.output or f"ftshare_1m_{year}.tar.zst",
        args.retries,
        args.timeout,
        args.force,
    )


if __name__ == "__main__":
    main()
