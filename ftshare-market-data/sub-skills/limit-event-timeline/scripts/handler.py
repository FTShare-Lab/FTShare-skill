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
    parser.add_argument("--symbol")
    parser.add_argument("--trade_date")
    parser.add_argument("--ready", required=False)
    parser.add_argument("--status", required=False)
    parser.add_argument("--limit_up_price", required=False)
    parser.add_argument("--limit_down_price", required=False)
    parser.add_argument("--limit_up_enter", required=False)
    parser.add_argument("--limit_up_break", required=False)
    parser.add_argument("--limit_down_enter", required=True)
    parser.add_argument("--limit_down_break", required=True)
    parser.add_argument("--first_limit_up_time", required=False)
    parser.add_argument("--limit_up_break_count", required=False)
    parser.add_argument("--last_limit_down_time", required=False)
    parser.add_argument("--limit_down_break_count", required=False)
    parser.add_argument("--limit_down_seal_value", required=False)
    args = parser.parse_args()
    params = {}
    if args.symbol is not None: params["symbol"] = args.symbol
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.symbol is not None: params["symbol"] = args.symbol
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.ready is not None: params["ready"] = args.ready
    if args.status is not None: params["status"] = args.status
    if args.limit_up_price is not None: params["limit_up_price"] = args.limit_up_price
    if args.limit_down_price is not None: params["limit_down_price"] = args.limit_down_price
    if args.limit_up_enter is not None: params["limit_up_enter"] = args.limit_up_enter
    if args.limit_up_break is not None: params["limit_up_break"] = args.limit_up_break
    if args.limit_down_enter is not None: params["limit_down_enter"] = args.limit_down_enter
    if args.limit_down_break is not None: params["limit_down_break"] = args.limit_down_break
    if args.first_limit_up_time is not None: params["first_limit_up_time"] = args.first_limit_up_time
    if args.limit_up_break_count is not None: params["limit_up_break_count"] = args.limit_up_break_count
    if args.last_limit_down_time is not None: params["last_limit_down_time"] = args.last_limit_down_time
    if args.limit_down_break_count is not None: params["limit_down_break_count"] = args.limit_down_break_count
    if args.limit_down_seal_value is not None: params["limit_down_seal_value"] = args.limit_down_seal_value
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
