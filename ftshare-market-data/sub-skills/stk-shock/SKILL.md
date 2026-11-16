---
name: stk-shock
description: "查询个股异常波动及买卖营业部明细。接口：GET /api/v2/market/data/stk-shock。同义：打板。"
---

# 个股异常波动

接口：GET `/api/v2/market/data/stk-shock`。参数和响应以 [《个股异常波动》](https://market.ft.tech/gateway/doc/pages/d66clwan.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--ts_code` | 否 | 股票代码，精确匹配，例如 `000779.SZ`。 |
| `--trade_date` | 否 | 单个交易日，格式 `YYYYMMDD`。 |
| `--start_date` | 否 | 区间起始日期，格式 `YYYYMMDD`，需与 `end_date` 一起传入。 |
| `--end_date` | 否 | 区间结束日期，格式 `YYYYMMDD`，需与 `start_date` 一起传入。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page_size` | 否 | 每页数量，默认 `100`，范围 `1`–`1000`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`order_book_id`、`date`、`side`、`rank`、`agency`、`buy_value`、`sell_value`、`type`、`reason`

## 调用示例

```bash
python <RUN_PY> stk-shock --page 1 --trade_date 20260828
```
