---
name: limit-list
description: "统一查询涨停、跌停或炸板股票池。可用参数：--limit_type、--trade_date。接口：GET /api/v1/market/data/limit-list。同义：打板。"
---

# 涨跌停池

接口：GET `/api/v1/market/data/limit-list`。参数和响应以 [《涨跌停池》](https://market.ft.tech/gateway/doc/pages/qt0y1loe.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--limit_type` | 是 | 股票池类型：`up` 涨停池、`down` 跌停池、`up_break` 炸板池。 |
| `--trade_date` | 否 | 交易日期，格式 `YYYYMMDD`；不传或传入当日时查询实时数据。 |

## 返回

- 记录字段：`symbol`、`trade_date`、`ready`、`status`、`limit_up_price`、`limit_down_price`、`limit_up_enter`、`limit_up_break`、`limit_down_enter`、`limit_down_break`、`first_limit_up_time`、`limit_up_break_count`、`last_limit_down_time`、`limit_down_break_count`、`limit_up_seal_value`、`limit_down_seal_value`

## 调用示例

```bash
python <RUN_PY> limit-list --limit_type up --trade_date 20260828
```
