#!/usr/bin/env python3
"""期货实时日K线（GET /api/v4/market/data/futures-realtime-day-kline）"""
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
ENDPOINT = "/api/v4/market/data/futures-realtime-day-kline"

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


def fetch(symbols):
    query = urllib.parse.urlencode({"symbols": symbols}, doseq=True)
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
    parser = argparse.ArgumentParser(description="批量查询期货合约当前交易日的实时日 K 线")
    parser.add_argument("--symbols", required=True,
                        help="期货合约代码列表，逗号分隔，1～20 个，如 A2611.DCE,CU2611.SHF；支持 .DCE/.SHF/.CZC/.INE/.GFE/.CFE 短后缀")
    args = parser.parse_args()

    symbols = parse_symbols(args.symbols)
    print(json.dumps(fetch(symbols), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
