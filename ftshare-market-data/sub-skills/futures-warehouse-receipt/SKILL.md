---
name: futures-warehouse-receipt
description: "查询商品期货交易所发布的仓单日报明细。接口：GET /api/v1/market/data/futures/fut-wsr。"
---

# 期货仓单日报

接口：`GET /api/v1/market/data/futures/fut-wsr`。在线文档：[《期货仓单日报》](https://market.ft.tech/gateway/doc/pages/btn0gr4b.md)

外部接口：`GET /api/v1/market/data/futures/fut-wsr`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-date` | 否 | 单个交易日，格式 `YYYYMMDD`；不能与日期区间同时使用。 |
| `--start-date` | 否 | 开始交易日，格式 `YYYYMMDD`。 |
| `--end-date` | 否 | 结束交易日，格式 `YYYYMMDD`。 |
| `--symbol` | 否 | 品种代码，例如 `CU`、`A`、`SR`。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page-size` | 否 | 每页条数，默认 `50`，最大 `200`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`symbol`、`fut_name`、`warehouse`、`wh_id`、`pre_vol`、`vol`、`vol_chg`、`area`、`year`、`grade`、`brand`

## 调用示例

```bash
python <RUN_PY> futures-warehouse-receipt --symbol CU --trade-date 20260721 --page 1 --page-size 5
```
