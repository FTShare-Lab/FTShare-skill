---
name: market-distribution-intraday
description: "获取市场涨跌分布的日内分时序列。接口：GET /api/v2/market/data/market-distribution-intraday。"
---

# 市场涨跌分布分时

接口：GET `/api/v2/market/data/market-distribution-intraday`。参数和响应以 [《市场涨跌分布分时》](https://market.ft.tech/gateway/doc/pages/c8hl03ku.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

无需请求参数。

## 返回

- 记录字段：`ts_millis`、`up_limited`、`down_limited`、`xshg`、`xshe`、`bjse`

## 调用示例

```bash
python <RUN_PY> market-distribution-intraday
```
