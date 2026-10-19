---
name: abnormal-trading-overview
description: 查询龙虎榜总览。接口：GET /api/v1/market/data/abnormal-trading-overview。所有请求必须设置 FTSHARE_API_KEY。
---

# 龙虎榜总览

接口：GET `/api/v1/market/data/abnormal-trading-overview`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/龙虎榜总览.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数与注意事项

- `date` 格式 `YYYYMMDD`；不传返回最新快照。`page` 从 1 开始；`page_size` 默认 200，最大 500。
- 每条记录含 `symbol`、`symbol_name`、`reason`（上榜原因）、`change_rate`、`close`、`turnover`。
- 同一标的在同一交易日可能因不同上榜原因返回多条记录。
- `symbol` 使用短市场后缀，如 `600000.SH`、`000001.SZ`、`920001.BJ`。

## 调用示例

```bash
python <RUN_PY> abnormal-trading-overview --page 1 --page_size 200 --date 20260828
```
