---
name: stock-institution-holdings
description: 查询机构持股。接口：GET /api/v2/market/data/share/stock-institution-holdings。所有请求必须设置 FTSHARE_API_KEY。
---

# 机构持股

接口：GET `/api/v2/market/data/share/stock-institution-holdings`。参数和响应以 `ftshare-doc/api-doc/股票数据/基础数据/机构持股.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-institution-holdings --year 2025 --report_type annual --institution_type all_inst --page 1 --page_size 5
```
