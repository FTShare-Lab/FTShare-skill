#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/tdx-board-daily'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='通达信板块日线')
    parser.add_argument("--start_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--ts_code")
    parser.add_argument("--idx_name")
    parser.add_argument("--idx_type")
    parser.add_argument("--idx_type_code")
    parser.add_argument("--market")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=False)
    parser.add_argument("--trade_date", required=True)
    parser.add_argument("--open", required=False)
    parser.add_argument("--high", required=False)
    parser.add_argument("--low", required=False)
    parser.add_argument("--close", required=False)
    parser.add_argument("--vol", required=False)
    parser.add_argument("--amount", required=False)
    parser.add_argument("--float_shares", required=False)
    args = parser.parse_args()
    params = {}
    if args.start_date is not None: params["start_date"] = args.start_date
    if args.end_date is not None: params["end_date"] = args.end_date
    if args.ts_code is not None: params["ts_code"] = args.ts_code
    if args.idx_name is not None: params["idx_name"] = args.idx_name
    if args.idx_type is not None: params["idx_type"] = args.idx_type
    if args.idx_type_code is not None: params["idx_type_code"] = args.idx_type_code
    if args.market is not None: params["market"] = args.market
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.ts_code is not None: params["ts_code"] = args.ts_code
    if args.idx_name is not None: params["idx_name"] = args.idx_name
    if args.idx_type is not None: params["idx_type"] = args.idx_type
    if args.idx_type_code is not None: params["idx_type_code"] = args.idx_type_code
    if args.market is not None: params["market"] = args.market
    if args.open is not None: params["open"] = args.open
    if args.high is not None: params["high"] = args.high
    if args.low is not None: params["low"] = args.low
    if args.close is not None: params["close"] = args.close
    if args.vol is not None: params["vol"] = args.vol
    if args.amount is not None: params["amount"] = args.amount
    if args.float_shares is not None: params["float_shares"] = args.float_shares
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
