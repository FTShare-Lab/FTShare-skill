---
name: futures-limit
description: "查询期货合约每日涨停价、跌停价和最低保证金率。接口：GET /api/v1/market/data/futures/ft-limit。"
---

# 期货合约涨跌停价

接口：`GET /api/v1/market/data/futures/ft-limit`。在线文档：[《期货合约涨跌停价》](https://market.ft.tech/gateway/doc/pages/5nbz5zdb.md)

外部接口：`GET /api/v1/market/data/futures/ft-limit`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--ts-code` | 否 | 合约代码，例如 `A2609.DCE`、`CU2608.SHF`。 |
| `--trade-date` | 否 | 单个交易日，格式 `YYYYMMDD`；不能与日期区间同时使用。`trade_date` 与 `start_date`+`end_date` 至少提供一组。 |
| `--start-date` | 否 | 开始交易日，格式 `YYYYMMDD`；须与 `end_date` 同时提供。 |
| `--end-date` | 否 | 结束交易日，格式 `YYYYMMDD`；须与 `start_date` 同时提供。 |
| `--cont` | 否 | 品种代码，例如 `CU`、`A`。 |
| `--exchange` | 是 | 交易所代码：`SHFE`、`INE`、`CZCE`、`CFFEX`、`DCE`、`GFEX`。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page-size` | 否 | 每页条数，默认 `50`，最大 `200`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`ts_code`、`name`、`up_limit`、`down_limit`、`m_ratio`、`cont`、`exchange`

## 调用示例

```bash
python <RUN_PY> futures-limit --ts-code A2609.DCE --trade-date 20260721 --exchange DCE --page 1 --page-size 5
```
