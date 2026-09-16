---
name: stk-ah-comparison
description: 查询 A/H 股比价、涨跌幅和溢价率。用户询问港股与对应 A 股估值比较时使用。
---

# AH 股对比

接口：`GET /api/v1/market/data/hk/stk-ah-comparison`。可按 `--hk-code`、`--ts-code`、`--trade-date` 或日期区间 `--start-date`/`--end-date` 过滤；日期区间最多 30 个自然日。分页参数为 `--page`（默认 1）和 `--page-size`（默认 50，最大 1000），支持 `--all` 自动翻页。

```bash
python <RUN_PY> stk-ah-comparison --hk-code 00700.HK --trade-date 20260623 --page 1 --page-size 20
```

响应为 `code/message/data` 分页信封，记录位于 `data.records`，包含双方代码、名称、收盘价、涨跌幅、A/H 比价和溢价率。
