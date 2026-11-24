#!/usr/bin/env python3
"""板块洞察检索（GET /api/v3/market/data/sector-knowledge/insights）"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v3/market/data/sector-knowledge/insights"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}

DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200
SORT_VALUES = ("relevance", "latest", "influence", "confidence")
SECTOR_TYPES = ("industry", "concept", "region", "index_style", "macro_asset")
MARKETS = ("CN", "US", "HK", "KR", "JP", "global")


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
    return SAFE_URLOPENER.open(request, timeout=timeout)


def _parse_date(value, flag):
    try:
        return datetime.strptime(value, "%Y%m%d")
    except ValueError:
        print(f"{flag} 必须为 YYYYMMDD 格式", file=sys.stderr)
        raise SystemExit(2)


def _parse_int(value, flag):
    try:
        return int(value)
    except (TypeError, ValueError):
        print(f"{flag} 必须为整数", file=sys.stderr)
        raise SystemExit(2)


def _parse_float(value, flag):
    try:
        return float(value)
    except (TypeError, ValueError):
        print(f"{flag} 必须为数值", file=sys.stderr)
        raise SystemExit(2)


def build_params(args):
    params = {}
    if args.sector_name is not None:
        params["sector_name"] = args.sector_name
    if args.sector_type is not None:
        params["sector_type"] = args.sector_type
    if args.market is not None:
        params["market"] = args.market
    if args.keyword is not None:
        params["keyword"] = args.keyword
    if args.keyword_expression is not None:
        params["keyword_expression"] = args.keyword_expression
    if args.insight_category:
        params["insight_category"] = args.insight_category
    if args.start_date is not None:
        params["start_date"] = args.start_date
    if args.end_date is not None:
        params["end_date"] = args.end_date
    if args.min_influence_score is not None:
        params["min_influence_score"] = args.min_influence_score
    if args.min_confidence is not None:
        params["min_confidence"] = args.min_confidence
    if args.sort is not None:
        params["sort"] = args.sort
    params["page"] = args.page
    params["page_size"] = args.page_size
    return params


def fetch_page(params):
    query = urllib.parse.urlencode(params, doseq=True)
    request = urllib.request.Request(
        f"{BASE_URL}{ENDPOINT}?{query}",
        headers={**HEADERS, **_REQUEST_HEADERS},
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
    _require_api_key()
    parser = argparse.ArgumentParser(description="板块洞察检索：按板块、分类、日期、影响力、置信度等条件检索板块洞察")
    parser.add_argument("--sector-name", dest="sector_name", default=None, help="板块标准名称，精确匹配，如 A股半导体")
    parser.add_argument("--sector-type", dest="sector_type", default=None, help="板块类型：industry/concept/region/index_style/macro_asset")
    parser.add_argument("--market", default=None, help="市场：CN/US/HK/KR/JP/global")
    parser.add_argument("--keyword", default=None, help="关键词子串匹配 title、summary，最长 200 字符；与 --keyword-expression 互斥")
    parser.add_argument("--keyword-expression", dest="keyword_expression", default=None, help="布尔表达式，支持 AND/OR/括号；与 --keyword 互斥")
    parser.add_argument("--insight-category", dest="insight_category", action="append", default=None, help="板块洞察分类，可重复传入；同维度多值为 OR")
    parser.add_argument("--start-date", dest="start_date", default=None, help="板块洞察生成日期下界 YYYYMMDD")
    parser.add_argument("--end-date", dest="end_date", default=None, help="板块洞察生成日期上界 YYYYMMDD")
    parser.add_argument("--min-influence-score", dest="min_influence_score", default=None, help="最低影响力，0~100")
    parser.add_argument("--min-confidence", dest="min_confidence", default=None, help="最低置信度，0~1；使用时必须提供 --sector-name")
    parser.add_argument("--sort", default=None, help="relevance/latest/influence/confidence，默认 relevance")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1，最大 1000")
    parser.add_argument("--page-size", dest="page_size", type=int, default=DEFAULT_PAGE_SIZE,
                        help=f"每页条数，默认 {DEFAULT_PAGE_SIZE}，最大 {MAX_PAGE_SIZE}")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    if args.keyword is not None and args.keyword_expression is not None:
        print("--keyword 与 --keyword-expression 不能同时传入", file=sys.stderr)
        raise SystemExit(2)
    if (args.keyword is not None or args.keyword_expression is not None or args.min_confidence is not None) and args.sector_name is None:
        print("使用 --keyword、--keyword-expression 或 --min-confidence 时必须提供 --sector-name", file=sys.stderr)
        raise SystemExit(2)
    if not 1 <= args.page <= 1000:
        print("--page 须在 1~1000 之间", file=sys.stderr)
        raise SystemExit(2)
    if not 1 <= args.page_size <= MAX_PAGE_SIZE:
        print(f"--page-size 须在 1~{MAX_PAGE_SIZE} 之间", file=sys.stderr)
        raise SystemExit(2)
    if args.sector_type is not None and args.sector_type not in SECTOR_TYPES:
        print(f"--sector-type 取值须为 {'/'.join(SECTOR_TYPES)}", file=sys.stderr)
        raise SystemExit(2)
    if args.market is not None and args.market not in MARKETS:
        print(f"--market 取值须为 {'/'.join(MARKETS)}", file=sys.stderr)
        raise SystemExit(2)
    if args.sort is not None and args.sort not in SORT_VALUES:
        print(f"--sort 取值须为 {'/'.join(SORT_VALUES)}", file=sys.stderr)
        raise SystemExit(2)
    if args.start_date is not None:
        start = _parse_date(args.start_date, "--start-date")
        if args.end_date is not None and _parse_date(args.end_date, "--end-date") < start:
            print("--start-date 不能晚于 --end-date", file=sys.stderr)
            raise SystemExit(2)
    elif args.end_date is not None:
        _parse_date(args.end_date, "--end-date")
    if args.min_influence_score is not None and not 0 <= _parse_int(args.min_influence_score, "--min-influence-score") <= 100:
        print("--min-influence-score 须在 0~100 之间", file=sys.stderr)
        raise SystemExit(2)
    if args.min_confidence is not None and not 0 <= _parse_float(args.min_confidence, "--min-confidence") <= 1:
        print("--min-confidence 须在 0~1 之间", file=sys.stderr)
        raise SystemExit(2)
    if not any([
        args.sector_name, args.sector_type, args.market, args.keyword, args.keyword_expression,
        args.insight_category, args.start_date, args.end_date,
        args.min_influence_score, args.min_confidence,
    ]):
        print("至少需要提供一个检索条件", file=sys.stderr)
        raise SystemExit(2)

    params = build_params(args)
    if args.fetch_all:
        first = fetch_page(params)
        data = first.get("data") or {}
        records = list(data.get("records", []))
        total_pages = data.get("pages") or 1
        for page in range(2, total_pages + 1):
            page_data = fetch_page({**params, "page": page})
            records.extend((page_data.get("data") or {}).get("records", []))
        result = {
            "records": records,
            "pages": total_pages,
            "total": data.get("total", len(records)),
        }
    else:
        result = fetch_page(params)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()