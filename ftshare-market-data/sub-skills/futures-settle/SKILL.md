---
name: futures-settle
description: 期货每日结算参数。调用 /api/v1/market/data/futures/fut-settle，所有请求必须设置 FTSHARE_API_KEY。
---

# 期货每日结算参数

外部接口：`GET /api/v1/market/data/futures/fut-settle`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。`--exchange` 必填（`SHFE`/`INE`/`CZCE`/`CFFEX`/`DCE`/`GFEX`）；`--trade-date` 与 `--start-date`/`--end-date` 二选一，区间跨度不超过 31 天。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> futures-settle --exchange DCE --ts-code A2609.DCE --trade-date 20260721 --page 1 --page-size 5
```
