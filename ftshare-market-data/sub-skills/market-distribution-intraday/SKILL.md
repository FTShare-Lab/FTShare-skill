---
name: market-distribution-intraday
description: 查询市场涨跌分布分时。接口：GET /api/v2/market/data/market-distribution-intraday。所有请求必须设置 FTSHARE_API_KEY。
---

# 市场涨跌分布分时

接口：GET `/api/v2/market/data/market-distribution-intraday`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/市场涨跌分布分时.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> market-distribution-intraday --ts_millis 1787191200000 --up_limited 5 --down_limited 5
```
