#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v3/market/data/ashare-news-sentiment-factors'
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(request, timeout=30):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    return SAFE_URLOPENER.open(request, timeout=timeout)


def _parse_date(value, flag):
    try:
        return datetime.strptime(value, "%Y%m%d")
    except ValueError:
        print(f"{flag} 必须为 YYYYMMDD 格式", file=sys.stderr)
        raise SystemExit(2)


def main():
    key = _require_api_key()
    parser = argparse.ArgumentParser(description='查询 A 股新闻情绪因子')
    parser.add_argument("--trade-code", required=True, help="股票代码，格式 600519.SH；也接受 600519、SH:600519、600519.XSHG")
    parser.add_argument("--date", help="单日预测日 YYYYMMDD，与 --start-date/--end-date 互斥")
    parser.add_argument("--start-date", help="起始预测日 YYYYMMDD，必须与 --end-date 同时传入")
    parser.add_argument("--end-date", help="截止预测日 YYYYMMDD，必须与 --start-date 同时传入")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", type=int, default=50, help="每页条数，默认 50，最大 200")

    args = parser.parse_args()
    if args.page < 1:
        print("--page 必须 >= 1", file=sys.stderr)
        raise SystemExit(2)
    if not 1 <= args.page_size <= 200:
        print("--page-size 必须在 1~200 之间", file=sys.stderr)
        raise SystemExit(2)
    if args.date is not None and (args.start_date is not None or args.end_date is not None):
        print("--date 不能与 --start-date/--end-date 同时传入", file=sys.stderr)
        raise SystemExit(2)
    if (args.start_date is None) != (args.end_date is None):
        print("--start-date 与 --end-date 必须同时传入", file=sys.stderr)
        raise SystemExit(2)
    if args.date is not None:
        _parse_date(args.date, "--date")
    if args.start_date is not None:
        d0 = _parse_date(args.start_date, "--start-date")
        d1 = _parse_date(args.end_date, "--end-date")
        if d1 < d0:
            print("--start-date 不能晚于 --end-date", file=sys.stderr)
            raise SystemExit(2)
        if (d1 - d0).days > 30:
            print("--start-date 与 --end-date 含首尾跨度不能超过 31 天", file=sys.stderr)
            raise SystemExit(2)

    params = {'trade_code': args.trade_code}
    if args.date is not None:
        params['date'] = args.date
    if args.start_date is not None:
        params['start_date'] = args.start_date
        params['end_date'] = args.end_date
    params['page'] = args.page
    params['page_size'] = args.page_size

    query = "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(BASE_URL + ENDPOINT + query, headers={"FTSHARE_API_KEY": key, "X-Client-Name": "ft-claw", "Content-Type": "application/json"}, method="GET")
    try:
        with safe_urlopen(request) as response:
            payload = json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()