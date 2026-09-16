---
name: stock-dividends
description: 查询股票分红记录。接口：GET /api/v1/market/data/stock-dividends。所有请求必须设置 FTSHARE_API_KEY。
---

# 股票分红记录

接口：GET `/api/v1/market/data/stock-dividends`。参数和响应以 `ftshare-doc/api-doc/股票数据/参考数据/股票分红记录.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-dividends --symbol 600519.SH --page 1
```
