---
name: sw-industry-daily-metrics
description: 查询申万行业日度指标。接口：GET /api/v1/market/data/sw-industry/daily-metrics。所有请求必须设置 FTSHARE_API_KEY。
---

# 申万行业日度指标

接口：GET `/api/v1/market/data/sw-industry/daily-metrics`。参数和响应以 `ftshare-doc/api-doc/指数专题/申万行业/申万行业日度指标.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> sw-industry-daily-metrics --start_date 20260828 --end_date 20260828 --industry_code 银行 --page 1
```
