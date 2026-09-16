#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/eastmoney-dapan-flow'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='东方财富大盘资金流')
    parser.add_argument("--trade_date")
    parser.add_argument("--start_date")
    parser.add_argument("--end_date")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=False)
    parser.add_argument("--sh_close", required=False)
    parser.add_argument("--sh_change_pct", required=False)
    parser.add_argument("--sz_close", required=False)
    parser.add_argument("--sz_change_pct", required=False)
    parser.add_argument("--main_net", required=False)
    parser.add_argument("--main_pct", required=False)
    parser.add_argument("--xlarge_net", required=False)
    parser.add_argument("--xlarge_pct", required=False)
    parser.add_argument("--large_net", required=False)
    parser.add_argument("--large_pct", required=False)
    parser.add_argument("--mid_net", required=False)
    parser.add_argument("--mid_pct", required=False)
    parser.add_argument("--small_net", required=False)
    parser.add_argument("--small_pct", required=False)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    params = {}
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.start_date is not None: params["start_date"] = args.start_date
    if args.end_date is not None: params["end_date"] = args.end_date
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.sh_close is not None: params["sh_close"] = args.sh_close
    if args.sh_change_pct is not None: params["sh_change_pct"] = args.sh_change_pct
    if args.sz_close is not None: params["sz_close"] = args.sz_close
    if args.sz_change_pct is not None: params["sz_change_pct"] = args.sz_change_pct
    if args.main_net is not None: params["main_net"] = args.main_net
    if args.main_pct is not None: params["main_pct"] = args.main_pct
    if args.xlarge_net is not None: params["xlarge_net"] = args.xlarge_net
    if args.xlarge_pct is not None: params["xlarge_pct"] = args.xlarge_pct
    if args.large_net is not None: params["large_net"] = args.large_net
    if args.large_pct is not None: params["large_pct"] = args.large_pct
    if args.mid_net is not None: params["mid_net"] = args.mid_net
    if args.mid_pct is not None: params["mid_pct"] = args.mid_pct
    if args.small_net is not None: params["small_net"] = args.small_net
    if args.small_pct is not None: params["small_pct"] = args.small_pct
    if args.name is not None: params["name"] = args.name
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
