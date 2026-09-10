#!/usr/bin/env python3
"""获取 A 股融资融券明细，支持单日/区间查询、分页与全量拉取"""
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

ENDPOINT = "/api/v1/market/data/margin-trading-details"


def _check_date(value, flag):
    if len(value) != 8 or not value.isdigit():
        print(f"{flag} 格式应为 YYYYMMDD：{value}", file=sys.stderr)
        raise SystemExit(2)
    return value


def build_params(page, page_size, date, start_date, end_date, stock):
    if page < 1:
        print("--page 必须大于等于 1", file=sys.stderr)
        raise SystemExit(2)
    if page_size < 1 or page_size > 1000:
        print("--page_size 允许范围 1~1000", file=sys.stderr)
        raise SystemExit(2)
    params = {"page": page, "page_size": page_size}
    if date:
        params["date"] = _check_date(date, "--date")
    if start_date or end_date:
        if date:
            print("--date 不能与 --start-date/--end-date 同时使用", file=sys.stderr)
            raise SystemExit(2)
        if not (start_date and end_date and stock):
            print("区间查询需要 --start-date、--end-date、--stock 同时提供", file=sys.stderr)
            raise SystemExit(2)
        _check_date(start_date, "--start-date")
        _check_date(end_date, "--end-date")
        if start_date >= end_date:
            print("--start-date 必须早于 --end-date", file=sys.stderr)
            raise SystemExit(2)
        end_ymd = (int(end_date[:4]), int(end_date[4:6]), int(end_date[6:8]))
        start_limit = (int(start_date[:4]) + 3, int(start_date[4:6]), int(start_date[6:8]))
        if end_ymd > start_limit:
            print("区间跨度不能超过 3 年", file=sys.stderr)
            raise SystemExit(2)
        params["start_date"] = start_date
        params["end_date"] = end_date
        params["stock"] = stock
    elif stock:
        params["stock"] = stock
    return params


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
    parser = argparse.ArgumentParser(description="获取 A 股融资融券明细")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始）")
    parser.add_argument("--page_size", type=int, default=20, help="每页记录数（最大 1000）")
    parser.add_argument("--date", type=str, default=None,
                        help="单日查询日期，格式 YYYYMMDD，必须为交易日；不传返回前一交易日快照")
    parser.add_argument("--start-date", dest="start_date", type=str, default=None,
                        help="区间查询开始日期 YYYYMMDD；须与 --end-date、--stock 同时提供")
    parser.add_argument("--end-date", dest="end_date", type=str, default=None,
                        help="区间查询结束日期 YYYYMMDD；须与 --start-date、--stock 同时提供，跨度不超过 3 年")
    parser.add_argument("--stock", type=str, default=None,
                        help="标的代码过滤，如 600000.SH；区间查询时必填")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    params = build_params(args.page, args.page_size, args.date,
                          args.start_date, args.end_date, args.stock)

    if args.fetch_all:
        first = fetch_page(params)
        data = first.get("data") or {}
        records = list(data.get("records", []))
        pages = data.get("pages", 1)
        for p in range(2, pages + 1):
            page_params = dict(params, page=p)
            page_data = fetch_page(page_params)
            records.extend((page_data.get("data") or {}).get("records", []))
        result = {"records": records, "pages": pages, "total": data.get("total", len(records))}
    else:
        result = fetch_page(params)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
