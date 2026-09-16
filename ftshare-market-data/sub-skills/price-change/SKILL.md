---
name: price-change
description: 查询价格变动。接口：GET /api/v2/market/data/price/get-price-change。所有请求必须设置 FTSHARE_API_KEY。
---

# 价格变动

接口：GET `/api/v2/market/data/price/get-price-change`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/价格变动.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> price-change --stock_code 600519 --base_date 20260828 --n 5 --direction forward --stock_name 1 --start_date 20260828 --end_date 20260828 --actual_trading_days 1 --start_price 1 --end_price 1 --price_change 1
```
