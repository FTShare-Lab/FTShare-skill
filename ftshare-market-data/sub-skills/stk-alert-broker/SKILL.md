---
name: stk-alert-broker
description: 查询交易所重点提示证券。接口：GET /api/v2/market/data/stk-alert-broker。所有请求必须设置 FTSHARE_API_KEY。
---

# 交易所重点提示证券

接口：GET `/api/v2/market/data/stk-alert-broker`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/交易所重点提示证券.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stk-alert-broker --page 1 --name 1 --type stock
```
