---
name: abnormal-trading-overview
description: 查询龙虎榜总览。接口：GET /api/v1/market/data/abnormal-trading-overview。所有请求必须设置 FTSHARE_API_KEY。
---

# 龙虎榜总览

接口：GET `/api/v1/market/data/abnormal-trading-overview`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/龙虎榜总览.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> abnormal-trading-overview --page 1 --symbol 600519.SH
```
