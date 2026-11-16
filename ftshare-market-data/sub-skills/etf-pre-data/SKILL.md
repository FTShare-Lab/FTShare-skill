---
name: etf-pre-data
description: "获取指定交易日的全部 ETF 盘前信息（申赎单位、净值、现金差额、是否公布 IOPV、申赎允许情况、预估现金部分等）。可用参数：--date。接口：GET /api/v2/market/data/etf-pre-data。"
---

# ETF盘前数据

接口：GET `/api/v2/market/data/etf-pre-data`。参数和响应以 [《ETF盘前数据》](https://market.ft.tech/gateway/doc/pages/gzgewm9p.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--date` | 否 | 交易日 YYYYMMDD；不传则使用当日（CST） |

## 返回

- 记录容器：`data.items`
- 记录字段：`trade_date`、`etf_symbol_id`、`etf_market_id`、`creation_redemption_unit`、`max_cash_ratio`、`publish_ipov`、`creation_redemption_flag`、`record_num`、`estimate_cash_component`、`cash_component`、`nav_per_cu`、`nav`、`member_market_type`

## 调用示例

```bash
python <RUN_PY> etf-pre-data
```
