---
name: daec-history-prices
description: 查询标的分时数据。接口：GET /api/v4/market/data/daec/history/prices。所有请求必须设置 FTSHARE_API_KEY。
---

# 标的分时数据

接口：GET `/api/v4/market/data/daec/history/prices`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/标的分时数据.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> daec-history-prices --symbol 600519.SH
```
