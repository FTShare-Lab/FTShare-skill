#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/tdx-board-index'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='通达信板块指数最新快照')
    parser.add_argument("--ts_code")
    parser.add_argument("--idx_name")
    parser.add_argument("--idx_type")
    parser.add_argument("--idx_type_code")
    parser.add_argument("--market")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=False)
    parser.add_argument("--trade_date", required=True)
    parser.add_argument("--price", required=False)
    parser.add_argument("--rise_speed", required=False)
    parser.add_argument("--pre_close", required=False)
    parser.add_argument("--lead_market", required=False)
    parser.add_argument("--lead_code", required=False)
    parser.add_argument("--lead_name", required=False)
    parser.add_argument("--lead_price", required=False)
    parser.add_argument("--lead_rise_speed", required=True)
    parser.add_argument("--lead_pre_close", required=True)
    args = parser.parse_args()
    params = {}
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
    if args.price is not None: params["price"] = args.price
    if args.rise_speed is not None: params["rise_speed"] = args.rise_speed
    if args.pre_close is not None: params["pre_close"] = args.pre_close
    if args.lead_market is not None: params["lead_market"] = args.lead_market
    if args.lead_code is not None: params["lead_code"] = args.lead_code
    if args.lead_name is not None: params["lead_name"] = args.lead_name
    if args.lead_price is not None: params["lead_price"] = args.lead_price
    if args.lead_rise_speed is not None: params["lead_rise_speed"] = args.lead_rise_speed
    if args.lead_pre_close is not None: params["lead_pre_close"] = args.lead_pre_close
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
