---
name: wallstreetcn-financial-calendar
description: 查询华尔街见闻财经日历。接口：GET /api/v1/market/data/finance/financial-calendar/wallstreetcn。所有请求必须设置 FTSHARE_API_KEY。
---

# 华尔街见闻财经日历

接口：GET `/api/v1/market/data/finance/financial-calendar/wallstreetcn`。参数和响应以 `ftshare-doc/api-doc/宏观经济/国内宏观/华尔街见闻财经日历.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> wallstreetcn-financial-calendar --start_date 20260828 --end_date 20260828 --page 1
```
