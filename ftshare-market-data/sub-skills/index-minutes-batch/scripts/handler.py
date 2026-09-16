#!/usr/bin/env python3
import argparse,json,os,sys,urllib.parse,urllib.request
BASE_URL=os.environ.get("FTSHARE_BASE_URL","https://market.ft.tech/gateway").rstrip("/");_REQUEST_HEADERS={"FTSHARE_API_KEY":os.environ.get("FTSHARE_API_KEY", ""),"Content-Type":"application/json"}; ENDPOINT="/api/v2/market/data/index_minutes/batch"
def main():
 p=argparse.ArgumentParser(); p.add_argument("--symbols",required=True); p.add_argument("--since-ts-millis",required=True,type=int); p.add_argument("--until-ts-millis",required=True,type=int); p.add_argument("--interval-value",type=int,default=1); p.add_argument("--adjust-kind",choices=["None","Forward","Backward"],default="None"); p.add_argument("--limit",type=int,default=50); a=p.parse_args()
 if a.interval_value<1 or not 1<=a.limit<=1000:p.error("interval-value 须大于 0，limit 须在 1～1000 之间")
 key=os.environ.get("FTSHARE_API_KEY")
 if not key: print("FTSHARE_API_KEY environment variable is required",file=sys.stderr); raise SystemExit(2)
 params=[("symbols",s.strip()) for s in a.symbols.split(",") if s.strip()]+[("since_ts_millis",a.since_ts_millis),("until_ts_millis",a.until_ts_millis),("interval_value",a.interval_value),("limit",a.limit)]
 if a.adjust_kind!="None":params.append(("adjust_kind",a.adjust_kind))
 req=urllib.request.Request(BASE_URL+ENDPOINT+"?"+urllib.parse.urlencode(params),headers={"FTSHARE_API_KEY":key,"Content-Type":"application/json"},method="GET")
 try:
  with urllib.request.urlopen(req,timeout=30) as r: print(json.dumps(json.loads(r.read().decode()),ensure_ascii=False,indent=2))
 except Exception as e: print(f"请求失败: {e}",file=sys.stderr); raise SystemExit(1)
if __name__=="__main__":main()
