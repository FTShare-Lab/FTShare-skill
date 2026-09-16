---
name: libor-daily
description: 查询国际基准利率日度。接口：GET /api/v1/market/data/libor-daily。所有请求必须设置 FTSHARE_API_KEY。
---

# 国际基准利率日度

接口：GET `/api/v1/market/data/libor-daily`。参数和响应以 `ftshare-doc/api-doc/宏观经济/国际宏观/国际基准利率日度.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> libor-daily --start_date 20260828 --end_date 20260828 --page 1 --trade_date 20260828
```
