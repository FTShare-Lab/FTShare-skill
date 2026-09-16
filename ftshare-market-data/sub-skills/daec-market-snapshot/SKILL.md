---
name: daec-market-snapshot
description: 查询市场行情快照。接口：GET /api/v1/market/data/daec/market/snapshot。所有请求必须设置 FTSHARE_API_KEY。
---

# 市场行情快照

接口：GET `/api/v1/market/data/daec/market/snapshot`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/市场行情快照.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> daec-market-snapshot
```
