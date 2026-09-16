---
name: institution-share-holdings
description: 查询机构股本持股。接口：GET /api/v2/market/data/institution/institution-share-holdings。所有请求必须设置 FTSHARE_API_KEY。
---

# 机构股本持股

接口：GET `/api/v2/market/data/institution/institution-share-holdings`。参数和响应以 `ftshare-doc/api-doc/股票数据/基础数据/机构股本持股.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> institution-share-holdings --institution_id XXX --year 2025 --report_type annual --invest_type all
```
