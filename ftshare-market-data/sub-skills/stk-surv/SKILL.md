---
name: stk-surv
description: "查询 A 股个股严重异常波动记录，返回证券、市场、异常原因和异常期间。接口：GET /api/v2/market/data/stk-surv。同义：打板。"
---

# 个股严重异常波动

接口：GET `/api/v2/market/data/stk-surv`。参数和响应以 [《个股严重异常波动》](https://market.ft.tech/gateway/doc/pages/hflud05f.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--ts_code` | 否 | 股票代码，精确匹配，例如 `001896.SZ`。 |
| `--trade_date` | 否 | 单个交易日，格式 `YYYYMMDD`。 |
| `--start_date` | 否 | 区间起始日期，格式 `YYYYMMDD`，需与 `end_date` 一起传入。 |
| `--end_date` | 否 | 区间结束日期，格式 `YYYYMMDD`，需与 `start_date` 一起传入。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page_size` | 否 | 每页数量，默认 `100`，范围 `1`–`1000`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`ts_code`、`trade_date`、`name`、`trade_market`、`reason`、`period`

## 调用示例

```bash
python <RUN_PY> stk-surv --page 1 --trade_date 20260828
```
