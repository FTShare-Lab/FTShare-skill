---
name: cashflow-stock-code
description: "获取所有有现金流量表数据的股票代码与名称列表，不分页，一次返回全量。接口：GET /api/v2/market/data/finance/cashflow-stock-code。"
---

# 现金流支持股票代码

接口：GET `/api/v2/market/data/finance/cashflow-stock-code`。参数和响应以 [《现金流支持股票代码》](https://market.ft.tech/gateway/doc/pages/skukfb13.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

无需请求参数。

## 返回

- 记录容器：`data.items`
- 记录字段：`stock_code`、`stock_name`

## 调用示例

```bash
python <RUN_PY> cashflow-stock-code
```
