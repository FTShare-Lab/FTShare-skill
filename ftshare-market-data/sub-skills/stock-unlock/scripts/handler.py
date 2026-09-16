#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/unlock/stock_unlock'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='限售解禁')
    parser.add_argument("--stock_code")
    parser.add_argument("--start_date")
    parser.add_argument("--end_date")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=False)
    parser.add_argument("--stock-code", required=True)
    parser.add_argument("--stock-name", required=True)
    parser.add_argument("--unlock-date")
    parser.add_argument("--holder-count")
    parser.add_argument("--able-free-shares")
    parser.add_argument("--current-free-shares")
    parser.add_argument("--non-free-shares")
    parser.add_argument("--lift-market-cap")
    parser.add_argument("--total-ratio")
    parser.add_argument("--free-ratio")
    parser.add_argument("--new-price")
    parser.add_argument("--free-shares-type", required=False)
    parser.add_argument("--b20-adjchrate")
    parser.add_argument("--a20-adjchrate")
    parser.add_argument("--crawl-date", required=False)
    parser.add_argument("--source", required=False)
    parser.add_argument("--holders", required=False)
    parser.add_argument("--holder-name", required=False)
    parser.add_argument("--add-listing-shares")
    parser.add_argument("--actual-listed-shares")
    parser.add_argument("--add-listing-cap")
    parser.add_argument("--lock-month")
    parser.add_argument("--residual-limited-shares")
    parser.add_argument("--plan-feature", required=False)
    args = parser.parse_args()
    params = {}
    if args.stock_code is not None: params["stock_code"] = args.stock_code
    if args.start_date is not None: params["start_date"] = args.start_date
    if args.end_date is not None: params["end_date"] = args.end_date
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.stock_code is not None: params["stock_code"] = args.stock_code
    if args.stock_name is not None: params["stock_name"] = args.stock_name
    if args.unlock_date is not None: params["unlock_date"] = args.unlock_date
    if args.holder_count is not None: params["holder_count"] = args.holder_count
    if args.able_free_shares is not None: params["able_free_shares"] = args.able_free_shares
    if args.current_free_shares is not None: params["current_free_shares"] = args.current_free_shares
    if args.non_free_shares is not None: params["non_free_shares"] = args.non_free_shares
    if args.lift_market_cap is not None: params["lift_market_cap"] = args.lift_market_cap
    if args.total_ratio is not None: params["total_ratio"] = args.total_ratio
    if args.free_ratio is not None: params["free_ratio"] = args.free_ratio
    if args.new_price is not None: params["new_price"] = args.new_price
    if args.free_shares_type is not None: params["free_shares_type"] = args.free_shares_type
    if args.b20_adjchrate is not None: params["b20_adjchrate"] = args.b20_adjchrate
    if args.a20_adjchrate is not None: params["a20_adjchrate"] = args.a20_adjchrate
    if args.crawl_date is not None: params["crawl_date"] = args.crawl_date
    if args.source is not None: params["source"] = args.source
    if args.holders is not None: params["holders"] = args.holders
    if args.holder_name is not None: params["holder_name"] = args.holder_name
    if args.add_listing_shares is not None: params["add_listing_shares"] = args.add_listing_shares
    if args.actual_listed_shares is not None: params["actual_listed_shares"] = args.actual_listed_shares
    if args.add_listing_cap is not None: params["add_listing_cap"] = args.add_listing_cap
    if args.lock_month is not None: params["lock_month"] = args.lock_month
    if args.residual_limited_shares is not None: params["residual_limited_shares"] = args.residual_limited_shares
    if args.plan_feature is not None: params["plan_feature"] = args.plan_feature
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
