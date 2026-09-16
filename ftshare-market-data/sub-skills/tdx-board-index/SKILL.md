---
name: tdx-board-index
description: 查询通达信板块指数最新快照。接口：GET /api/v1/market/data/tdx-board-index。所有请求必须设置 FTSHARE_API_KEY。
---

# 通达信板块指数最新快照

接口：GET `/api/v1/market/data/tdx-board-index`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/通达信板块指数最新快照.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> tdx-board-index --page 1 --trade_date 20260828 --lead_rise_speed 1 --lead_pre_close 1
```
