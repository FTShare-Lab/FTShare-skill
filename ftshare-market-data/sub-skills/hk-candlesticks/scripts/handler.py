#!/usr/bin/env python3
"""查询港股 K 线（market.ft.tech）"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
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

INTERVAL_UNITS = ("day", "month", "quarter", "year")
ADJUST_KINDS = ("forward", "none")

BEIJING_TZ = timezone(timedelta(hours=8))
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def _validate_date(value: str, name: str) -> str:
    """校验 YYYY-MM-DD 格式；若传入时带时间/时区则截取日期部分（东八区）。"""
    v = value.strip()
    if DATE_RE.match(v):
        return v
    try:
        raw = v
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=BEIJING_TZ)
        else:
            dt = dt.astimezone(BEIJING_TZ)
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        print(f"{name} 格式错误，需为 YYYY-MM-DD：{value}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询港股 K 线")
    parser.add_argument(
        "--trade-code",
        dest="trade_code",
        required=True,
        help="港股代码，如 00700.HK 或 700；响应统一为 5 位 + .HK",
    )
    parser.add_argument(
        "--interval-unit",
        dest="interval_unit",
        required=True,
        choices=INTERVAL_UNITS,
        help="K 线间隔：day / month / quarter / year",
    )
    parser.add_argument(
        "--until-date",
        dest="until_date",
        required=True,
        help="结束日期，YYYY-MM-DD（东八区交易日）",
    )
    parser.add_argument(
        "--since-date",
        dest="since_date",
        default=None,
        help="开始日期，YYYY-MM-DD；不传则从库中最早数据起",
    )
    parser.add_argument(
        "--adjust-kind",
        dest="adjust_kind",
        default="forward",
        choices=ADJUST_KINDS,
        help="复权类型：forward（前复权，默认）或 none（不复权）",
    )
    parser.add_argument(
        "--interval-value",
        dest="interval_value",
        type=int,
        default=1,
        help="间隔数值，当前仅支持 1（默认 1）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="返回条数上限；日 K 在 SQL 层下推，月/季/年聚合后截取最近 N 根",
    )
    args = parser.parse_args()

    until_date = _validate_date(args.until_date, "--until-date")
    since_date = None
    if args.since_date is not None and args.since_date.strip():
        since_date = _validate_date(args.since_date, "--since-date")

    params = {
        "trade_code": args.trade_code.strip(),
        "interval_unit": args.interval_unit,
        "until_date": until_date.replace("-", ""),
        "adjust_kind": args.adjust_kind,
        "interval_value": args.interval_value,
    }
    if since_date is not None:
        params["since_date"] = since_date.replace("-", "")
    if args.limit is not None:
        params["limit"] = args.limit

    path = "/api/v2/market/data/hk/hk-candlesticks"
    url = BASE_URL + path + "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, method="GET", headers=_REQUEST_HEADERS)

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
