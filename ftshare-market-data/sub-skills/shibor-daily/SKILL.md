---
name: shibor-daily
description: 查询SHIBOR日度利率。接口：GET /api/v1/market/data/shibor-daily。所有请求必须设置 FTSHARE_API_KEY。
---

# SHIBOR日度利率

接口：GET `/api/v1/market/data/shibor-daily`。参数和响应以 `ftshare-doc/api-doc/宏观经济/国内宏观/SHIBOR日度利率.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> shibor-daily --start_date 20260828 --end_date 20260828 --page 1 --trade_date 20260828 --w1 1 --w2 1 --m1 1 --m3 1 --m6 1 --m9 1 --y1 1
```
