---
name: supply-chain-industry-names
description: "查询供应链行业名称全集。接口：GET /api/v3/market/data/supply-chain/industry-names。"
---

# 供应链行业名称

接口：GET `/api/v3/market/data/supply-chain/industry-names`。参数和响应以 [《供应链行业名称》](https://market.ft.tech/gateway/doc/pages/z5k1xvhk.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

无需请求参数。

## 返回

- 字段以在线文档为准。

## 调用示例

```bash
python <RUN_PY> supply-chain-industry-names
```
