#!/usr/bin/env python3
"""招股书列表（GET /api/v2/market/data/announcements/stock-prospectuses）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v2/market/data/announcements/stock-prospectuses"

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 500

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base_parsed = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base_parsed.scheme or parsed.netloc != base_parsed.netloc:
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


def build_params(args):
    params = {"page": args.page, "page_size": args.page_size}
    if args.stock_code is not None:
        params["stock_code"] = args.stock_code
    if args.start_date is not None:
        params["start_date"] = args.start_date
    if args.end_date is not None:
        params["end_date"] = args.end_date
    return params


def fetch_page(params):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{BASE_URL}{ENDPOINT}?{query}",
        headers={**HEADERS, **_REQUEST_HEADERS},
        method="GET",
    )
    try:
        with safe_urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(
        description="招股书列表：按标的（--stock-code）或按单日披露日期（--start-date）查询"
    )
    parser.add_argument("--stock-code", dest="stock_code", default=None,
                        help="股票代码，支持裸代码/短后缀/长后缀，如 600000、600000.SH、600000.XSHG")
    parser.add_argument("--start-date", dest="start_date", default=None,
                        help="披露日期 YYYYMMDD（未提供 stock-code 时必填，仅支持单日）")
    parser.add_argument("--end-date", dest="end_date", default=None,
                        help="披露日期 YYYYMMDD；不填默认等于 start-date，传入时必须相等")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", dest="page_size", type=int, default=DEFAULT_PAGE_SIZE,
                        help=f"每页条数，默认 {DEFAULT_PAGE_SIZE}，最大 {MAX_PAGE_SIZE}")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    if args.stock_code is None and args.start_date is None:
        print("必须提供 --stock-code（按标的查）或 --start-date（按日期查）", file=sys.stderr)
        raise SystemExit(2)
    if args.page < 1:
        print("--page 须大于等于 1", file=sys.stderr)
        raise SystemExit(2)
    if not 1 <= args.page_size <= MAX_PAGE_SIZE:
        print(f"--page-size 须在 1～{MAX_PAGE_SIZE} 之间", file=sys.stderr)
        raise SystemExit(2)
    if args.stock_code is None and args.end_date is not None and args.end_date != args.start_date:
        print("按日期查询仅支持单日：--end-date 必须等于 --start-date", file=sys.stderr)
        raise SystemExit(2)

    params = build_params(args)
    if args.fetch_all:
        first = fetch_page(params)
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