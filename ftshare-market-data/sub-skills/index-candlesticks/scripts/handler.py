#!/usr/bin/env python3
"""查询单只指数历史 K 线（GET /api/v1/market/data/index-candlesticks）"""
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
ENDPOINT = "/api/v1/market/data/index-candlesticks"

INTERVAL_UNITS = ("Minute", "Day", "Week", "Month", "Year")
ADJUST_KINDS = ("None", "Forward", "Backward")


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


HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def build_body(symbol, interval_unit, interval_value, adjust_kind,
               since_ts_millis, until_ts_millis, limit):
    body = {
        "symbol": symbol,
        "interval_unit": interval_unit,
        "until_ts_millis": until_ts_millis,
    }
    if interval_value is not None and interval_value != 1:
        body["interval_value"] = interval_value
    if adjust_kind and adjust_kind != "None":
        body["adjust_kind"] = adjust_kind
    if since_ts_millis is not None:
        body["since_ts_millis"] = since_ts_millis
    if limit is not None:
        body["limit"] = limit
    return body


def fetch(
symbol, interval_unit, interval_value, adjust_kind,
          since_ts_millis, until_ts_millis, limit):
    body = build_body(symbol, interval_unit, interval_value, adjust_kind,
                      since_ts_millis, until_ts_millis, limit)
    query = urllib.parse.urlencode(body, doseq=True)
    url = f"{BASE_URL}{ENDPOINT}?{query}"
    req = urllib.request.Request(
        url,
        headers={**HEADERS, **_REQUEST_HEADERS},
        method="GET",
    )
    try:
        with safe_urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        print(f"HTTP {e.code}: {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询单只指数历史 K 线（GET 查询参数）")
    parser.add_argument("--symbol", required=True, help="指数代码，如 000300.XSHG、399001.XSHE")
    parser.add_argument("--interval-unit", dest="interval_unit", required=True,
                        choices=INTERVAL_UNITS, help="K 线周期：Minute/Day/Week/Month/Year")
    parser.add_argument("--interval-value", dest="interval_value", type=int, default=1,
                        help="间隔数值，默认 1（Minute+5 表示 5 分钟 K）")
    parser.add_argument("--adjust-kind", dest="adjust_kind", default="None",
                        choices=ADJUST_KINDS, help="复权：None（默认）/Forward/Backward")
    parser.add_argument("--since-ts-millis", dest="since_ts_millis", type=int, default=None,
                        help="开始时间戳（毫秒）；分钟 K 与 until 跨度 ≤3 天")
    parser.add_argument("--until-ts-millis", dest="until_ts_millis", required=True, type=int,
                        help="结束时间戳（毫秒）")
    parser.add_argument("--limit", type=int, default=None, help="返回条数上限")
    args = parser.parse_args()

    data = fetch(args.symbol, args.interval_unit, args.interval_value,
                 args.adjust_kind, args.since_ts_millis, args.until_ts_millis, args.limit)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
