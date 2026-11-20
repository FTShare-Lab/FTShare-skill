#!/usr/bin/env python3
"""期货官方日K与9999主连（GET /api/v1/market/data/futures/daily-kline）"""
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
ENDPOINT = "/api/v1/market/data/futures/daily-kline"

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
    for key, value in _REQUEST_HEADERS.items():
        req_or_url.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(req_or_url)


def build_query(symbol, trade_date, start_date, end_date, rule_version, page, page_size):
    body = {"symbol": symbol}
    if trade_date is not None:
        body["trade_date"] = trade_date
    if start_date is not None:
        body["start_date"] = start_date
    if end_date is not None:
        body["end_date"] = end_date
    if rule_version is not None:
        body["rule_version"] = rule_version
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


def fetch_all(params):
    """按 page_size 逐页取，直到取满 total 或返回空页。"""
    page_size = params.get("page_size") or 50
    page = 1
    items = []
    payload = None
    while True:
        payload = fetch({**params, "page": page, "page_size": page_size})
        data = payload.get("data") or {}
        rows = data.get("items") or []
        items.extend(rows)
        total = data.get("total")
        if not rows or len(rows) < page_size:
            break
        if isinstance(total, int) and len(items) >= total:
            break
        page += 1
    payload = payload or {"data": {}}
    data = dict(payload.get("data") or {})
    data["items"] = items
    data["page"] = 1
    data["page_size"] = page_size
    payload["data"] = data
    return payload


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询期货真实合约或 9999 主连的官方日 K")
    parser.add_argument("--symbol", required=True,
                        help="期货合约或 9999 主连代码，如 A2405、A2405.DCE、A9999、A9999.DCE；CZCE 真实合约须用四位年份代码")
    parser.add_argument("--trade-date", dest="trade_date",
                        help="单个交易日 YYYYMMDD；与 --start-date/--end-date 二选一")
    parser.add_argument("--start-date", dest="start_date",
                        help="区间起始交易日 YYYYMMDD；必须与 --end-date 同时传入")
    parser.add_argument("--end-date", dest="end_date",
                        help="区间结束交易日 YYYYMMDD；必须与 --start-date 同时传入")
    parser.add_argument("--rule-version", dest="rule_version", default=None,
                        help="9999 主连映射规则版本，默认由服务端使用 v1")
    parser.add_argument("--page", type=int, default=None, help="页码，从 1 开始")
    parser.add_argument("--page-size", dest="page_size", type=int, default=None,
                        help="每页条数，默认 50，最大 500")
    parser.add_argument("--all", action="store_true", dest="fetch_all",
                        help="自动翻页取全部记录（按 page_size 逐页取）")
    args = parser.parse_args()

    single_day = args.trade_date is not None
    ranged = args.start_date is not None or args.end_date is not None
    if single_day and ranged:
        print("--trade-date 不能与 --start-date/--end-date 同时传入", file=sys.stderr)
        raise SystemExit(2)
    if not single_day and not ranged:
        print("必须提供 --trade-date，或同时提供 --start-date 与 --end-date", file=sys.stderr)
        raise SystemExit(2)
    if ranged and (args.start_date is None or args.end_date is None):
        print("--start-date 与 --end-date 必须成对传入", file=sys.stderr)
        raise SystemExit(2)
    if ranged and args.start_date > args.end_date:
        print("--start-date 不能晚于 --end-date", file=sys.stderr)
        raise SystemExit(2)
    if args.page is not None and args.page < 1:
        print("--page 须大于 0", file=sys.stderr)
        raise SystemExit(2)
    if args.page_size is not None and not 1 <= args.page_size <= MAX_PAGE_SIZE:
        print(f"--page-size 须在 1～{MAX_PAGE_SIZE} 之间", file=sys.stderr)
        raise SystemExit(2)

    params = build_query(args.symbol, args.trade_date, args.start_date, args.end_date,
                         args.rule_version, args.page, args.page_size)
    payload = fetch_all(params) if args.fetch_all else fetch(params)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()