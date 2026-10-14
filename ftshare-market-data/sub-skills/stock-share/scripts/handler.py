#!/usr/bin/env python3
"""查询股票股本信息。

- 传 stock_code：返回该标的截至 date 的最新股本记录（单标的模式，page/page_size 被忽略）。
- 不传 stock_code：返回 date 当日全市场股本记录，分页返回。
- date 在所有模式下均必填，格式 YYYYMMDD；缺少 date 返回 HTTP 400。
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import os
SAFE_URLOPENER = urllib.request.build_opener()

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}

def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != urllib.parse.urlparse(BASE_URL).scheme or parsed.netloc != urllib.parse.urlparse(BASE_URL).netloc:
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

ENDPOINT = "/api/v2/market/data/share/get-stock-share"


def build_params(args, page=None):
    params = {"date": args.date}
    if args.stock_code is not None:
        params["stock_code"] = args.stock_code
    if args.date_type is not None:
        params["date_type"] = args.date_type
    # page/page_size 仅在全市场查询（未指定 stock_code）时生效，单标的查询会被服务端忽略。
    if args.stock_code is None:
        params["page"] = args.page if page is None else page
        params["page_size"] = args.page_size
    return params


def fetch(params):
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询股票股本信息")
    parser.add_argument("--stock_code", default=None, help="股票代码，如 000001.SZ；不传返回全市场")
    parser.add_argument("--date", required=True, help="日期 YYYYMMDD")
    parser.add_argument("--date_type", dest="date_type", choices=["publish_date", "end_date"], default=None,
                        help="日期条件类型，默认 publish_date（发布日期），可选 end_date（生效日期）")
    parser.add_argument("--page", type=int, default=1, help="全市场查询页码，从 1 开始，默认 1；单标的查询忽略")
    parser.add_argument("--page_size", dest="page_size", type=int, default=200,
                        help="全市场查询每页条数，默认 200，最大 500；单标的查询忽略")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全市场全量数据")
    args = parser.parse_args()

    if args.stock_code is None and not (1 <= args.page_size <= 500):
        parser.error("--page_size 须在 1～500 之间")
    if args.stock_code is None and args.page < 1:
        parser.error("--page 须大于等于 1")

    if args.fetch_all:
        first = fetch(build_params(args, page=1))
        data = first.get("data") or {}
        items = list(data.get("items", []))
        total_pages = int(data.get("total_pages") or 1)
        for page in range(2, total_pages + 1):
            page_data = fetch(build_params(args, page=page)).get("data") or {}
            items.extend(page_data.get("items", []))
        data["items"] = items
        data["total_pages"] = total_pages
        first["data"] = data
        result = first
    else:
        result = fetch(build_params(args))

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
