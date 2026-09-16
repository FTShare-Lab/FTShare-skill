---
name: global-index-daily-kline
description: 查询全球指数日K线。接口：GET /api/v1/market/data/global-index/daily-kline。所有请求必须设置 FTSHARE_API_KEY。
---

# 全球指数日K线

接口：GET `/api/v1/market/data/global-index/daily-kline`。参数和响应以 `ftshare-doc/api-doc/指数专题/指数行情/全球指数日K线.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> global-index-daily-kline --secid 1 --limit 5 --name 1 --trade_date 20260828 --amplitude 1
```
