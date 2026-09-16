#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v2/market/data/stk-shock'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='个股异常波动')
    parser.add_argument("--ts_code")
    parser.add_argument("--trade_date")
    parser.add_argument("--start_date")
    parser.add_argument("--end_date")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=False)
    parser.add_argument("--order_book_id", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--side", required=False)
    parser.add_argument("--rank", required=True)
    parser.add_argument("--agency", required=False)
    parser.add_argument("--buy_value", required=False)
    parser.add_argument("--sell_value", required=False)
    parser.add_argument("--type", required=True)
    parser.add_argument("--reason", required=False)
    args = parser.parse_args()
    params = {}
    if args.ts_code is not None: params["ts_code"] = args.ts_code
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.start_date is not None: params["start_date"] = args.start_date
    if args.end_date is not None: params["end_date"] = args.end_date
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.order_book_id is not None: params["order_book_id"] = args.order_book_id
    if args.date is not None: params["date"] = args.date
    if args.side is not None: params["side"] = args.side
    if args.rank is not None: params["rank"] = args.rank
    if args.agency is not None: params["agency"] = args.agency
    if args.buy_value is not None: params["buy_value"] = args.buy_value
    if args.sell_value is not None: params["sell_value"] = args.sell_value
    if args.type is not None: params["type"] = args.type
    if args.reason is not None: params["reason"] = args.reason
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
