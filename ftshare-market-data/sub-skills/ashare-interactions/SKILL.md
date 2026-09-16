---
name: ashare-interactions
description: 查询e互动。接口：GET /api/v2/market/data/ashare-interactions。所有请求必须设置 FTSHARE_API_KEY。
---

# e互动

接口：GET `/api/v2/market/data/ashare-interactions`。参数和响应以 `ftshare-doc/api-doc/股票数据/特色数据/e互动.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> ashare-interactions --start_date 20260828 --end_date 20260828 --page 1 --page_size 5
```
