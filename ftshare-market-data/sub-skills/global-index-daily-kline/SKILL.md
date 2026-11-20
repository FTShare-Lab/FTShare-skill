---
name: global-index-daily-kline
description: "获取全球指数（含部分 A 股/港股宽基）的历史日K线，返回 `{total, items}` 结构（非分页，按时间区间一次性返回）。可用参数：--secid、--start_date、--end_date、--limit。接口：GET /api/v1/market/data/global-index/daily-kline。"
---

# 全球指数日K线

接口：GET `/api/v1/market/data/global-index/daily-kline`。参数和响应以 [《全球指数日K线》](https://market.ft.tech/gateway/doc/pages/j0twmp6x.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--secid` | 是 | 东方财富全球指数编码，如 100.NDX、100.DJIA、100.SPX、100.HSI、100.N225 |
| `--start_date` | 否 | 开始日期 YYYYMMDD（含） |
| `--end_date` | 否 | 结束日期 YYYYMMDD（含） |
| `--limit` | 否 | 返回根数上限，1~5000；不传时无日期区间返回最近 100 根，带日期区间最多返回 5000 根 |

## 返回

- 记录容器：`data.items`
- 分页字段：`total`
- 记录字段：`secid`、`name`、`trade_date`、`open`、`close`、`high`、`low`、`volume`、`amount`、`amplitude`、`change_pct`、`change_amount`、`turnover`

## 调用示例

```bash
python <RUN_PY> global-index-daily-kline --secid 100.DJIA --limit 5
```
