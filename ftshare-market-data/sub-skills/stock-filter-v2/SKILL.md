---
name: stock-filter-v2
description: 查询股票筛选。接口：GET /api/v2/market/data/stock-list/filter。所有请求必须设置 FTSHARE_API_KEY。
---

# 股票筛选

接口：GET `/api/v2/market/data/stock-list/filter`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/股票筛选.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-filter-v2 --symbol 600519.SH --page 1 --type stock --symbol_id 1 --symbol_name 1
```
