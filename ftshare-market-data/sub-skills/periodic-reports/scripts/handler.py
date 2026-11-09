#!/usr/bin/env python3
"""查询上市公司定期报告列表，或按 url_hash 下载报告原文 PDF。

- 列表模式：stock_code / report_type / report_year / document_variant 均可选，分页返回。
- 下载模式：传 --url-hash 时下载对应报告 PDF 到本地。
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v2/market/data/announcements/periodic-reports"
DOWNLOAD_ENDPOINT = "/api/v2/market/data/announcements/periodic-reports/{url_hash}"
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 500
REPORT_TYPES = ["annual", "semi_annual", "q1", "q3"]
DOCUMENT_VARIANTS = ["full", "summary", "english"]


def _require_api_key():
    key = os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr)
        raise SystemExit(2)
    return key


def safe_urlopen(req_or_url, timeout=30):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    base = urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(req_or_url, urllib.request.Request):
        req_or_url = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    for key, value in _REQUEST_HEADERS.items():
        req_or_url.add_unredirected_header(key, value)
    return SAFE_URLOPENER.open(req_or_url, timeout=timeout)


def _validate_url_hash(value):
    if re.fullmatch(r"[0-9a-f]{64}", value) is None:
        print(f"url_hash 须为 64 位小写十六进制: {value}", file=sys.stderr)
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
    for name in ("stock_code", "report_type", "report_year", "document_variant"):
        value = getattr(args, name)
        if value is not None:
            params[name] = value
    return params


def fetch_page(params):
    request = urllib.request.Request(
        BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params),
        headers={**_REQUEST_HEADERS, "X-Client-Name": "ft-claw"},
        method="GET",
    )
    try:
        with safe_urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    _require_api_key()
    parser = argparse.ArgumentParser(description="查询定期报告列表，或按 url_hash 下载报告原文 PDF")
    parser.add_argument("--stock-code", dest="stock_code", default=None,
                        help="股票代码，支持裸代码/短后缀/长后缀（不支持冒号格式）")
    parser.add_argument("--report-type", dest="report_type", choices=REPORT_TYPES, default=None,
                        help="报告类型：annual / semi_annual / q1 / q3；不传返回全部四类")
    parser.add_argument("--report-year", dest="report_year", type=int, default=None,
                        help="报告年份，如 2025")
    parser.add_argument("--document-variant", dest="document_variant", choices=DOCUMENT_VARIANTS, default=None,
                        help="文件版本类型：full / summary / english；当前数据均为 full")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", dest="page_size", type=int, default=DEFAULT_PAGE_SIZE,
                        help=f"每页条数，默认 {DEFAULT_PAGE_SIZE}，最大 {MAX_PAGE_SIZE}")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    parser.add_argument("--url-hash", dest="url_hash", default=None, help="报告文件哈希；传入即下载 PDF")
    parser.add_argument("--output", default=None, help="落盘路径，默认 <url_hash>.pdf；必须在当前工作目录内")
    args = parser.parse_args()

    if args.url_hash is not None:
        _validate_url_hash(args.url_hash)
        download_pdf(args.url_hash, args.output or f"{args.url_hash}.pdf")
        return

    if args.page < 1:
        print("--page 须大于等于 1", file=sys.stderr)
        raise SystemExit(2)
    if not 1 <= args.page_size <= MAX_PAGE_SIZE:
        print(f"--page-size 须在 1～{MAX_PAGE_SIZE} 之间", file=sys.stderr)
        raise SystemExit(2)
    if args.report_year is not None and not 0 <= args.report_year <= 65535:
        print("--report-year 须在 0～65535 之间", file=sys.stderr)
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
