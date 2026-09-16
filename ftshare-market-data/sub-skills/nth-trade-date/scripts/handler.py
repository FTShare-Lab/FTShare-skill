#!/usr/bin/env python3
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request
BASE_URL=os.environ.get("FTSHARE_BASE_URL","https://market.ft.tech/gateway").rstrip("/"); ENDPOINT="/api/v1/market/data/time/get-nth-trade-date"
_REQUEST_HEADERS={"Content-Type":"application/json"}
def safe_urlopen(request):
 url=request.full_url if isinstance(request,urllib.request.Request) else str(request)
 parsed=urllib.parse.urlparse(url); base=urllib.parse.urlparse(BASE_URL)
 if (parsed.scheme,parsed.netloc)!=(base.scheme,base.netloc): print("Invalid URL for safe_urlopen",file=sys.stderr); raise SystemExit(1)
 if not isinstance(request,urllib.request.Request): request=urllib.request.Request(url,headers=_REQUEST_HEADERS,method="GET")
 return urllib.request.urlopen(request,timeout=30)
def main():
 p=argparse.ArgumentParser(description="查询第 N 个交易日"); p.add_argument("--n",type=int,required=True); a=p.parse_args()
 if a.n<1: p.error("n 必须大于等于 1")
 key=os.environ.get("FTSHARE_API_KEY")
 if not key: print("FTSHARE_API_KEY environment variable is required",file=sys.stderr); raise SystemExit(2)
 url=BASE_URL+ENDPOINT+"?"+urllib.parse.urlencode({"n":a.n}); b,purl=urllib.parse.urlparse(BASE_URL),urllib.parse.urlparse(url)
 if (b.scheme,b.netloc)!=(purl.scheme,purl.netloc): print("Invalid URL for safe_urlopen",file=sys.stderr); raise SystemExit(1)
 try:
  req=urllib.request.Request(url,headers={"FTSHARE_API_KEY":key,"Content-Type":"application/json"},method="GET")
  with safe_urlopen(req) as r: result=json.loads(r.read().decode())
 except urllib.error.HTTPError as e: print(f"HTTP {e.code}: {e.read().decode()}",file=sys.stderr); raise SystemExit(1)
 except urllib.error.URLError as e: print(f"请求失败: {e.reason}",file=sys.stderr); raise SystemExit(1)
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
