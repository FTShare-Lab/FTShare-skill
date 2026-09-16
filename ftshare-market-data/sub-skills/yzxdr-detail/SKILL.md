---
name: yzxdr-detail
description: 查询一致行动人明细。接口：GET /api/v1/market/data/yzxdr-detail。所有请求必须设置 FTSHARE_API_KEY。
---

# 一致行动人明细

接口：GET `/api/v1/market/data/yzxdr-detail`。参数和响应以 `ftshare-doc/api-doc/股票数据/基础数据/一致行动人明细.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> yzxdr-detail --year 2025 --quarter 4 --page 1 --id 1 --stock_name 1
```
