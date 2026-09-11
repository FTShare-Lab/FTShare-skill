---
name: stock-st-history
description: 查询 A 股股票历史风险警示（ST/*ST/PT/退市整理期）状态区间。Use when user asks about 股票历史ST状态、ST 区间、风险警示区间、摘帽或退市整理期。
---

# 股票历史ST状态

接口：`GET /api/v1/market/data/stock-st-history`。`symbol` 必填，支持逗号分隔批量；`st_type` 可选过滤；不分页，一次返回全部阶段区间。

```bash
python <RUN_PY> stock-st-history --symbol 600735.SH
python <RUN_PY> stock-st-history --symbol 600735.SH,000004.SZ
python <RUN_PY> stock-st-history --symbol 000004.SZ --st-type 退市整理期
```

- `--symbol`：必填，带 `.SH`/`.SZ` 后缀的股票代码，逗号分隔去重后最多 50 只。
- `--st-type`：可选，阶段类型过滤，取值 `ST`、`*ST`、`PT`、`退市整理期`。

成功响应为 `code/message/data`，`data` 为阶段区间数组，元素包含 `symbol`、`st_type`、`st_name`、`start_date`、`end_date`、`delist_end`、`reason`、`publish_date`。`end_date` 为 `null` 表示仍在警示中；`delist_end=true` 表示该阶段以终止上市日结束。摘帽后的无警示区间不产生记录。
