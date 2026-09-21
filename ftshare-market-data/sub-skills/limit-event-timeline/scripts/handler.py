#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v2/market/data/limit-event-timeline-3s'
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr); raise SystemExit(2)
    return key
def safe_urlopen(request, timeout=30):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr); raise SystemExit(1)
    if not isinstance(request, urllib.request.Request): request = urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    request.add_unredirected_header("Content-Type", "application/json")
    return SAFE_URLOPENER.open(request, timeout=timeout)
def main():
    key = _require_api_key(); parser = argparse.ArgumentParser(description='涨跌停事件时间线')
    parser.add_argument("--symbol", help="标的代码，如 000001.XSHE；不传返回全市场")
    parser.add_argument("--trade_date", help="交易日期 YYYYMMDD；不传或传当日时查询实时数据")
    parser.add_argument("--page", help="页码，从 1 开始，默认 1")
    parser.add_argument("--page_size", help="每页条数，默认 50，最大 200")
    args = parser.parse_args()
    params = {}
    if args.symbol is not None: params["symbol"] = args.symbol
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    request = urllib.request.Request(BASE_URL + ENDPOINT + query, headers={**_REQUEST_HEADERS, "FTSHARE_API_KEY": key, "Content-Type": "application/json", "X-Client-Name": "ft-claw"}, method="GET")
    try:
        with safe_urlopen(request) as response: payload = json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr); raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr); raise SystemExit(1)
if __name__ == "__main__": main()
