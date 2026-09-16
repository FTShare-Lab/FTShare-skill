---
name: sw-industry-constituent-history
description: 查询申万行业成份股历史。接口：GET /api/v1/market/data/sw-industry/constituent-history。所有请求必须设置 FTSHARE_API_KEY。
---

# 申万行业成份股历史

接口：GET `/api/v1/market/data/sw-industry/constituent-history`。参数和响应以 `ftshare-doc/api-doc/指数专题/申万行业/申万行业成份股历史.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> sw-industry-constituent-history --industry_code 银行 --stock-code 600519 --stock-name 1 --sw-level1-code 1 --sw-level1-name 1
```
