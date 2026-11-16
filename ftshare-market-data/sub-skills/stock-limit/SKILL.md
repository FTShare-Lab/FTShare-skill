---
name: stock-limit
description: "查询每个标的每个交易日的昨收、涨停价、跌停价：可按交易日查全市场或单票，也可按标的分页查询历史区间。用户问涨跌停价、涨停/跌停幅度或某日全市场涨跌停价时使用。"
---

# 涨跌停价

接口：GET `/api/v1/market/data/stk-limit`。参数和响应以 [《涨跌停价》](https://market.ft.tech/gateway/doc/pages/vh0xsf7t.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--instrument_type` | 否 | 标的类型过滤：stock / etf / cb |
| `--symbol` | 否 | 证券代码，支持 000001.SZ / 000001.XSHE / 600519.SH 等格式；不传标的参数时按交易日返回全市场结果。区间查询时需提供该字段，或改用 symbol_id + market_id |
| `--trade_date` | 否 | 单日交易日 YYYYMMDD；不传时默认使用上一交易日。不传标的参数时查询该日全市场结果 |
| `--start_date` | 否 | 历史区间起始日 YYYYMMDD；需与 end_date 同时提供，且区间查询必须指定标的 |
| `--end_date` | 否 | 历史区间结束日 YYYYMMDD；需与 start_date 同时提供，且不能与 trade_date 混用 |
| `--page` | 否 | 页码，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 500 |

## 返回

- 记录容器：`data.items`
- 分页字段：`total_items`、`total_pages`、`total_pages`、`page_size`、`total_pages`、`page_size`（`total_pages` 依赖 `page_size`）
- 记录字段：`trade_date`、`ts_code`、`instrument_type`、`pre_close`、`up_limit`、`down_limit`

## 调用示例

```bash
python <RUN_PY> stock-limit --symbol 600519.SH --page 1
python <RUN_PY> stock-limit --trade_date 20260911 --page 1 --page_size 100
```

`--symbol` 可选：不传标的参数时按 `--trade_date` 返回全市场当日涨跌停截面（配合分页）；传入 `--symbol` 时查单标的单日或历史区间。
