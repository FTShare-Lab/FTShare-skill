---
name: eastmoney-stock-flow
description: 查询东方财富个股资金流。接口：GET /api/v1/market/data/eastmoney-stock-flow。所有请求必须设置 FTSHARE_API_KEY。
---

# 东方财富个股资金流

接口：GET `/api/v1/market/data/eastmoney-stock-flow`。参数和响应以 `ftshare-doc/api-doc/股票数据/资金流向数据/东方财富个股资金流.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数与注意事项

- `symbol` 为纯数字股票代码（如 `600522`），不带交易所后缀。
- `trade_date`、`start_date`、`end_date` 必须为 `YYYYMMDD`；带横杠的日期（如 `2026-08-18`）会返回 HTTP 400。响应中的 `trade_date` 为 `YYYY-MM-DD`。
- 日期区间需同时提供 `start_date` 和 `end_date`。
- `market` 字段：0=深，1=沪。分页默认 `page=1`、`page_size=50`，最大 `page_size=500`。

## 调用示例

```bash
python <RUN_PY> eastmoney-stock-flow --symbol 600519 --trade_date 20260818 --page 1
```
