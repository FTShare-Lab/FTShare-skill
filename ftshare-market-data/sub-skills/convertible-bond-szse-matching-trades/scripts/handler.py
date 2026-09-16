#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
ENDPOINT = '/api/v1/market/data/convertible-bond/szse/matching-trades'
SAFE_URLOPENER = urllib.request.build_opener()
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
def _require_api_key():
    key=os.environ.get("FTSHARE_API_KEY")
    if not key:
        print("FTSHARE_API_KEY environment variable is required", file=sys.stderr); raise SystemExit(2)
    return key
def safe_urlopen(request, timeout=30):
    url=request.full_url if isinstance(request, urllib.request.Request) else str(request)
    parsed,base=urllib.parse.urlparse(url),urllib.parse.urlparse(BASE_URL)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr); raise SystemExit(1)
    if not isinstance(request, urllib.request.Request): request=urllib.request.Request(url, method="GET")
    request.add_unredirected_header("FTSHARE_API_KEY", _require_api_key())
    return SAFE_URLOPENER.open(request, timeout=timeout)
def main():
    key=_require_api_key(); parser=argparse.ArgumentParser(description='深交所可转债匹配成交')
    parser.add_argument("--security-code", dest="security_code")
    parser.add_argument("--trade-date", dest="trade_date", type=int)
    parser.add_argument("--page", dest="page", type=int)
    parser.add_argument("--page-size", dest="page_size", type=int)
    ns=parser.parse_args(); params={}
    for name,value in vars(ns).items():
        if value is not None: params[name.replace("_","-") if False else name]=value
    request=urllib.request.Request(BASE_URL+ENDPOINT+"?"+urllib.parse.urlencode(params), headers={"FTSHARE_API_KEY":key,"X-Client-Name":"ft-claw","Content-Type":"application/json"}, method="GET")
    try:
        with safe_urlopen(request) as response: payload=json.loads(response.read().decode())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}", file=sys.stderr); raise SystemExit(1)
    except urllib.error.URLError as error:
        print(f"请求失败: {error.reason}", file=sys.stderr); raise SystemExit(1)
if __name__ == "__main__": main()
