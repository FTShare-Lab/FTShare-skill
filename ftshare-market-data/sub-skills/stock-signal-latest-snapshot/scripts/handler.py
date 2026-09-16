#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL = os.environ.get("FTSHARE_BASE_URL", "https://market.ft.tech/gateway").rstrip("/")
_REQUEST_HEADERS = {"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type": "application/json"} if os.environ.get("FTSHARE_API_KEY") else {}
ENDPOINT = "/api/v3/market/data/stock-signal-latest-snapshot"
TYPES = {"new_high_month","new_high_60d","new_high_120d","new_high_250d","new_low_month","new_low_60d","new_low_120d","new_low_250d","consecutive_up","consecutive_down","consecutive_vol_up","consecutive_vol_down","break_up_ma5","break_up_ma10","break_up_ma20","break_down_ma5","break_down_ma10","break_down_ma20","vol_price_rise","vol_price_fall"}
def fetch(params):
    if not os.environ.get("FTSHARE_API_KEY"): print("FTSHARE_API_KEY environment variable is required", file=sys.stderr); raise SystemExit(2)
    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    p, b = urllib.parse.urlparse(url), urllib.parse.urlparse(BASE_URL)
    if (p.scheme, p.netloc) != (b.scheme, b.netloc): print("Invalid URL for safe_urlopen", file=sys.stderr); raise SystemExit(1)
    req = urllib.request.Request(url, headers={"FTSHARE_API_KEY": os.environ["FTSHARE_API_KEY"], "Content-Type":"application/json"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError) as e: print(f"请求失败: {e}", file=sys.stderr); raise SystemExit(1)
def main():
    p=argparse.ArgumentParser(); p.add_argument("--signal-type", choices=sorted(TYPES)); p.add_argument("--page",type=int,default=1); p.add_argument("--page-size",type=int,default=50); p.add_argument("--all",action="store_true",dest="fetch_all"); a=p.parse_args()
    if not 1 <= a.page_size <= 200: p.error("page-size 须在 1～200 之间")
    base={"signal_type":a.signal_type} if a.signal_type else {}
    result=fetch({**base,"page":1 if a.fetch_all else a.page,"page_size":a.page_size})
    if a.fetch_all:
        d=result.get("data") or {}; records=list(d.get("records",[]))
        for page in range(2,int(d.get("pages",1))+1): records.extend((fetch({**base,"page":page,"page_size":a.page_size}).get("data") or {}).get("records",[]))
        result["data"]={**d,"records":records}
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__ == "__main__": main()
