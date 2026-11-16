---
name: ths-stock-daily-flow
description: "按日期范围查询同花顺个股日度资金流，返回股票代码和名称、收盘价、涨跌幅、换手率、资金流入/流出/净额及成交额。接口：GET /api/v1/market/data/ths-stock-daily-flow。"
---

# 同花顺个股资金流日度

接口：GET `/api/v1/market/data/ths-stock-daily-flow`。参数和响应以 [《同花顺个股资金流日度》](https://market.ft.tech/gateway/doc/pages/rxbypzx4.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start_date` | 是 | 开始日期，格式 YYYYMMDD |
| `--end_date` | 是 | 结束日期，格式 YYYYMMDD，不能早于 start_date |
| `--name` | 否 | 股票名称，精确匹配，不能是空白字符串 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`name`、`trade_date`、`close_price`、`change_pct`、`turnover_pct`、`inflow`、`outflow`、`net_amount`、`turnover_amount`

## 调用示例

```bash
python <RUN_PY> ths-stock-daily-flow --start_date 20260828 --end_date 20260828 --page 1
```
