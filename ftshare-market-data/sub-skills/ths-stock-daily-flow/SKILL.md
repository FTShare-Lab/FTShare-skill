---
name: ths-stock-daily-flow
description: 查询同花顺个股资金流日度。接口：GET /api/v1/market/data/ths-stock-daily-flow。所有请求必须设置 FTSHARE_API_KEY。
---

# 同花顺个股资金流日度

接口：GET `/api/v1/market/data/ths-stock-daily-flow`。参数和响应以 `ftshare-doc/api-doc/股票数据/资金流向数据/同花顺个股资金流日度.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> ths-stock-daily-flow --start_date 20260828 --end_date 20260828 --page 1 --trade_date 20260828
```
