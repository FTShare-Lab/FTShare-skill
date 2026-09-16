---
name: limit-list
description: 查询涨跌停池。接口：GET /api/v1/market/data/limit-list。所有请求必须设置 FTSHARE_API_KEY。
---

# 涨跌停池

接口：GET `/api/v1/market/data/limit-list`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/涨跌停池.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> limit-list --limit_type up --trade_date 20260828
```
