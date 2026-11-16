---
name: xueqiu-rank
description: "查询雪球股票排行榜最新一期快照，支持按榜单组（关注/讨论/交易）与周期（本周新增/最热门）组合查询，返回排名、代码、简称、核心指标值、最新价等。用户问雪球热榜、关注度排行、讨论热度榜时使用。"
---

# 雪球股票排名

接口：GET `/api/v1/market/data/xueqiu-rank`。参数和响应以 [《雪球股票排名》](https://market.ft.tech/gateway/doc/pages/kwt0flpu.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--rank_group` | 否 | 榜单组：`follow`（关注）/ `tweet`（讨论）/ `deal`（交易） |
| `--period` | 否 | 周期：`7d`（本周新增）/ `total`（最热门） |
| `--trade_date` | 否 | 交易日期，格式 `YYYY-MM-DD`，不传默认取最新 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页条数，默认 20，最大 100 |

## 返回

- 记录容器：`data.items`
- 分页字段：`total`
- 记录字段：`trade_date`、`display_name`、`metric_name`、`rank_no`、`normalized_symbol`、`stock_name`、`metric_value`、`latest_price`、`raw_symbol`

## 调用示例

```bash
python <RUN_PY> xueqiu-rank --page 1
```
