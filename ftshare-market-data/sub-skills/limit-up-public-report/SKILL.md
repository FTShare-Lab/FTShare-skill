---
name: limit-up-public-report
description: 查询涨停对外归因报告。接口：GET /api/v3/market/data/limit-up-reports/public-report。所有请求必须设置 FTSHARE_API_KEY。
---

# 涨停对外归因报告

接口：GET `/api/v3/market/data/limit-up-reports/public-report`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/涨停对外归因报告.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> limit-up-public-report --date 20260724 --security_code 603976.SH
```
