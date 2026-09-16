---
name: convertible-bond-szse-matching-trades
description: 深交所可转债匹配成交。调用 /api/v1/market/data/convertible-bond/szse/matching-trades，所有请求必须设置 FTSHARE_API_KEY。
---

# 深交所可转债匹配成交

外部接口：`GET /api/v1/market/data/convertible-bond/szse/matching-trades`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> convertible-bond-szse-matching-trades --page 1 --page-size 5
```
