---
name: stock-dividends
description: "获取 A 股分红记录（派息、送股、转增）分页视图；可按标的和公告日期范围筛选。接口：GET /api/v1/market/data/stock-dividends。"
---

# 股票分红记录

接口：GET `/api/v1/market/data/stock-dividends`。参数和响应以 [《股票分红记录》](https://market.ft.tech/gateway/doc/pages/0fxhla7v.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 否 | 标的代码，支持带交易所后缀的股票代码 |
| `--since_date` | 否 | 开始公告日期，格式 `YYYY-MM-DD`；与 `until_date` 成对传入 |
| `--until_date` | 否 | 结束公告日期，格式 `YYYY-MM-DD`；与 `since_date` 成对传入且不得早于开始日期 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`symbol`、`ann_date`、`reporting_period`、`cash_dividend_ratio`、`bonus_issue_ratio`、`bonus_issue_from_capital_reserves_ratio`、`ex_dividend_date`、`ann_url`

## 调用示例

```bash
python <RUN_PY> stock-dividends --symbol 600519.SH --page 1
```
