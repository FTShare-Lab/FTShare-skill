#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/eastmoney-rank'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='东方财富股票排名')
    parser.add_argument("--rank_group")
    parser.add_argument("--market")
    parser.add_argument("--trade_date")
    parser.add_argument("--display_name", required=True)
    parser.add_argument("--metric_name", required=True)
    parser.add_argument("--total", required=False)
    parser.add_argument("--items", required=False)
    parser.add_argument("--rank_no", required=True)
    parser.add_argument("--rank_change", required=False)
    parser.add_argument("--normalized_symbol", required=False)
    parser.add_argument("--stock_name", required=True)
    parser.add_argument("--hot_score", required=False)
    parser.add_argument("--latest_price", required=False)
    parser.add_argument("--change_amount", required=False)
    parser.add_argument("--change_pct", required=False)
    parser.add_argument("--raw_symbol", required=False)
    args = parser.parse_args()
    params = {}
    if args.rank_group is not None: params["rank_group"] = args.rank_group
    if args.market is not None: params["market"] = args.market
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.display_name is not None: params["display_name"] = args.display_name
    if args.metric_name is not None: params["metric_name"] = args.metric_name
    if args.total is not None: params["total"] = args.total
    if args.items is not None: params["items"] = args.items
    if args.rank_no is not None: params["rank_no"] = args.rank_no
    if args.rank_change is not None: params["rank_change"] = args.rank_change
    if args.normalized_symbol is not None: params["normalized_symbol"] = args.normalized_symbol
    if args.stock_name is not None: params["stock_name"] = args.stock_name
    if args.hot_score is not None: params["hot_score"] = args.hot_score
    if args.latest_price is not None: params["latest_price"] = args.latest_price
    if args.change_amount is not None: params["change_amount"] = args.change_amount
    if args.change_pct is not None: params["change_pct"] = args.change_pct
    if args.raw_symbol is not None: params["raw_symbol"] = args.raw_symbol
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
