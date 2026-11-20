#!/usr/bin/env python3
"""盘前数据（GET /api/v2/market/data/stk-premarket）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v2/market/data/stk-premarket"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = (
    {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"}
    if os.environ.get("FTSHARE_API_KEY")
    else {}
)


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(request, timeout=30):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed, base = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(request, urllib.request.Request):
        request = urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    request.add_unredirected_header("Content-Type", "application/json")
    return SAFE_URLOPENER.open(request, timeout=timeout)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="stk-premarket",
        description=(
            "盘前数据：每日股本（总股本 / A 股流通股本）、昨收、涨跌停价、价格与总市值 / 流通市值。"
            "支持「单日全市场」与「单票历史区间」两种查询。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "查询模式：\n"
            "  1) 单日全市场：--trade-date 20261113\n"
            "  2) 单票历史：  --ts-code 600036.SH --start-date 20250101 --end-date 20261116\n"
            "\n"
            "注意事项：\n"
            "  - 只传 --ts-code 不传区间时，仅返回该标的最新交易日 1 条；无数据标的返回空数组。\n"
            "  - 历史数据起点为 2022-01-04；更早的 --start-date 会被静默截断（不报错）。\n"
            "  - 分页默认 page=1、page_size=50，最大 500；长区间必须翻页或加 --all。\n"
            "  - 非交易日（周末 / 节假日）--trade-date 返回 200 + 空数组。\n"
            "  - 北交所代码为 92xxxx（如 920002.BJ），旧 83xxxx / 43xxxx 返回空。\n"
            "\n"
            "示例：\n"
            "  stk-premarket --ts-code 600036.SH --start-date 20250101 --end-date 20261116 --all\n"
            "  stk-premarket --trade-date 20261113 --page-size 500\n"
        ),
    )
    parser.add_argument(
        "--ts-code", "--ts_code", dest="ts_code", default=None,
        help="标的代码，如 000001.SZ / 600519.SH。只传本参数时仅返回最新交易日 1 条，查历史须配合 --start-date/--end-date",
    )
    parser.add_argument(
        "--trade-date", "--trade_date", dest="trade_date", default=None,
        help="交易日 YYYYMMDD，查询该日全市场快照；与 --start-date/--end-date 互斥。非交易日返回空数组",
    )
    parser.add_argument(
        "--start-date", "--start_date", dest="start_date", default=None,
        help="区间起始日 YYYYMMDD，必须与 --end-date 成对提供且配合 --ts-code；历史起点 2022-01-04",
    )
    parser.add_argument(
        "--end-date", "--end_date", dest="end_date", default=None,
        help="区间结束日 YYYYMMDD，必须与 --start-date 成对提供且配合 --ts-code",
    )
    parser.add_argument(
        "--page", type=int, default=1,
        help="页码，从 1 开始，默认 1",
    )
    parser.add_argument(
        "--page-size", "--page_size", dest="page_size", type=int, default=None,
        help="每页条数，1~500；默认 50，配合 --all 时默认 500",
    )
    parser.add_argument(
        "--all", action="store_true", dest="fetch_all",
        help="从第 1 页起按 total_pages 自动翻页，输出合并后的完整 items（忽略 --page；单票全历史建议使用）",
    )
    return parser


def fetch_page(params):
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        f"{BASE_URL}{ENDPOINT}?{query}",
        headers={**_REQUEST_HEADERS, "FTSHARE_API_KEY": _require_api_key(),
                 "Content-Type": "application/json", "X-Client-Name": "ft-claw"},
        method="GET",
    )
    try:
        with safe_urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


def main():
    args = build_parser().parse_args()
    _require_api_key()

    if args.page < 1:
        print("--page 必须 >= 1", file=sys.stderr)
        raise SystemExit(2)
    page_size = args.page_size if args.page_size is not None else (500 if args.fetch_all else 50)
    if not 1 <= page_size <= 500:
        print("--page-size 必须在 1~500 之间", file=sys.stderr)
        raise SystemExit(2)
    if (args.start_date is None) != (args.end_date is None):
        print("--start-date 与 --end-date 必须成对提供", file=sys.stderr)
        raise SystemExit(2)
    if args.trade_date is not None and args.start_date is not None:
        print("--trade-date 不能与 --start-date/--end-date 同时使用", file=sys.stderr)
        raise SystemExit(2)
    if args.start_date is not None and args.ts_code is None:
        print("--start-date/--end-date 需配合 --ts-code 使用", file=sys.stderr)
        raise SystemExit(2)

    params = {}
    for name in ("ts_code", "trade_date", "start_date", "end_date"):
        value = getattr(args, name)
        if value is not None:
            params[name] = value

    if not args.fetch_all:
        print(json.dumps(fetch_page({**params, "page": args.page, "page_size": page_size}),
                         ensure_ascii=False, indent=2))
        return

    first = fetch_page({**params, "page": 1, "page_size": page_size})
    data = first.get("data") or {}
    items = list(data.get("items") or [])
    total_pages = int(data.get("total_pages") or 1)
    for page in range(2, total_pages + 1):
        payload = fetch_page({**params, "page": page, "page_size": page_size})
        items.extend((payload.get("data") or {}).get("items") or [])

    print(json.dumps(
        {
            "code": first.get("code", 200),
            "message": first.get("message", "success"),
            "data": {"items": items, "total_items": len(items), "total_pages": total_pages},
        },
        ensure_ascii=False, indent=2,
    ))


if __name__ == "__main__":
    main()
