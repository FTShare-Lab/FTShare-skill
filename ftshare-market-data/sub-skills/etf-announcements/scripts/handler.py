#!/usr/bin/env python3
"""ETF 公告列表（GET /api/v2/market/data/announcements/etf-announcements）"""
import argparse
import json
import re
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
ENDPOINT = "/api/v2/market/data/announcements/etf-announcements"
DOWNLOAD_ENDPOINT = "/api/v2/market/data/announcements/etf-announcements/{url_hash}"

HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def safe_urlopen(req_or_url, timeout=30):
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
    return SAFE_URLOPENER.open(req_or_url, timeout=timeout)


def _validate_url_hash(value):
    if re.fullmatch(r"[A-Za-z0-9_-]+", value) is None:
        print(f"url_hash 含非法字符: {value}", file=sys.stderr)
        raise SystemExit(2)
    return value


def _safe_output_path(output):
    root = os.path.realpath(os.getcwd())
    target = os.path.realpath(os.path.join(root, output))
    if target == root or not target.startswith(root + os.sep):
        print(f"输出路径必须位于当前工作目录内: {output}", file=sys.stderr)
        raise SystemExit(2)
    return target


def _unlink(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


def download_pdf(url_hash, output):
    url = BASE_URL + DOWNLOAD_ENDPOINT.format(url_hash=urllib.parse.quote(url_hash, safe=""))
    target = _safe_output_path(output)
    part = target + ".part"
    base = urllib.parse.urlparse(BASE_URL)
    request = urllib.request.Request(
        url,
        headers={"FTSHARE_API_KEY": _require_api_key(), "X-Client-Name": "ft-claw"},
        method="GET",
    )
    try:
        with safe_urlopen(request, timeout=60) as response:
            final = urllib.parse.urlparse(response.geturl())
            if final.scheme != base.scheme or final.netloc != base.netloc:
                print(f"响应地址跳出基础地址，已中止: {response.geturl()}", file=sys.stderr)
                raise SystemExit(1)
            with open(part, "wb") as handle:
                while True:
                    block = response.read(65536)
                    if not block:
                        break
                    handle.write(block)
    except urllib.error.HTTPError as error:
        _unlink(part)
        print(f"HTTP {error.code}: {error.read().decode(errors='replace')}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        _unlink(part)
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)
    except BaseException:
        _unlink(part)
        raise
    os.replace(part, target)
    print(target)
    return target


def build_params(args):
    params = {"page": args.page, "page_size": args.page_size}
    if args.etf_code is not None:
        params["etf_code"] = args.etf_code
    if args.start_date is not None:
        params["start_date"] = args.start_date
        params["end_date"] = args.end_date or args.start_date
    elif args.end_date is not None:
        params["end_date"] = args.end_date
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
    parser = argparse.ArgumentParser(
        description="ETF 公告列表：按标的（--etf-code）或按单日日期（--start-date）查询；按 --url-hash 下载公告正文 PDF"
    )
    parser.add_argument("--etf-code", dest="etf_code", default=None,
                        help="ETF 代码，支持裸代码/短后缀/长后缀，如 159915、159915.SZ、510300.XSHG")
    parser.add_argument("--start-date", dest="start_date", default=None,
                        help="日期 YYYYMMDD（按日期查询时必填，仅支持单日）")
    parser.add_argument("--end-date", dest="end_date", default=None,
                        help="日期 YYYYMMDD；不填默认等于 start_date，且必须等于 start_date")
    parser.add_argument("--page", type=int, default=None, help="页码（列表模式必填）")
    parser.add_argument("--page-size", dest="page_size", type=int, default=None, help="每页条数（列表模式必填）")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    parser.add_argument("--url-hash", dest="url_hash", default=None,
                        help="公告文件 URL 哈希，取自列表响应；传入即下载正文 PDF")
    parser.add_argument("--output", default=None, help="下载落盘路径，默认 <url_hash>.pdf，必须在当前工作目录内")
    args = parser.parse_args()

    if args.url_hash is not None:
        _validate_url_hash(args.url_hash)
        download_pdf(args.url_hash, args.output or f"{args.url_hash}.pdf")
        return

    if args.page is None or args.page_size is None:
        parser.error("列表模式必须提供 --page 与 --page-size")
    if args.etf_code is None and args.start_date is None:
        print("必须提供 --etf-code（按标的查）或 --start-date（按日期查）", file=sys.stderr)
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
