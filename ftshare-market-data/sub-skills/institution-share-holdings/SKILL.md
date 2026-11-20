---
name: institution-share-holdings
description: "查询指定机构在指定报告期的持股汇总。可用参数：--institution_id、--year、--report_type、--invest_type。接口：GET /api/v2/market/data/institution/institution-share-holdings。"
---

# 机构股本持股

接口：GET `/api/v2/market/data/institution/institution-share-holdings`。参数和响应以 [《机构股本持股》](https://market.ft.tech/gateway/doc/pages/9vj4t4f2.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--institution_id` | 是 | 机构 ID |
| `--year` | 是 | 年份 |
| `--report_type` | 是 | 报告类型：q1 / q2 / q3 / annual / announcement |
| `--invest_type` | 是 | 持仓类型：all / stock / fund / bond / other |

## 返回

- 记录字段：`year`、`report_type`、`institution_type`、`invest_type`、`institution_id`、`institution_code`、`institution_main_code`、`institution_name`、`stock_holding_details`、`top10_holding_ratio`、`stock_code`、`stock_name`、`holding_shares`、`market_value`、`net_value_ratio`、`circulating_shares`、`total_shares`

## 调用示例

```bash
python <RUN_PY> institution-share-holdings --institution_id XXX --year 2025 --report_type annual --invest_type all
```
