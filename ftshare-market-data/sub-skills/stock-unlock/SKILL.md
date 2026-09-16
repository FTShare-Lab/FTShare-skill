---
name: stock-unlock
description: 查询限售解禁。接口：GET /api/v1/market/data/unlock/stock_unlock。所有请求必须设置 FTSHARE_API_KEY。
---

# 限售解禁

接口：GET `/api/v1/market/data/unlock/stock_unlock`。参数和响应以 `ftshare-doc/api-doc/股票数据/参考数据/限售解禁.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-unlock --page 1 --stock-code 600519 --stock-name 1
```
