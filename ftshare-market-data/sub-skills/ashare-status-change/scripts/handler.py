#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL=os.environ.get("FTSHARE_BASE_URL","https://market.ft.tech/gateway").rstrip("/"); ENDPOINT="/api/v1/market/data/stk-status-change"
_REQUEST_HEADERS={"Content-Type":"application/json"}
def safe_urlopen(request):
 url=request.full_url if isinstance(request,urllib.request.Request) else str(request)
 parsed=urllib.parse.urlparse(url); base=urllib.parse.urlparse(BASE_URL)
 if (parsed.scheme,parsed.netloc)!=(base.scheme,base.netloc): print("Invalid URL for safe_urlopen",file=sys.stderr); raise SystemExit(1)
 if not isinstance(request,urllib.request.Request): request=urllib.request.Request(url,headers=_REQUEST_HEADERS,method="GET")
 return urllib.request.urlopen(request,timeout=30)
def fetch(params):
 key=os.environ.get("FTSHARE_API_KEY")
 if not key: print("FTSHARE_API_KEY environment variable is required",file=sys.stderr); raise SystemExit(2)
 url=BASE_URL+ENDPOINT+"?"+urllib.parse.urlencode(params); b,p=urllib.parse.urlparse(BASE_URL),urllib.parse.urlparse(url)
 if (b.scheme,b.netloc)!=(p.scheme,p.netloc): print("Invalid URL for safe_urlopen",file=sys.stderr); raise SystemExit(1)
 try:
  with safe_urlopen(urllib.request.Request(url,headers={"FTSHARE_API_KEY":key,"Content-Type":"application/json"},method="GET")) as r:return json.loads(r.read().decode())
 except urllib.error.HTTPError as e: print(f"HTTP {e.code}: {e.read().decode()}",file=sys.stderr); raise SystemExit(1)
 except urllib.error.URLError as e: print(f"请求失败: {e.reason}",file=sys.stderr); raise SystemExit(1)
def main():
 p=argparse.ArgumentParser(description="查询 A 股状态变更"); p.add_argument("--trade-code"); p.add_argument("--change-date"); p.add_argument("--change-type"); a=p.parse_args()
 params={k:v for k,v in (("trade_code",a.trade_code),("change_date",a.change_date),("change_type",a.change_type)) if v is not None}
 print(json.dumps(fetch(params),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
