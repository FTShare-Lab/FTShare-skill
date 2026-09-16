#!/usr/bin/env python3
"""语义搜索新闻（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
import os
SAFE_URLOPENER = urllib.request.build_opener()

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
BEIJING_TZ = timezone(timedelta(hours=8))


def _normalize_to_beijing_iso(value: str) -> str:
    """
    将输入时间规范为东八区 ISO 8601 字符串。
    - 无时区：按东八区解释
    - 有时区：统一转换到东八区
    """
    raw = value.strip()
    if not raw:
        return raw
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=BEIJING_TZ)
    else:
        dt = dt.astimezone(BEIJING_TZ)
    return dt.isoformat()

def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != urllib.parse.urlparse(BASE_URL).scheme or parsed.netloc != urllib.parse.urlparse(BASE_URL).netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(str(req_or_url), headers=_REQUEST_HEADERS, method="GET")
    if isinstance(req_or_url, urllib.request.Request):
        for key, value in _REQUEST_HEADERS.items():
            req_or_url.add_unredirected_header(key, value)
    else:
        req_or_url = urllib.request.Request(str(req_or_url), headers=_REQUEST_HEADERS, method="GET")
    return SAFE_URLOPENER.open(req_or_url)



def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="语义搜索新闻")
    parser.add_argument(
        "--query",
        required=True,
        help="搜索文字，如：人工智能",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="返回条数，默认 10",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="年份，仅支持当年，用于限定搜索范围；不传则由服务端决定",
    )
    parser.add_argument(
        "--start_time",
        default=None,
        help="开始时间（含），ISO 8601，如 2026-03-01T00:00:00+08:00",
    )
    parser.add_argument(
        "--end_time",
        default=None,
        help="结束时间（含），ISO 8601，如 2026-03-15T23:59:59+08:00",
    )
    args = parser.parse_args()

    params = {"query": args.query, "limit": args.limit}
    if args.year is not None:
        params["year"] = args.year
    try:
        if args.start_time:
            params["start_time"] = _normalize_to_beijing_iso(args.start_time)
        if args.end_time:
            params["end_time"] = _normalize_to_beijing_iso(args.end_time)
    except ValueError as e:
        print(f"时间格式错误：{e}", file=sys.stderr)
        sys.exit(1)

    url = BASE_URL + "/api/v3/market/data/semantic-search-news?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET", headers=_REQUEST_HEADERS)

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
