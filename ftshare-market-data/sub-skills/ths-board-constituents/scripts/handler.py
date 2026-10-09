#!/usr/bin/env python3
"""查询同花顺板块成分股，支持按名称/代码/类型与截至日期检索"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
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

ENDPOINT = "/api/v1/market/data/ths-board-constituents"


def build_params(args) -> dict:
    params = {
        "board_code": args.board_code,
        "board_name": args.board_name,
        "board_type": args.board_type,
        "date": args.date,
        "page": args.page,
        "page_size": args.page_size,
    }
    return {key: value for key, value in params.items() if value is not None}


def fetch_page(params: dict) -> dict:
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询同花顺板块成分股")
    parser.add_argument("--board-code", dest="board_code", default=None, help="板块代码，如 300082（概念）、881101（行业）、882001（地域）、A（csrc）")
    parser.add_argument("--board-name", dest="board_name", default=None, help="板块名称，如 军工；概念板块建议用名称")
    parser.add_argument("--board-type", dest="board_type", default=None, help="板块类型：industry / concept / region / csrc，用于同名消歧")
    parser.add_argument("--date", default=None, help="查询日期 YYYYMMDD；不传返回当前成分股")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", dest="page_size", type=int, default=100, help="每页数量，默认 100，最大 1000")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全部成分股")
    args = parser.parse_args()

    if args.board_code is None and args.board_name is None:
        print("必须提供 --board-code 或 --board-name 至少一个", file=sys.stderr)
        raise SystemExit(2)

    params = build_params(args)
    if args.fetch_all:
        first = fetch_page({**params, "page": 1})
        data = first.get("data") or {}
        records = list(data.get("records", []))
        total_pages = data.get("pages") or 1
        for page in range(2, total_pages + 1):
            page_data = fetch_page({**params, "page": page})
            records.extend((page_data.get("data") or {}).get("records", []))
        result = {
            "records": records,
            "pages": total_pages,
            "total": data.get("total", len(records)),
        }
    else:
        result = fetch_page(params)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
