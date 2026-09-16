---
name: nth-trade-date
description: 查询第 N 个交易日。Use when user asks for 前 N 个交易日、某日期对应的第 N 个交易日或交易日倒推。
---

# 第 N 个交易日

接口：`GET /api/v1/market/data/time/get-nth-trade-date`。按服务端当前日期向前计算第 N 个交易日。

```bash
python <RUN_PY> nth-trade-date --n 5
```

- `--n`：必填整数，必须大于等于 1。

响应为 `code/message/data` 信封，`data` 包括 `current_date`、`nth_trade_date`（均为 `YYYY-MM-DD`）和请求的 `n`。
