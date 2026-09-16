#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = "/api/v1/market/data/holder/stock-ggcg-em"
_REQUEST_HEADERS = {"Content-Type": "application/json"}
def safe_urlopen(request):
    url = request.full_url if isinstance(request, urllib.request.Request) else str(request)
    b, p = urllib.parse.urlparse(BASE_URL), urllib.parse.urlparse(url)
    if (b.scheme, b.netloc) != (p.scheme, p.netloc): print("Invalid URL for safe_urlopen", file=sys.stderr); raise SystemExit(1)
    if not isinstance(request, urllib.request.Request): request = urllib.request.Request(url, headers=_REQUEST_HEADERS, method="GET")
    return urllib.request.urlopen(request, timeout=30)

def fetch(params):
    key = os.environ.get("FTSHARE_API_KEY")
    if not key: print("FTSHARE_API_KEY environment variable is required", file=sys.stderr); raise SystemExit(2)
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    b, p = urllib.parse.urlparse(BASE_URL), urllib.parse.urlparse(url)
    if (b.scheme, b.netloc) != (p.scheme, p.netloc): print("Invalid URL for safe_urlopen", file=sys.stderr); raise SystemExit(1)
    req = urllib.request.Request(url, headers={"FTSHARE_API_KEY": key, "Content-Type": "application/json"}, method="GET")
    try:
        with safe_urlopen(req) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e: print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr); raise SystemExit(1)
    except urllib.error.URLError as e: print(f"请求失败: {e.reason}", file=sys.stderr); raise SystemExit(1)
def main():
    p=argparse.ArgumentParser(description="查询东方财富股东增减持"); p.add_argument("--symbol", default="全部"); p.add_argument("--page", type=int, default=1); p.add_argument("--page-size", dest="page_size", type=int, default=50); p.add_argument("--all", action="store_true", dest="fetch_all"); a=p.parse_args()
    if a.symbol not in ("全部", "股东增持", "股东减持"): p.error("symbol 仅支持 全部、股东增持、股东减持")
    if a.page < 1 or not 1 <= a.page_size <= 200: p.error("page 须大于等于 1，page-size 须在 1～200 之间")
    params={"symbol":a.symbol,"page":1 if a.fetch_all else a.page,"page_size":a.page_size}; result=fetch(params)
    if a.fetch_all:
        data=result.get("data") or {}; records=list(data.get("records", []))
        for page in range(2,int(data.get("pages",1))+1): records.extend((fetch({**params,"page":page}).get("data") or {}).get("records", []))
        result["data"]={**data,"records":records}
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == "__main__": main()
