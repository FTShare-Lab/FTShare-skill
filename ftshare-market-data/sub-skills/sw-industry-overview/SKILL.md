---
name: sw-industry-overview
description: 查询申万行业总览。接口：GET /api/v1/market/data/sw-industry/overview。所有请求必须设置 FTSHARE_API_KEY。
---

# 申万行业总览

接口：GET `/api/v1/market/data/sw-industry/overview`。参数和响应以 `ftshare-doc/api-doc/指数专题/申万行业/申万行业总览.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> sw-industry-overview --date 20260828 --page 1 --industry-code 银行 --industry-name 银行
```
