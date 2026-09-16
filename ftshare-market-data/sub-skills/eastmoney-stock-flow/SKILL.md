---
name: eastmoney-stock-flow
description: 查询东方财富个股资金流。接口：GET /api/v1/market/data/eastmoney-stock-flow。所有请求必须设置 FTSHARE_API_KEY。
---

# 东方财富个股资金流

接口：GET `/api/v1/market/data/eastmoney-stock-flow`。参数和响应以 `ftshare-doc/api-doc/股票数据/资金流向数据/东方财富个股资金流.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> eastmoney-stock-flow --symbol 600519.SH --page 1 --name 1 --market A --super_large_net 1 --super_large_pct 1 --medium_net 1 --medium_pct 1
```
