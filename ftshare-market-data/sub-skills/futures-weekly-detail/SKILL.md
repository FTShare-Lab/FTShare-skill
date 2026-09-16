---
name: futures-weekly-detail
description: 期货主要品种交易周报。调用 /api/v1/market/data/futures/fut-weekly-detail，所有请求必须设置 FTSHARE_API_KEY。
---

# 期货主要品种交易周报

外部接口：`GET /api/v1/market/data/futures/fut-weekly-detail`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> futures-weekly-detail --week 202628 --prd CU,AL --page 1 --page-size 5
```
