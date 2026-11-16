---
name: nanhua-index-kline
description: "查询南华期货指数日 K 线，覆盖南华系列商品指数（`AD_NH`、`AG_NH`、`AL_NH`、`AO_NH`、`AP_NH` 等）。接口：GET /api/v1/market/data/futures/nanhua-index-kline。"
---

# 南华期货指数日K线

接口：GET `/api/v1/market/data/futures/nanhua-index-kline`。参数和响应以 [《南华期货指数日K线》](https://market.ft.tech/gateway/doc/pages/45cmhmre.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade_date` | 否 | 交易日期（YYYYMMDD）；传入时为单日截面模式，忽略 start_date/end_date |
| `--start_date` | 否 | 起始日期（YYYYMMDD），区间模式下界 |
| `--end_date` | 否 | 结束日期（YYYYMMDD），区间模式上界；不得早于 start_date |
| `--page` | 否 | 页码，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`open`、`high`、`low`、`close`、`pre_close`、`change`、`pct_chg`、`vol`、`amount`

## 调用示例

```bash
python <RUN_PY> nanhua-index-kline --trade_date 20260821 --page 1 --page_size 5
```
