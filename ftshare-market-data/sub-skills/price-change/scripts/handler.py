#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v2/market/data/price/get-price-change'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='价格变动')
    parser.add_argument("--stock_code", required=True)
    parser.add_argument("--base_date", required=True)
    parser.add_argument("--n", required=True)
    parser.add_argument("--direction", required=True)
    parser.add_argument("--stock_name", required=True)
    parser.add_argument("--start_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--actual_trading_days", required=True)
    parser.add_argument("--start_price", required=True)
    parser.add_argument("--end_price", required=True)
    parser.add_argument("--price_change", required=True)
    parser.add_argument("--change_pct", required=False)
    args = parser.parse_args()
    params = {}
    if args.stock_code is not None: params["stock_code"] = args.stock_code
    if args.base_date is not None: params["base_date"] = args.base_date
    if args.n is not None: params["n"] = args.n
    if args.direction is not None: params["direction"] = args.direction
    if args.stock_name is not None: params["stock_name"] = args.stock_name
    if args.start_date is not None: params["start_date"] = args.start_date
    if args.end_date is not None: params["end_date"] = args.end_date
    if args.actual_trading_days is not None: params["actual_trading_days"] = args.actual_trading_days
    if args.start_price is not None: params["start_price"] = args.start_price
    if args.end_price is not None: params["end_price"] = args.end_price
    if args.price_change is not None: params["price_change"] = args.price_change
    if args.change_pct is not None: params["change_pct"] = args.change_pct
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
