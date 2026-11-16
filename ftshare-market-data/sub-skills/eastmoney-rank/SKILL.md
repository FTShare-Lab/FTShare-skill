---
name: eastmoney-rank
description: "查询东方财富股票排行榜最新一期快照。可用参数：--rank_group、--market、--trade_date。接口：GET /api/v1/market/data/eastmoney-rank。"
---

# 东方财富股票排名

接口：GET `/api/v1/market/data/eastmoney-rank`。参数和响应以 [《东方财富股票排名》](https://market.ft.tech/gateway/doc/pages/178klizp.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--rank_group` | 否 | 榜单组：`hot`（人气榜）/ `up`（飙升榜） |
| `--market` | 否 | 市场：`A`（A股）/ `HK`（港股）/ `US`（美股） |
| `--trade_date` | 否 | 交易日期，格式 `YYYY-MM-DD`，不传默认取最新 |

## 返回

- 记录容器：`data.items`
- 分页字段：`total`
- 记录字段：`trade_date`、`display_name`、`metric_name`、`rank_no`、`rank_change`、`normalized_symbol`、`stock_name`、`hot_score`、`latest_price`、`change_amount`、`change_pct`、`raw_symbol`

## 调用示例

```bash
python <RUN_PY> eastmoney-rank --rank_group hot --market A
```
