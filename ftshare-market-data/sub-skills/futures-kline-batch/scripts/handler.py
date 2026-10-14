#!/usr/bin/env python3
"""批量期货合约历史K线（GET /api/v2/market/data/futures/kline/batch）"""
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
ENDPOINT = "/api/v2/market/data/futures/kline/batch"

INTERVALS = ("daily", "weekly", "monthly", "quarterly", "yearly")
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
        print(f"--symbols 最多 {MAX_SYMBOLS} 个合约，当前 {len(syms)} 个", file=sys.stderr)
        sys.exit(1)
    return syms


def build_query(symbols, interval, start, end, limit):
    body = {"symbols": symbols, "interval": interval.lower()}
    if start is not None:
        body["start"] = start
    if end is not None:
        body["end"] = end
    if limit is not None:
        body["limit"] = limit
    return body


def fetch(symbols, interval, start, end, limit):
    body = build_query(symbols, interval, start, end, limit)
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
    parser = argparse.ArgumentParser(description="批量查询多个期货合约的历史 K 线")
    parser.add_argument("--symbols", required=True,
                        help="期货合约代码列表，逗号分隔，1～20 个，如 A2611.DCE,M2611.DCE；支持 .DCE/.SHF/.CZC/.INE/.GFE/.CFE 短后缀")
    parser.add_argument("--interval", default="daily", choices=INTERVALS,
                        help="K 线周期，默认 daily；周/月/季/年 K 由日 K 聚合")
    parser.add_argument("--start", type=int, default=None,
                        help="起始时间戳（毫秒，闭区间）")
    parser.add_argument("--end", type=int, default=None,
                        help="结束时间戳（毫秒，闭区间）；不能单独传入")
    parser.add_argument("--limit", type=int, default=None,
                        help="每个合约返回的最新 K 线条数，默认 500")
    args = parser.parse_args()

    if args.end is not None and args.start is None:
        print("--end 不能单独传入，必须与 --start 同时使用", file=sys.stderr)
        raise SystemExit(2)

    symbols = parse_symbols(args.symbols)
    data = fetch(symbols, args.interval, args.start, args.end, args.limit)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
