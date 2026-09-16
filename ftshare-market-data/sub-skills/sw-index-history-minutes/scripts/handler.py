#!/usr/bin/env python3
import argparse,json,os,sys,urllib.parse,urllib.request
BASE_URL=os.environ.get("FTSHARE_BASE_URL","https://market.ft.tech/gateway").rstrip("/");_REQUEST_HEADERS={"FTSHARE_API_KEY":os.environ.get("FTSHARE_API_KEY", ""),"Content-Type":"application/json"}; ENDPOINT="/api/v1/market/data/sw-index/history-minutes"
def fetch(params):
 key=os.environ.get("FTSHARE_API_KEY")
 if not key: print("FTSHARE_API_KEY environment variable is required",file=sys.stderr);raise SystemExit(2)
 url=BASE_URL+ENDPOINT+"?"+urllib.parse.urlencode(params); p,b=urllib.parse.urlparse(url),urllib.parse.urlparse(BASE_URL)
 if (p.scheme,p.netloc)!=(b.scheme,b.netloc):print("Invalid URL for safe_urlopen",file=sys.stderr);raise SystemExit(1)
 with urllib.request.urlopen(urllib.request.Request(url,headers={"FTSHARE_API_KEY":key,"Content-Type":"application/json"},method="GET"),timeout=30) as r:return json.loads(r.read().decode())
def main():
 p=argparse.ArgumentParser();p.add_argument("--index-code",required=True);p.add_argument("--start-date",required=True);p.add_argument("--end-date",required=True);p.add_argument("--page",type=int,default=1);p.add_argument("--page-size",type=int,default=50);p.add_argument("--all",action="store_true",dest="fetch_all");a=p.parse_args()
 if not 1<=a.page_size<=200:p.error("page-size 须在 1～200 之间")
 base={"index_code":a.index_code,"start_date":a.start_date,"end_date":a.end_date};result=fetch({**base,"page":1 if a.fetch_all else a.page,"page_size":a.page_size})
 if a.fetch_all:
  d=result.get("data") or {};records=list(d.get("records",[]))
  for page in range(2,int(d.get("pages",1))+1):records.extend((fetch({**base,"page":page,"page_size":a.page_size}).get("data")or{}).get("records",[]))
  result["data"]={**d,"records":records}
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
