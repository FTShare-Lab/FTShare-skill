---
name: etf-pre-data
description: 查询ETF盘前数据。接口：GET /api/v2/market/data/etf-pre-data。所有请求必须设置 FTSHARE_API_KEY。
---

# ETF盘前数据

接口：GET `/api/v2/market/data/etf-pre-data`。参数和响应以 `ftshare-doc/api-doc/ETF专题/ETF盘前数据.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> etf-pre-data
```
