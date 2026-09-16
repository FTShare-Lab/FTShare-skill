---
name: ashare-status-change
description: 查询 A 股状态变更记录。Use when user asks about 上市、退市、暂停上市或股票状态变更。
---

# A 股状态变更

接口：`GET /api/v1/market/data/stk-status-change`。支持代码、变更日期和变更类型任意组合过滤，不分页。

```bash
python <RUN_PY> ashare-status-change --trade-code 600848.SH
python <RUN_PY> ashare-status-change --trade-code 600848.SH --change-type 上市
python <RUN_PY> ashare-status-change --change-date 20240101
```

- `--trade-code`：可选，支持逗号分隔多个 `.SZ`/`.SH` 代码。
- `--change-date`：可选，精确日期过滤，格式 `YYYYMMDD`。
- `--change-type`：可选，精确类型过滤，如 `上市`、`退市`、`暂停上市`。

成功响应为 `code/message/data`，记录包括 `trade_code`、`name`、`change_date`、`change_type`、`change_details`，按代码升序、日期降序返回。
