#!/usr/bin/env python3
"""查询股指期货合约深度快照、对应指数价格与仪器映射。

- 不传日期返回最新交易日。
- trade_date 与 start_date/end_date 互斥；区间查询须成对传入。
- code_prefix 支持 IF / IC / IM / IH，不区分大小写。
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v1/market/data/index-fut/depth"
CODE_PREFIXES = ["IF", "IC", "IM", "IH"]


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(req_or_url, timeout=30):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    for key, value in _REQUEST_HEADERS.items():
        req_or_url.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(req_or_url, timeout=timeout)


def _validate_date(name, value):
    if re.fullmatch(r"\d{8}", value) is None:
        print(f"{name} 格式须为 YYYYMMDD: {value}", file=sys.stderr)
        raise SystemExit(2)
    return value


def build_params(args):
    params = {}
    if args.trade_date is not None:
        params["trade_date"] = args.trade_date
    if args.start_date is not None:
        params["start_date"] = args.start_date
    if args.end_date is not None:
        params["end_date"] = args.end_date
    if args.code_prefix is not None:
        params["code_prefix"] = args.code_prefix
    return params


def fetch(params):
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    request = urllib.request.Request(
        BASE_URL + ENDPOINT + query,
        headers={**_REQUEST_HEADERS, "X-Client-Name": "ft-claw"},
        method="GET",
    )
    try:
        with safe_urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询股指期货与指数深度行情")
    parser.add_argument("--trade-date", dest="trade_date", default=None,
                        help="单日查询日期 YYYYMMDD；不传日期参数时查询最新交易日")
    parser.add_argument("--start-date", dest="start_date", default=None,
                        help="区间起始日 YYYYMMDD；必须与 --end-date 同时传入")
    parser.add_argument("--end-date", dest="end_date", default=None,
                        help="区间结束日 YYYYMMDD；必须与 --start-date 同时传入，且区间不超过 3 年")
    parser.add_argument("--code-prefix", dest="code_prefix", type=str.upper, choices=CODE_PREFIXES, default=None,
                        help="品种筛选 IF / IC / IM / IH，不区分大小写；不传返回全部")
    args = parser.parse_args()

    if args.trade_date is not None and (args.start_date is not None or args.end_date is not None):
        print("--trade-date 与 --start-date / --end-date 互斥", file=sys.stderr)
        raise SystemExit(2)
    if (args.start_date is None) != (args.end_date is None):
        print("--start-date 与 --end-date 必须同时传入", file=sys.stderr)
        raise SystemExit(2)
    for name, value in (("--trade-date", args.trade_date), ("--start-date", args.start_date), ("--end-date", args.end_date)):
        if value is not None:
            _validate_date(name, value)
    if args.start_date is not None and args.end_date < args.start_date:
        print("--end-date 不得早于 --start-date", file=sys.stderr)
        raise SystemExit(2)

    result = fetch(build_params(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
