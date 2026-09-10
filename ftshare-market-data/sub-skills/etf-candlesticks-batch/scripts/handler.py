#!/usr/bin/env python3
"""批量查询多只 ETF K 线（GET /api/v2/market/data/etf-candlesticks/batch）"""
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
ENDPOINT = "/api/v2/market/data/etf-candlesticks/batch"

INTERVAL_UNITS = ("Day", "Week", "Month", "Year")
ADJUST_KINDS = ("None", "Forward", "Backward")

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


def parse_symbols(raw):
    syms = [s.strip() for s in raw.split(",") if s.strip()]
    if not syms:
        print("--symbols 不能为空", file=sys.stderr)
        sys.exit(1)
    return syms


def build_query(symbols, interval_unit, adjust_kind, since_ts_millis, until_ts_millis, limit):
    body = {
        "symbols": symbols,
        "interval_unit": interval_unit,
        "until_ts_millis": until_ts_millis,
    }
    if adjust_kind and adjust_kind != "None":
        body["adjust_kind"] = adjust_kind
    if since_ts_millis is not None:
        body["since_ts_millis"] = since_ts_millis
    if limit is not None:
        body["limit"] = limit
    return body


def fetch(symbols, interval_unit, adjust_kind, since_ts_millis, until_ts_millis, limit):
    body = build_query(symbols, interval_unit, adjust_kind, since_ts_millis, until_ts_millis, limit)
    query = urllib.parse.urlencode(body, doseq=True)
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
    parser = argparse.ArgumentParser(description="批量获取多只 ETF 的历史 K 线（不支持分钟周期）")
    parser.add_argument("--symbols", required=True,
                        help="ETF 代码列表，逗号分隔，如 510300.XSHG,159915.XSHE；也接受 .SH/.SZ 短后缀")
    parser.add_argument("--interval-unit", dest="interval_unit", required=True, type=str.capitalize,
                        choices=INTERVAL_UNITS, help="K 线周期：Day/Week/Month/Year（大小写不敏感，不支持 Minute）")
    parser.add_argument("--adjust-kind", dest="adjust_kind", default="None",
                        choices=ADJUST_KINDS, help="复权：None（默认）/Forward/Backward")
    parser.add_argument("--since-ts-millis", dest="since_ts_millis", required=True, type=int,
                        help="开始时间戳（毫秒）；与结束时间跨度不得超过 12 个日历月")
    parser.add_argument("--until-ts-millis", dest="until_ts_millis", required=True, type=int,
                        help="结束时间戳（毫秒）")
    parser.add_argument("--limit", type=int, default=None,
                        help="每个标的返回条数上限；不传时返回请求时间范围内的全部数据")
    args = parser.parse_args()

    if args.since_ts_millis > args.until_ts_millis:
        print("--since-ts-millis 不能晚于 --until-ts-millis", file=sys.stderr)
        raise SystemExit(2)

    symbols = parse_symbols(args.symbols)
    data = fetch(symbols, args.interval_unit, args.adjust_kind,
                 args.since_ts_millis, args.until_ts_millis, args.limit)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
