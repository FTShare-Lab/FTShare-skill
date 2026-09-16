---
name: abnormal-trading-details
description: 查询龙虎榜明细。接口：GET /api/v1/market/data/abnormal-trading-details。所有请求必须设置 FTSHARE_API_KEY。
---

# 龙虎榜明细

接口：GET `/api/v1/market/data/abnormal-trading-details`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/龙虎榜明细.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> abnormal-trading-details --date 20260828 --page 1 --page_size 5
```
