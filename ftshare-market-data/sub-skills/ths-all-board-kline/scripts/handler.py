#!/usr/bin/env python3
"""查询同花顺全板块K线-按日期范围（market.ft.tech）"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/ths-all-board-kline"
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}


def _normalize_date(d):
    """Normalize YYYYMMDD or YYYY-MM-DD to YYYY-MM-DD."""
    if not d:
        return d
    d = d.strip()
    if re.match(r"^\d{8}$", d):
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        return d
    print(f"Invalid date format: {d} (expected YYYY-MM-DD or YYYYMMDD)", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询同花顺全板块K线-按日期范围")
    parser.add_argument("--start-date", default=None, help="起始日期（YYYY-MM-DD 或 YYYYMMDD）")
    parser.add_argument("--end-date", default=None, help="截止日期（YYYY-MM-DD 或 YYYYMMDD）")
    parser.add_argument("--page", type=int, default=1, help="页码，默认 1")
    parser.add_argument("--page-size", type=int, default=50, help="每页数量，默认 50")
    args = parser.parse_args()

    params = {"page": args.page, "page_size": args.page_size}
    start = _normalize_date(args.start_date) if args.start_date else None
    end = _normalize_date(args.end_date) if args.end_date else None
    if start:
        params["start_date"] = start
    if end:
        params["end_date"] = end

    qs = urllib.parse.urlencode(params)
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    url = f"{BASE_URL}{ENDPOINT}?{qs}"
    req = urllib.request.Request(url, headers={"FTSHARE_API_KEY": key, "Content-Type": "application/json"}, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500] if e.fp else ""
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
