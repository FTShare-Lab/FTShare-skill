#!/usr/bin/env python3
"""查询东财美股历史日K线。

有日期范围时：按 3 天窗口分批请求（避免服务端大范围 500），合并去重后客户端分页。
无日期范围时：全量拉取（不传日期参数）。
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
import os

SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v1/market/data/eastmoney-us-stock-daily-ohlc"


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


MAX_WINDOW_DAYS = 3  # 每次请求日期跨度不超过 3 天


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


def _fetch_page(stock_code: str, start_date: str = None, end_date: str = None,
                page: int = 1, page_size: int = 100) -> dict:
    params = {"stock_code": stock_code, "page": page, "page_size": page_size}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    qs = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    with safe_urlopen(url) as resp:
        return json.loads(resp.read().decode())


def _fetch_window_pages(stock_code: str, start: str, end: str, page_size: int = 100) -> list:
    """请求一个日期窗口内所有页的数据。"""
    first = _fetch_page(stock_code, start, end, 1, page_size)
    data = first.get("data") or {}
    records = list(data.get("records", []))
    total_pages = data.get("pages", 1)
    for p in range(2, total_pages + 1):
        page_data = _fetch_page(stock_code, start, end, p, page_size)
        pdata = page_data.get("data") or {}
        records.extend(pdata.get("records", []))
    return records


def _fetch_full(stock_code: str, page_size: int = 100) -> list:
    """全量拉取（不传日期参数）。"""
    first = _fetch_page(stock_code, page=1, page_size=page_size)
    data = first.get("data") or {}
    records = list(data.get("records", []))
    total_pages = data.get("pages", 1)
    for p in range(2, total_pages + 1):
        page_data = _fetch_page(stock_code, page=p, page_size=page_size)
        pdata = page_data.get("data") or {}
        records.extend(pdata.get("records", []))
    return records


def _normalize_date(d: str) -> str:
    d = d.strip().replace("-", "")
    if len(d) == 8:
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    return d


def _date_range_windows(start: str, end: str, max_days: int = 3) -> list:
    """将日期区间拆分为 max_days 天的小窗口。"""
    fmt = "%Y-%m-%d"
    s = datetime.strptime(start, fmt)
    e = datetime.strptime(end, fmt)
    windows = []
    cur = s
    while cur <= e:
        w_end = min(cur + timedelta(days=max_days - 1), e)
        windows.append((cur.strftime(fmt), w_end.strftime(fmt)))
        cur = w_end + timedelta(days=1)
    return windows


def fetch_by_windows(stock_code: str, start_date: str, end_date: str) -> list:
    """按 3 天窗口分批请求，合并去重。"""
    windows = _date_range_windows(start_date, end_date, MAX_WINDOW_DAYS)
    total_wins = len(windows)
    print(f"info: 日期区间 {start_date}~{end_date} 拆分为 {total_wins} 个 {MAX_WINDOW_DAYS} 天窗口", file=sys.stderr)

    all_records = []
    seen = set()
    for i, (ws, we) in enumerate(windows):
        records = _fetch_window_pages(stock_code, ws, we)
        for r in records:
            d = r.get("date", "")
            if d and d not in seen:
                seen.add(d)
                all_records.append(r)
        if total_wins > 1:
            print(f"info: 窗口 {i + 1}/{total_wins} ({ws}~{we}) 获取 {len(records)} 条", file=sys.stderr)

    # 按日期排序
    all_records.sort(key=lambda r: r.get("date", ""))
    return all_records


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询东财美股历史日K线（3天窗口分批）")
    parser.add_argument("--stock_code", required=True, help="股票代码，如 AAL")
    parser.add_argument("--start_date", default=None, help="起始日期（含），格式 YYYY-MM-DD 或 YYYYMMDD")
    parser.add_argument("--end_date", default=None, help="截止日期（含），格式 YYYY-MM-DD 或 YYYYMMDD")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始，默认 1）")
    parser.add_argument("--page_size", type=int, default=50, help="每页条数（默认 50）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="返回全量数据（不分页）")
    args = parser.parse_args()

    has_date_filter = bool(args.start_date or args.end_date)

    if has_date_filter:
        start = _normalize_date(args.start_date) if args.start_date else ""
        end = _normalize_date(args.end_date) if args.end_date else ""
        # 确保至少有一个边界
        if not start:
            start = "2000-01-01"
        if not end:
            end = "2099-12-31"
        records = fetch_by_windows(args.stock_code, start, end)
    else:
        records = _fetch_full(args.stock_code)

    total = len(records)

    if total == 0:
        result = {"code": 0, "message": "success", "data": None}
    elif args.fetch_all:
        result = {
            "code": 0,
            "message": "success",
            "data": {
                "pageNum": 1,
                "pageSize": total,
                "total": total,
                "pages": 1,
                "records": records,
            },
        }
    else:
        start_idx = (args.page - 1) * args.page_size
        end_idx = start_idx + args.page_size
        result = {
            "code": 0,
            "message": "success",
            "data": {
                "pageNum": args.page,
                "pageSize": args.page_size,
                "total": total,
                "pages": max(1, (total + args.page_size - 1) // args.page_size),
                "records": records[start_idx:end_idx],
            },
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
