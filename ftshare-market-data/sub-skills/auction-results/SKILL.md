---
name: auction-results
description: "返回当日所有股票的盘前集合竞价结果（9:25 开盘集合竞价快照）：集合竞价开盘价/收盘价（最新价）、最高价、最低价、成交量、成交额、均价（vwap）。接口：GET /api/v2/market/data/auction-results。"
---

# 集合竞价结果

接口：GET `/api/v2/market/data/auction-results`。参数和响应以 [《集合竞价结果》](https://market.ft.tech/gateway/doc/pages/z7n8ucgi.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--ts_code` | 否 | 股票代码，如 000001.XSHE |
| `--trade_date` | 否 | 交易日，格式 YYYYMMDD |
| `--start_date` | 否 | 起始日期，格式 YYYYMMDD |
| `--end_date` | 否 | 结束日期，格式 YYYYMMDD |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`symbol`、`close`、`open`、`high`、`low`、`volume`、`amount`、`vwap`

## 调用示例

```bash
python <RUN_PY> auction-results --ts_code 600519.SH --page 1
```
