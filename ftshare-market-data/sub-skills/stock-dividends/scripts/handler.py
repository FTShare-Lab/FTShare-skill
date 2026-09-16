#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/stock-dividends'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='股票分红记录')
    parser.add_argument("--symbol")
    parser.add_argument("--since_date")
    parser.add_argument("--until_date")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=False)
    parser.add_argument("--ann_date", required=False)
    parser.add_argument("--reporting_period", required=False)
    parser.add_argument("--cash_dividend_ratio", required=False)
    parser.add_argument("--bonus_issue_ratio", required=False)
    parser.add_argument("--bonus_issue_from_capital_reserves_ratio", required=False)
    parser.add_argument("--ex_dividend_date", required=False)
    parser.add_argument("--ann_url", required=False)
    args = parser.parse_args()
    params = {}
    if args.symbol is not None: params["symbol"] = args.symbol
    if args.since_date is not None: params["since_date"] = args.since_date
    if args.until_date is not None: params["until_date"] = args.until_date
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.symbol is not None: params["symbol"] = args.symbol
    if args.ann_date is not None: params["ann_date"] = args.ann_date
    if args.reporting_period is not None: params["reporting_period"] = args.reporting_period
    if args.cash_dividend_ratio is not None: params["cash_dividend_ratio"] = args.cash_dividend_ratio
    if args.bonus_issue_ratio is not None: params["bonus_issue_ratio"] = args.bonus_issue_ratio
    if args.bonus_issue_from_capital_reserves_ratio is not None: params["bonus_issue_from_capital_reserves_ratio"] = args.bonus_issue_from_capital_reserves_ratio
    if args.ex_dividend_date is not None: params["ex_dividend_date"] = args.ex_dividend_date
    if args.ann_url is not None: params["ann_url"] = args.ann_url
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
