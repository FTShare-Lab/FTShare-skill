---
name: ashare-code-change
description: 查询 A 股代码变更历史。Use when user asks about 股票代码变更、改名换码、代码迁移或北交所升板代码历史。
---

# A 股代码变更

接口：`GET /api/v1/market/data/stk-code-change`。`trade_code` 必填，支持逗号分隔多个带市场后缀的代码；不分页，返回全部变更记录。在线文档：[《A股代码变更》](https://market.ft.tech/gateway/doc/pages/yuzopjw5.md)

```bash
python <RUN_PY> ashare-code-change --trade-code 001872.SZ
python <RUN_PY> ashare-code-change --trade-code 001872.SZ,920000.BJ --start-date 20180101 --end-date 20241231
```

- `--trade-code`：必填，如 `600848.SH`，可逗号分隔多个。
- `--start-date`、`--end-date`：可选，格式 `YYYYMMDD`；同时提供时起始日不得晚于截止日。

成功响应为 `code/message/data`，`data` 为记录数组或对象中的记录数据，记录包括最新 `trade_code`、实际使用的 `code`、`name`、`start_date` 和可为空的 `end_date`。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-code` | 是 | 股票代码（带 .SZ/.SH 后缀），支持逗号分隔多个，如 `600848.SH` 或 `600848.SH,000001.SZ` |
| `--start-date` | 否 | 过滤区间起始日期，`YYYYMMDD` 格式 |
| `--end-date` | 否 | 过滤区间结束日期，`YYYYMMDD` 格式；与 `start_date` 同时提供时须 `start_date` ≤ `end_date` |

## 返回

- 记录字段：`trade_code`、`name`、`start_date`、`end_date`
