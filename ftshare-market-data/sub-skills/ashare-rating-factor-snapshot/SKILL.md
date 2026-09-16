---
name: ashare-rating-factor-snapshot
description: 查询指定 A 股的 Top-K 相关公司。用户询问股票相关性、相关公司排名或相关性评分时使用。
---

# A股相关性 Top-K

外部接口：`GET /api/v3/market/data/ashare-rating-factor-snapshot`

必填：`--trade-code`。可选：`--date`（YYYYMMDD）、`--top-k`（1–500，默认由服务端设为 20）。不分页。

```bash
python <RUN_PY> ashare-rating-factor-snapshot --trade-code 600000.SH --date 20260819 --top-k 10
```

返回 `code`、`message`、`data`，其中 `data.related_securities` 按相关性分数返回相关证券。
