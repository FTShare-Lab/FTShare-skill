#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/sw-industry/overview'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='申万行业总览')
    parser.add_argument("--date", required=True)
    parser.add_argument("--level")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--industry-code", required=True)
    parser.add_argument("--industry-name", required=True)
    parser.add_argument("--parent-industry-name")
    parser.add_argument("--constituent-count")
    parser.add_argument("--trade-date")
    parser.add_argument("--lyr-pe")
    parser.add_argument("--lyr-pe-percentile")
    parser.add_argument("--ttm-pe")
    parser.add_argument("--ttm-pe-percentile")
    parser.add_argument("--pb")
    parser.add_argument("--pb-percentile")
    parser.add_argument("--dv-ratio")
    parser.add_argument("--dv-ratio-percentile")
    args = parser.parse_args()
    params = {}
    if args.date is not None: params["date"] = args.date
    if args.level is not None: params["level"] = args.level
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.industry_code is not None: params["industry_code"] = args.industry_code
    if args.industry_name is not None: params["industry_name"] = args.industry_name
    if args.level is not None: params["level"] = args.level
    if args.parent_industry_name is not None: params["parent_industry_name"] = args.parent_industry_name
    if args.constituent_count is not None: params["constituent_count"] = args.constituent_count
    if args.trade_date is not None: params["trade_date"] = args.trade_date
    if args.lyr_pe is not None: params["lyr_pe"] = args.lyr_pe
    if args.lyr_pe_percentile is not None: params["lyr_pe_percentile"] = args.lyr_pe_percentile
    if args.ttm_pe is not None: params["ttm_pe"] = args.ttm_pe
    if args.ttm_pe_percentile is not None: params["ttm_pe_percentile"] = args.ttm_pe_percentile
    if args.pb is not None: params["pb"] = args.pb
    if args.pb_percentile is not None: params["pb_percentile"] = args.pb_percentile
    if args.dv_ratio is not None: params["dv_ratio"] = args.dv_ratio
    if args.dv_ratio_percentile is not None: params["dv_ratio_percentile"] = args.dv_ratio_percentile
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
