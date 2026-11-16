---
name: eastmoney-futures-position
description: "获取东方财富期货每日成交持仓排行榜数据，按合约/会员维度给出成交量、多头、空头、净多头、净空头的排名与持仓量及变化，含多头增/减仓、空头增/减仓排名，以及结算价、多头/空头平均价。接口：GET /api/v1/market/data/eastmoney-futures-position。"
---

# 东方财富期货持仓

接口：`GET /api/v1/market/data/eastmoney-futures-position`。在线文档：[《东方财富期货持仓》](https://market.ft.tech/gateway/doc/pages/7al9wvew.md)

外部接口：`GET /api/v1/market/data/eastmoney-futures-position`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--exchange` | 否 | 交易所代码：shfe / dce / czce / cffex / ine / gfe |
| `--variety-code` | 否 | 品种代码，如 cu / au / al / IF |
| `--contract-code` | 否 | 合约代码，如 CU2607 / AU2608 |
| `--trade-date` | 否 | 交易日 YYYY-MM-DD 或 YYYYMMDD；与其他日期条件组合时按 AND 过滤 |
| `--start-date` | 否 | 起始日期 YYYY-MM-DD 或 YYYYMMDD；过滤大于等于该日期的记录 |
| `--end-date` | 否 | 结束日期 YYYY-MM-DD 或 YYYYMMDD；过滤小于等于该日期的记录 |
| `--member-name-abbr` | 否 | 会员简称 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页条数，默认 50，最大 500 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`exchange`、`variety_code`、`contract_code`、`trade_date`、`org_code`、`member_name_abbr`、`volume_rank`、`volume`、`volume_change`、`lp_rank`、`long_position`、`lp_change`、`sp_rank`、`short_position`、`sp_change`、`nlp_rank`、`net_long_position`、`nlp_change` …共 28 个

## 调用示例

```bash
python <RUN_PY> eastmoney-futures-position --page 1 --page-size 5
```
