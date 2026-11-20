---
name: futures-settle
description: "查询期货合约每日结算价、手续费和保证金参数。接口：GET /api/v1/market/data/futures/fut-settle。"
---

# 期货每日结算参数

接口：`GET /api/v1/market/data/futures/fut-settle`。在线文档：[《期货每日结算参数》](https://market.ft.tech/gateway/doc/pages/hvux2jh0.md)

外部接口：`GET /api/v1/market/data/futures/fut-settle`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。`--exchange` 在未传 `--ts-code` 时必填（`SHFE`/`INE`/`CZCE`/`CFFEX`/`DCE`/`GFEX`）；`--trade-date` 与 `--start-date`/`--end-date` 二选一，区间跨度不超过 31 天。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--ts-code` | 否 | 不带交易所后缀的合约代码，如 `A2609`；请求不区分大小写，CZCE 真实合约必须使用四位年份代码（如 `AP2612`）。传入时可省略 `--exchange`。 |
| `--trade-date` | 否 | 单个交易日，格式 `YYYYMMDD`；不能与日期区间同时使用。 |
| `--start-date` | 否 | 开始交易日，格式 `YYYYMMDD`；必须与 `end_date` 同时传入，且日期区间跨度不超过 31 天。 |
| `--end-date` | 否 | 结束交易日，格式 `YYYYMMDD`；必须与 `start_date` 同时传入。 |
| `--exchange` | 否 | 交易所代码：`SHFE`、`INE`、`CZCE`、`CFFEX`、`DCE`、`GFEX`。不传 `--ts-code` 时必填；传 `--ts-code` 时用于范围限制和一致性校验。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page-size` | 否 | 每页条数，默认 `50`，最大 `4000`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`ts_code`、`trade_date`、`settle`、`trading_fee_rate`、`trading_fee`、`delivery_fee`、`b_hedging_margin_rate`、`s_hedging_margin_rate`、`long_margin_rate`、`short_margin_rate`、`offset_today_fee`、`exchange`

## 调用示例

```bash
python <RUN_PY> futures-settle --exchange DCE --ts-code A2609 --trade-date 20260721 --page 1 --page-size 5
```
