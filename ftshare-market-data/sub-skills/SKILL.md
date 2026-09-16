---
name: sub-skills
description: 查询股票列表。接口：GET /api/v1/market/data/stock-list。所有请求必须设置 FTSHARE_API_KEY。
---

# 股票列表

接口：GET `/api/v1/market/data/stock-list`。

请求参数通过同名 kebab-case CLI 选项传入；详细参数和响应字段以 `ftshare-doc/api-doc/股票数据/基础数据/股票列表.md` 为准。

所有请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

```bash
python <RUN_PY> sub-skills
```
