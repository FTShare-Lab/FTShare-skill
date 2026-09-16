---
name: futures-warehouse-receipt
description: 期货仓单日报。调用 /api/v1/market/data/futures/fut-wsr，所有请求必须设置 FTSHARE_API_KEY。
---

# 期货仓单日报

外部接口：`GET /api/v1/market/data/futures/fut-wsr`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> futures-warehouse-receipt --symbol CU --trade-date 20260721 --page 1 --page-size 5
```
