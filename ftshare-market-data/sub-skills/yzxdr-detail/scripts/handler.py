#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/yzxdr-detail'
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
    key = _require_api_key(); parser = argparse.ArgumentParser(description='一致行动人明细')
    parser.add_argument("--year", required=True)
    parser.add_argument("--quarter", required=True)
    parser.add_argument("--stock_code")
    parser.add_argument("--page")
    parser.add_argument("--page_size")
    parser.add_argument("--total", required=False)
    parser.add_argument("--id", required=True)
    parser.add_argument("--data_date", required=False)
    parser.add_argument("--stock_name", required=True)
    parser.add_argument("--group_ratio")
    parser.add_argument("--group_shares")
    parser.add_argument("--row_no", required=False)
    parser.add_argument("--holder_name", required=False)
    parser.add_argument("--holder_rank", required=False)
    parser.add_argument("--hold_shares")
    parser.add_argument("--hold_value")
    parser.add_argument("--tradable_shares")
    parser.add_argument("--hold_ratio")
    parser.add_argument("--shares_change")
    parser.add_argument("--ratio_change")
    parser.add_argument("--holder_type")
    parser.add_argument("--share_type")
    parser.add_argument("--is_controlling")
    parser.add_argument("--notice_date")
    parser.add_argument("--created_at", required=False)
    parser.add_argument("--updated_at", required=False)
    args = parser.parse_args()
    params = {}
    if args.year is not None: params["year"] = args.year
    if args.quarter is not None: params["quarter"] = args.quarter
    if args.stock_code is not None: params["stock_code"] = args.stock_code
    if args.page is not None: params["page"] = args.page
    if args.page_size is not None: params["page_size"] = args.page_size
    if args.total is not None: params["total"] = args.total
    if args.id is not None: params["id"] = args.id
    if args.data_date is not None: params["data_date"] = args.data_date
    if args.stock_code is not None: params["stock_code"] = args.stock_code
    if args.stock_name is not None: params["stock_name"] = args.stock_name
    if args.group_ratio is not None: params["group_ratio"] = args.group_ratio
    if args.group_shares is not None: params["group_shares"] = args.group_shares
    if args.row_no is not None: params["row_no"] = args.row_no
    if args.holder_name is not None: params["holder_name"] = args.holder_name
    if args.holder_rank is not None: params["holder_rank"] = args.holder_rank
    if args.hold_shares is not None: params["hold_shares"] = args.hold_shares
    if args.hold_value is not None: params["hold_value"] = args.hold_value
    if args.tradable_shares is not None: params["tradable_shares"] = args.tradable_shares
    if args.hold_ratio is not None: params["hold_ratio"] = args.hold_ratio
    if args.shares_change is not None: params["shares_change"] = args.shares_change
    if args.ratio_change is not None: params["ratio_change"] = args.ratio_change
    if args.holder_type is not None: params["holder_type"] = args.holder_type
    if args.share_type is not None: params["share_type"] = args.share_type
    if args.is_controlling is not None: params["is_controlling"] = args.is_controlling
    if args.notice_date is not None: params["notice_date"] = args.notice_date
    if args.created_at is not None: params["created_at"] = args.created_at
    if args.updated_at is not None: params["updated_at"] = args.updated_at
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
