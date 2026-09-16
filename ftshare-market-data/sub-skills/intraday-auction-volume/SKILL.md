---
name: intraday-auction-volume
description: 查询单只股票连续竞价成交量和成交额占比。用户询问个股分时成交占比时使用。
---

# 单标的连续竞价成交量

接口：`GET /api/v1/market/data/intraday-auction-volume/symbol`。必填 `--symbol`；可选 `--trade-date`（YYYYMMDD）、`--page` 和 `--page-size`，每页最多 200 条。

```bash
python <RUN_PY> intraday-auction-volume --symbol 600000.SH --page 1 --page-size 50
```

不传交易日查询当日实时数据，传入历史交易日查询历史分钟数据；响应为 `code/message/data` 分页信封，分钟记录位于 `data.records`。
