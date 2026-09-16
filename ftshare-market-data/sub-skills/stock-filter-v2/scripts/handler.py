#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v2/market/data/stock-list/filter'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='股票筛选')
    parser.add_argument("--symbol")
    parser.add_argument("--board")
    parser.add_argument("--listing_date_since")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--type", required=True)
    parser.add_argument("--symbol_id", required=True)
    parser.add_argument("--symbol_name", required=True)
    parser.add_argument("--close")
    parser.add_argument("--open")
    parser.add_argument("--high")
    parser.add_argument("--low")
    parser.add_argument("--prev_close")
    parser.add_argument("--change")
    parser.add_argument("--change_rate")
    parser.add_argument("--amplitude")
    parser.add_argument("--volume")
    parser.add_argument("--turnover")
    parser.add_argument("--change_rate_day5")
    parser.add_argument("--change_rate_day10")
    parser.add_argument("--change_rate_day20")
    parser.add_argument("--change_rate_day60")
    parser.add_argument("--change_rate_ytd")
    parser.add_argument("--ts_nanos")
    args = parser.parse_args()
    params = {}
    if args.symbol is not None: params["symbol"] = args.symbol
    if args.board is not None: params["board"] = args.board
    if args.listing_date_since is not None: params["listing_date_since"] = args.listing_date_since
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.type is not None: params["type"] = args.type
    if args.symbol is not None: params["symbol"] = args.symbol
    if args.symbol_id is not None: params["symbol_id"] = args.symbol_id
    if args.symbol_name is not None: params["symbol_name"] = args.symbol_name
    if args.close is not None: params["close"] = args.close
    if args.open is not None: params["open"] = args.open
    if args.high is not None: params["high"] = args.high
    if args.low is not None: params["low"] = args.low
    if args.prev_close is not None: params["prev_close"] = args.prev_close
    if args.change is not None: params["change"] = args.change
    if args.change_rate is not None: params["change_rate"] = args.change_rate
    if args.amplitude is not None: params["amplitude"] = args.amplitude
    if args.volume is not None: params["volume"] = args.volume
    if args.turnover is not None: params["turnover"] = args.turnover
    if args.change_rate_day5 is not None: params["change_rate_day5"] = args.change_rate_day5
    if args.change_rate_day10 is not None: params["change_rate_day10"] = args.change_rate_day10
    if args.change_rate_day20 is not None: params["change_rate_day20"] = args.change_rate_day20
    if args.change_rate_day60 is not None: params["change_rate_day60"] = args.change_rate_day60
    if args.change_rate_ytd is not None: params["change_rate_ytd"] = args.change_rate_ytd
    if args.ts_nanos is not None: params["ts_nanos"] = args.ts_nanos
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
