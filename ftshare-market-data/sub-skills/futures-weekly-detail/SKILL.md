---
name: futures-weekly-detail
description: "查询期货主要品种的周成交量、成交额、持仓量和周度变化。接口：GET /api/v1/market/data/futures/fut-weekly-detail。"
---

# 期货主要品种交易周报

接口：`GET /api/v1/market/data/futures/fut-weekly-detail`。在线文档：[《期货主要品种交易周报》](https://market.ft.tech/gateway/doc/pages/wao8q91z.md)

外部接口：`GET /api/v1/market/data/futures/fut-weekly-detail`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--week` | 否 | 单个统计周期，格式 `YYYYWW`，例如 `202601`。 |
| `--prd` | 否 | 期货品种代码；支持逗号分隔，例如 `CU,AL`。 |
| `--start-week` | 否 | 开始统计周期，格式 `YYYYWW`。 |
| `--end-week` | 否 | 结束统计周期，格式 `YYYYWW`。 |
| `--exchange` | 否 | 交易所代码：`SHFE`、`INE`、`CZCE`、`CFFEX`、`DCE`、`GFEX`。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page-size` | 否 | 每页条数，默认 `50`，最大 `200`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`exchange`、`prd`、`name`、`vol`、`vol_yoy`、`amount`、`amout_yoy`、`cumvol`、`cumvol_yoy`、`cumamt`、`cumamt_yoy`、`open_interest`、`interest_wow`、`mc_close`、`close_wow`、`week`、`week_date`

## 调用示例

```bash
python <RUN_PY> futures-weekly-detail --week 202628 --prd CU,AL --page 1 --page-size 5
```
