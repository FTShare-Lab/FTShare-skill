---
name: stk-surv
description: 查询个股严重异常波动。接口：GET /api/v2/market/data/stk-surv。所有请求必须设置 FTSHARE_API_KEY。
---

# 个股严重异常波动

接口：GET `/api/v2/market/data/stk-surv`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/个股严重异常波动.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stk-surv --page 1 --name 1 --trade_market A
```
