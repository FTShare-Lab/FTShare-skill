---
name: stk-shock
description: 查询个股异常波动。接口：GET /api/v2/market/data/stk-shock。所有请求必须设置 FTSHARE_API_KEY。
---

# 个股异常波动

接口：GET `/api/v2/market/data/stk-shock`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/个股异常波动.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stk-shock --page 1 --order_book_id 1 --date 20260828 --rank 1 --type stock
```
