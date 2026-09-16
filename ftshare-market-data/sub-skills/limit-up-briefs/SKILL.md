---
name: limit-up-briefs
description: 查询涨停简报。接口：GET /api/v3/market/data/limit-up-reports/briefs。所有请求必须设置 FTSHARE_API_KEY。
---

# 涨停简报

接口：GET `/api/v3/market/data/limit-up-reports/briefs`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/涨停简报.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> limit-up-briefs --date 20260828
```
