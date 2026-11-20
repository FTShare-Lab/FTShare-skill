#!/usr/bin/env python3
"""申万指数日行情（GET /api/v1/market/data/sw-index/daily-quotes）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v1/market/data/sw-index/daily-quotes"

MAX_PAGE_SIZE = 200

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
    for key, value in _REQUEST_HEADERS.items():
        req_or_url.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(req_or_url)


def build_query(index_code, trade_date, start_date, end_date, index_type, page, page_size):
    body = {}
    if index_code is not None:
        body["index_code"] = index_code
    if trade_date is not None:
        body["trade_date"] = trade_date
    if start_date is not None:
        body["start_date"] = start_date
    if end_date is not None:
        body["end_date"] = end_date
    if index_type:
        body["index_type"] = index_type
    if page is not None:
        body["page"] = page
    if page_size is not None:
        body["page_size"] = page_size
    return body


def fetch(params):
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


def fetch_all(base_params, page_size):
    """按 pages 逐页取，合并 records。"""
    payload = fetch({**base_params, "page": 1, "page_size": page_size})
    data = payload.get("data") or {}
    records = list(data.get("records") or [])
    pages = int(data.get("pages") or 0)
    for page in range(2, pages + 1):
        page_payload = fetch({**base_params, "page": page, "page_size": page_size})
        page_records = (page_payload.get("data") or {}).get("records") or []
        if not page_records:
            break
        records.extend(page_records)
    payload["data"] = {**data, "pageNum": 1, "pageSize": page_size, "records": records}
    return payload


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询申万指数日行情")
    parser.add_argument("--index-code", dest="index_code",
                        help="申万指数代码，如 801001；也可带 .SI 后缀")
    parser.add_argument("--trade-date", dest="trade_date",
                        help="单个交易日 YYYYMMDD（单日全市场截面）；与 --start-date/--end-date 互斥")
    parser.add_argument("--start-date", dest="start_date",
                        help="起始日期 YYYYMMDD（含当天）；需与 --end-date 同时提供")
    parser.add_argument("--end-date", dest="end_date",
                        help="截止日期 YYYYMMDD（含当天）；需与 --start-date 同时提供")
    parser.add_argument("--index-type", dest="index_type",
                        help="指数分类：一级行业/二级行业/三级行业/市场表征/风格指数/量化策略/新三板/大类风格")
    parser.add_argument("--page", type=int, default=None, help="页码，从 1 开始")
    parser.add_argument("--page-size", dest="page_size", type=int, default=None,
                        help="每页数量，默认 50，最大 200")
    parser.add_argument("--all", action="store_true", dest="fetch_all",
                        help="自动翻页取全部记录")
    args = parser.parse_args()

    single_day = args.trade_date is not None
    ranged = args.start_date is not None or args.end_date is not None
    if single_day and ranged:
        print("--trade-date 不能与 --start-date/--end-date 同时传入", file=sys.stderr)
        raise SystemExit(2)
    if not single_day:
        if args.start_date is None or args.end_date is None:
            print("不传 --trade-date 时必须同时提供 --start-date 与 --end-date", file=sys.stderr)
            raise SystemExit(2)
        if args.start_date > args.end_date:
            print("--start-date 不能晚于 --end-date", file=sys.stderr)
            raise SystemExit(2)
    if args.page is not None and args.page < 1:
        print("--page 须大于 0", file=sys.stderr)
        raise SystemExit(2)
    if args.page_size is not None and not 1 <= args.page_size <= MAX_PAGE_SIZE:
        print(f"--page-size 须在 1～{MAX_PAGE_SIZE} 之间", file=sys.stderr)
        raise SystemExit(2)

    params = build_query(args.index_code, args.trade_date, args.start_date, args.end_date,
                         args.index_type, args.page, args.page_size)
    if args.fetch_all:
        payload = fetch_all(
            {k: v for k, v in params.items() if k not in ("page", "page_size")},
            args.page_size or 50,
        )
    else:
        payload = fetch(params)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()