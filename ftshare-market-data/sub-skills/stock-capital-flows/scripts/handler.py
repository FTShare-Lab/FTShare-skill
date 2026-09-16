#!/usr/bin/env python3
"""查询 A 股股票资金流向（实时快照 / 历史 15 分钟切片），支持分页、全量拉取与单股定位"""
import argparse
import json
import re
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
ENDPOINT = "/api/v1/market/data/stock-capital-flows"

# HHMM，分钟须为 00/15/30/45
VALID_TIME_RE = re.compile(r"^\d{2}(00|15|30|45)$")


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


def fetch_page(page: int, page_size: int, date: str = None, time_slice: str = None) -> dict:
    params = {"page": page, "page_size": page_size}
    if date:
        params["date"] = date
        params["time"] = time_slice or "1530"
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    try:
        with safe_urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def find_symbol(symbol: str, page_size: int, date: str = None, time_slice: str = None) -> dict:
    """定位单只标的。先扫第 1 页与最后 1 页（覆盖排名头部/尾部），命中即返回；
    否则从前向后补扫中间页。返回其在全市场中的排名与记录。"""
    target = symbol.strip().upper()

    def match(data, page_no):
        for i, it in enumerate(data.get("items", [])):
            if (it.get("symbol") or "").strip().upper() == target:
                rank = (page_no - 1) * page_size + i + 1
                return rank, it
        return None, None

    first = fetch_page(1, page_size, date, time_slice)
    total_pages = first.get("total_pages", 1)
    total_items = first.get("total_items", 0)

    rank, rec = match(first, 1)
    if rec is not None:
        return {"found": True, "symbol": symbol, "rank": rank,
                "total_items": total_items, "record": rec}

    if total_pages > 1:
        last = fetch_page(total_pages, page_size, date, time_slice)
        rank, rec = match(last, total_pages)
        if rec is not None:
            return {"found": True, "symbol": symbol, "rank": rank,
                    "total_items": total_items, "record": rec}

    for p in range(2, total_pages):
        rank, rec = match(fetch_page(p, page_size, date, time_slice), p)
        if rec is not None:
            return {"found": True, "symbol": symbol, "rank": rank,
                    "total_items": total_items, "record": rec}

    return {"found": False, "symbol": symbol, "rank": None, "total_items": total_items}


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询 A 股股票资金流向（实时快照 / 历史 15 分钟切片）")
    parser.add_argument("--date", type=str, default=None,
                        help="查询日期，格式 YYYYMMDD；不传则返回当前实时快照")
    parser.add_argument("--time", type=str, default=None,
                        help="15 分钟切片时刻，格式 HHMM，分钟须为 00/15/30/45；仅在传 --date 时有效，默认 1530（日终）")
    parser.add_argument("--symbol", type=str, default=None,
                        help="只返回指定标的（如 601138.SH）；逐页扫描定位，找到即停，返回其排名与记录")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=50, help="每页记录数（默认 50）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    # --time 仅在指定 --date 时有意义
    time_slice = None
    if args.date:
        time_slice = args.time or "1530"
        if not VALID_TIME_RE.match(time_slice):
            print(f"错误：--time 必须为 HHMM 且分钟须为 00/15/30/45，当前为 [{time_slice}]", file=sys.stderr)
            sys.exit(1)
    elif args.time:
        print("错误：--time 仅在指定 --date 时有效。查询实时快照请去掉 --time。", file=sys.stderr)
        sys.exit(1)

    # 单股定位（优先级最高；与 --all 互斥时以 --symbol 为准）
    if args.symbol:
        result = find_symbol(args.symbol, args.page_size, args.date, time_slice)
    elif args.fetch_all:
        first = fetch_page(1, args.page_size, args.date, time_slice)
        all_items = list(first.get("items", []))
        total_pages = first.get("total_pages", 1)
        for p in range(2, total_pages + 1):
            page_data = fetch_page(p, args.page_size, args.date, time_slice)
            all_items.extend(page_data.get("items", []))
        result = {
            "items": all_items,
            "total_pages": total_pages,
            "total_items": first.get("total_items", len(all_items)),
        }
    else:
        result = fetch_page(args.page, args.page_size, args.date, time_slice)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
