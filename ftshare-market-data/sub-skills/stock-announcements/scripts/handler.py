#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v2/market/data/announcements/stock-announcements"
DOWNLOAD_ENDPOINT = "/api/v2/market/data/announcements/stock-announcements/{url_hash}"
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}


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


def main():
    key = _require_api_key()
    parser = argparse.ArgumentParser(description="查询 A 股公告列表，或按 url_hash 下载公告正文 PDF")
    parser.add_argument("--stock-code", dest="stock_code")
    parser.add_argument("--start-date", dest="start_date")
    parser.add_argument("--end-date", dest="end_date")
    parser.add_argument("--type", default="stock")
    parser.add_argument("--page", type=int)
    parser.add_argument("--page-size", dest="page_size", type=int)
    parser.add_argument("--url-hash", dest="url_hash")
    parser.add_argument("--output")
    args = parser.parse_args()

    if args.url_hash is not None:
        _validate_url_hash(args.url_hash)
        download_pdf(args.url_hash, args.output or f"{args.url_hash}.pdf")
        return

    if args.page is None or args.page_size is None:
        parser.error("列表模式必须提供 --page 与 --page-size")
    if not args.stock_code and not args.start_date:
        parser.error("stock-code 与 start-date 至少提供一个")
    if args.type != "stock":
        parser.error("type 当前只支持 stock")
    params = {"type": args.type, "page": args.page, "page_size": args.page_size}
    for name in ("stock_code", "start_date", "end_date"):
        value = getattr(args, name)
        if value is not None:
            params[name] = value
    request = urllib.request.Request(BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params),
                                     headers={"FTSHARE_API_KEY": key, "X-Client-Name": "ft-claw", "Content-Type": "application/json"}, method="GET")
    try:
        with safe_urlopen(request) as response:
            print(json.dumps(json.loads(response.read().decode()), ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
