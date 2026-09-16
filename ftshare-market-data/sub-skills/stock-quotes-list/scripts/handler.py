#!/usr/bin/env python3
"""查询 A 股行情列表（分页，daec stocks）"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from http.client import IncompleteRead
from typing import Optional
import os
SAFE_URLOPENER = urllib.request.build_opener()

def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


BEIJING_TZ = timezone(timedelta(hours=8))

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v1/market/data/daec/stocks"

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

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def build_params(order_by=None, ob=None, filter_=None, masks=None, page_size=None, page_no=None, filter_index=None):
    """构造 daec 分页列表查询参数。

    关键映射：v2 的 `page_no` → daec 的 `page`（daec 忽略 page_no，不转则永远返回第一页）；
    `ob` 作为 `order_by` 的别名。注：daec 当前忽略 masks（返回全字段）。
    """
    params = {}
    sort = order_by if order_by else ob
    if sort:
        params["order_by"] = sort
    if filter_:
        params["filter"] = filter_
    if masks:
        params["masks"] = masks
    if page_size is not None:
        params["page_size"] = page_size
    if page_no is not None:
        params["page"] = page_no  # v2 page_no → daec page
    if filter_index is not None:
        params["filter_index"] = filter_index
    return params


MAX_RETRIES = 5
_SLEEP_BASE = 0.3  # 指数退避基准秒


def _get_json(url: str):
    """发起 GET 并解析 JSON。daec 大响应偶发截断，对传输类错误重试。"""
    last_exc = None
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers={**HEADERS, **_REQUEST_HEADERS})
        try:
            with safe_urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"HTTP {e.code}: {body}", file=sys.stderr)
            sys.exit(1)
        except (IncompleteRead, OSError) as e:
            last_exc = e
            if attempt < MAX_RETRIES - 1:
                time.sleep(_SLEEP_BASE * (2 ** attempt))
    print(f"请求失败（重试 {MAX_RETRIES} 次仍截断或网络错误）: {last_exc}", file=sys.stderr)
    sys.exit(1)


def fetch(
order_by=None, ob=None, filter_=None, masks=None, page_size=None, page_no=None, filter_index=None):
    params = build_params(order_by, ob, filter_, masks, page_size, page_no, filter_index)
    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = _get_json(url)
    # items 每条的交易所时间戳 ts_millis（毫秒）转为北京时间 ISO 字符串
    for item in data.get("items", []):
        if isinstance(item, dict) and "ts_millis" in item:
            item["ts_millis"] = ms_to_iso(item["ts_millis"])
    return data


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询 A 股行情列表（分页，daec）")
    parser.add_argument("--order_by", required=True, help='排序规则，如 change_rate desc')
    parser.add_argument("--page_no", type=int, required=True, help="页码，从 1 开始")
    parser.add_argument("--page_size", type=int, required=True, help="每页记录数")
    parser.add_argument("--filter", default="", help="筛选条件表达式，可选")
    parser.add_argument("--masks", default="", help="返回字段掩码（daec 当前忽略，返回全字段）")
    args = parser.parse_args()

    result = fetch(
        order_by=args.order_by,
        filter_=args.filter,
        masks=args.masks,
        page_size=args.page_size,
        page_no=args.page_no,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
