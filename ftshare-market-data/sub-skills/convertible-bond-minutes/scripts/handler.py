#!/usr/bin/env python3
"""查询单只或批量可转债历史分钟 K 线（GET /api/v2/market/data/convertible-bond-minute-candlesticks）"""
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
ENDPOINT = "/api/v2/market/data/convertible-bond-minute-candlesticks"

INTERVAL_VALUES = (1, 5, 15)
MAX_SYMBOLS = 20

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
    if len(syms) > MAX_SYMBOLS:
        print(f"--symbols 最多 {MAX_SYMBOLS} 个标的，当前 {len(syms)} 个", file=sys.stderr)
        sys.exit(1)
    return syms


def build_query(symbol, symbols, interval_value, since_ts_millis, until_ts_millis, limit):
    body = {}
    if symbol is not None:
        body["symbol"] = symbol
    if symbols is not None:
        body["symbols"] = symbols
    if interval_value is not None:
        body["interval_value"] = interval_value
    body["since_ts_millis"] = since_ts_millis
    body["until_ts_millis"] = until_ts_millis
    if limit is not None:
        body["limit"] = limit
    return body


def fetch(symbol, symbols, interval_value, since_ts_millis, until_ts_millis, limit):
    body = build_query(symbol, symbols, interval_value, since_ts_millis, until_ts_millis, limit)
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
    parser = argparse.ArgumentParser(description="查询单只或批量可转债历史分钟 K 线（GET 查询参数）")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--symbol", help="单只可转债代码，如 113042.SH")
    target.add_argument("--symbols", help="可转债代码列表，逗号分隔，1～20 只，如 113042.SH,123107.SZ")
    parser.add_argument("--interval-value", dest="interval_value", type=int, default=None,
                        choices=INTERVAL_VALUES, help="分钟周期：1/5/15，默认 1")
    parser.add_argument("--since-ts-millis", dest="since_ts_millis", required=True, type=int,
                        help="起始时间戳（毫秒）；与结束时间相差不超过 3 个北京时间自然日")
    parser.add_argument("--until-ts-millis", dest="until_ts_millis", required=True, type=int,
                        help="结束时间戳（毫秒）")
    parser.add_argument("--limit", type=int, default=None,
                        help="每只标的聚合后返回条数上限，范围 1～1000；省略返回窗口内全部记录")
    args = parser.parse_args()

    if args.since_ts_millis > args.until_ts_millis:
        print("--since-ts-millis 不能晚于 --until-ts-millis", file=sys.stderr)
        raise SystemExit(2)
    if args.limit is not None and not 1 <= args.limit <= 1000:
        print("--limit 须在 1～1000 之间", file=sys.stderr)
        raise SystemExit(2)

    symbols = parse_symbols(args.symbols) if args.symbols is not None else None
    data = fetch(args.symbol, symbols, args.interval_value,
                 args.since_ts_millis, args.until_ts_millis, args.limit)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()