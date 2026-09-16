#!/usr/bin/env python3
"""查询同花顺板块列表（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.request
import os

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}


def main():
    parser = argparse.ArgumentParser(description="查询同花顺板块列表")
    parser.add_argument("--module", choices=["concept", "csrc", "industry", "region"],
                        help="板块类型过滤：concept/csrc/industry/region")
    parser.add_argument("--search", default=None, help="搜索板块名称或代码")
    args = parser.parse_args()

    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    url = f"{BASE_URL}/api/v1/market/data/ths-board-list"
    req = urllib.request.Request(url, headers={**_REQUEST_HEADERS, "FTSHARE_API_KEY": key}, method="GET")

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

    if not isinstance(data, dict) or not isinstance(data.get("data"), list):
        print("Unexpected response format", file=sys.stderr)
        sys.exit(1)

    rows = data["data"]
    if args.module:
        rows = [b for b in rows if b.get("module") == args.module]

    if args.search:
        q = args.search.lower()
        rows = [b for b in rows if q in b.get("name", "").lower() or q in b.get("code", "")]

    data["data"] = rows
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
