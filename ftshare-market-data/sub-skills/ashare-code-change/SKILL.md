---
name: ashare-code-change
description: 查询 A 股代码变更历史。Use when user asks about 股票代码变更、改名换码、代码迁移或北交所升板代码历史。
---

# A 股代码变更

接口：`GET /api/v1/market/data/stk-code-change`。`trade_code` 必填，支持逗号分隔多个带市场后缀的代码；不分页，返回全部变更记录。

```bash
python <RUN_PY> ashare-code-change --trade-code 001872.SZ
python <RUN_PY> ashare-code-change --trade-code 001872.SZ,920000.BJ --start-date 20180101 --end-date 20241231
```

- `--trade-code`：必填，如 `600848.SH`，可逗号分隔多个。
- `--start-date`、`--end-date`：可选，格式 `YYYYMMDD`；同时提供时起始日不得晚于截止日。

成功响应为 `code/message/data`，`data` 为记录数组或对象中的记录数据，记录包括最新 `trade_code`、实际使用的 `code`、`name`、`start_date` 和可为空的 `end_date`。
