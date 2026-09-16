---
name: stock-limit
description: 查询涨跌停价。接口：GET /api/v1/market/data/stk-limit。所有请求必须设置 FTSHARE_API_KEY。
---

# 涨跌停价

接口：GET `/api/v1/market/data/stk-limit`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/涨跌停价.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-limit --symbol 600519.SH --page 1
```
