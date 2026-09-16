---
name: nanhua-index-kline
description: 查询南华期货指数日K线。接口：GET /api/v1/market/data/futures/nanhua-index-kline。所有请求必须设置 FTSHARE_API_KEY。
---

# 南华期货指数日K线

接口：GET `/api/v1/market/data/futures/nanhua-index-kline`。参数和响应以 `ftshare-doc/api-doc/期货数据/南华期货指数日K线.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> nanhua-index-kline --trade_date 20260821 --page 1 --page_size 5
```
