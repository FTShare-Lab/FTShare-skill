#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/sw-industry/constituent-history'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='申万行业成份股历史')
    parser.add_argument("--industry_code", required=True)
    parser.add_argument("--stock-code", required=True)
    parser.add_argument("--stock-name", required=True)
    parser.add_argument("--in-date")
    parser.add_argument("--out-date")
    parser.add_argument("--sw-level1-code", required=True)
    parser.add_argument("--sw-level1-name", required=True)
    parser.add_argument("--sw-level2-code")
    parser.add_argument("--sw-level2-name")
    parser.add_argument("--sw-level3-code")
    parser.add_argument("--sw-level3-name")
    args = parser.parse_args()
    params = {}
    if args.industry_code is not None: params["industry_code"] = args.industry_code
    if args.stock_code is not None: params["stock_code"] = args.stock_code
    if args.stock_name is not None: params["stock_name"] = args.stock_name
    if args.in_date is not None: params["in_date"] = args.in_date
    if args.out_date is not None: params["out_date"] = args.out_date
    if args.sw_level1_code is not None: params["sw_level1_code"] = args.sw_level1_code
    if args.sw_level1_name is not None: params["sw_level1_name"] = args.sw_level1_name
    if args.sw_level2_code is not None: params["sw_level2_code"] = args.sw_level2_code
    if args.sw_level2_name is not None: params["sw_level2_name"] = args.sw_level2_name
    if args.sw_level3_code is not None: params["sw_level3_code"] = args.sw_level3_code
    if args.sw_level3_name is not None: params["sw_level3_name"] = args.sw_level3_name
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
