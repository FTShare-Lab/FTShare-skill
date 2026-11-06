#!/usr/bin/env python3
"""查询全市场上市公司公告列表，或按 url_hash 下载公告原文 PDF。

- 列表模式：keyword / category / stock_code / start_date / end_date / plate / column_type 均可选，分页返回。
- 下载模式：传 --url-hash 时下载对应公告 PDF 到本地。
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
ENDPOINT = "/api/v2/market/data/announcements/market-announcements"
DOWNLOAD_ENDPOINT = "/api/v2/market/data/announcements/market-announcements/{url_hash}"
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 500


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
    for name in ("keyword", "category", "stock_code", "start_date", "end_date", "plate", "column_type"):
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
    parser = argparse.ArgumentParser(description="查询全市场公告列表，或按 url_hash 下载公告原文 PDF")
    parser.add_argument("--keyword", default=None, help="公告标题关键字，子串匹配；去首尾空格后最长 60 字符")
    parser.add_argument("--category", default=None, help="公告分类，22 个允许值逗号分隔多选，任一命中即返回")
    parser.add_argument("--stock-code", dest="stock_code", default=None, help="股票代码，支持裸代码/短后缀/长后缀/冒号格式")
    parser.add_argument("--start-date", dest="start_date", default=None, help="起始日期 YYYYMMDD；单独提供时查询该单日")
    parser.add_argument("--end-date", dest="end_date", default=None, help="结束日期 YYYYMMDD；须与 start-date 成对使用")
    parser.add_argument("--plate", default=None, help="板块 sh / sz / sz_chi_next / sh_star / bj，逗号分隔多选")
    parser.add_argument("--column-type", dest="column_type", default=None, help="栏目 stock / hke / fund / bond，逗号分隔多选")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", dest="page_size", type=int, default=DEFAULT_PAGE_SIZE,
                        help=f"每页条数，默认 {DEFAULT_PAGE_SIZE}，最大 {MAX_PAGE_SIZE}")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    parser.add_argument("--url-hash", dest="url_hash", default=None, help="公告文件哈希；传入即下载 PDF")
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
    if args.end_date is not None and args.start_date is None:
        print("--end-date 不能单独提供，须与 --start-date 成对使用", file=sys.stderr)
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
