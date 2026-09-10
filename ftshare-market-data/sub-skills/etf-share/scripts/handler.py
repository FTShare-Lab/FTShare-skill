#!/usr/bin/env python3
"""ETF 份额变动（GET /api/v2/market/data/etf-share）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v2/market/data/etf-share"

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}

STATI_PERD = ("日", "季度", "年度", "截止时点", "半年", "全部")


def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base_parsed = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base_parsed.scheme or parsed.netloc != base_parsed.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(str(req_or_url), headers=_REQUEST_HEADERS, method="GET")
    if isinstance(req_or_url, urllib.request.Request):
        for key, value in _REQUEST_HEADERS.items():
            req_or_url.add_unredirected_header(key, value)
    else:
        req_or_url = urllib.request.Request(str(req_or_url), headers=_REQUEST_HEADERS, method="GET")
    return SAFE_URLOPENER.open(req_or_url)


def build_params(args):
    params = {"etf_code": args.etf_code}
    if args.stati_perd is not None:
        params["stati_perd"] = args.stati_perd
    if args.start_date is not None:
        params["start_date"] = args.start_date
    if args.end_date is not None:
        params["end_date"] = args.end_date
    params["page"] = args.page
    params["page_size"] = args.page_size
    return params


def fetch_page(params):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{BASE_URL}{ENDPOINT}?{query}",
        headers={**HEADERS, **_REQUEST_HEADERS},
        method="GET",
    )
    try:
        with safe_urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="按 ETF 代码分页查询份额变动")
    parser.add_argument("--etf-code", dest="etf_code", required=True,
                        help="ETF 代码，如 510300")
    parser.add_argument("--stati-perd", dest="stati_perd", default=None, choices=STATI_PERD,
                        help="统计周期：日/季度/年度/截止时点/半年/全部；不传默认全部")
    parser.add_argument("--start-date", dest="start_date", type=int, default=None,
                        help="开始日期 YYYYMMDD，按 trade_date 过滤")
    parser.add_argument("--end-date", dest="end_date", type=int, default=None,
                        help="结束日期 YYYYMMDD，按 trade_date 过滤")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", dest="page_size", type=int, default=50,
                        help="每页条数，默认 50，最大 200")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    params = build_params(args)
    if args.fetch_all:
        first = fetch_page(params)
        data = first.get("data") or {}
        items = list(data.get("items", []))
        total_pages = data.get("total_pages") or 1
        for page in range(2, total_pages + 1):
            page_data = fetch_page({**params, "page": page})
            items.extend((page_data.get("data") or {}).get("items", []))
        result = {
            "items": items,
            "total_pages": total_pages,
            "total_items": data.get("total_items", len(items)),
        }
    else:
        result = fetch_page(params)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
