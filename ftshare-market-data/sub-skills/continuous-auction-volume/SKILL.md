---
name: continuous-auction-volume
description: 查询全市场连续竞价成交量和成交额占比。用户询问全市场、沪深北市场的分时成交占比时使用。
---

# 连续竞价成交量

接口：`GET /api/v2/market/data/intraday-auction-volume`。可选 `--trade-date`（YYYYMMDD）、`--page` 和 `--page-size`，每页最多 200 条；支持 `--all` 自动翻页。

```bash
python <RUN_PY> continuous-auction-volume --trade-date 20260620 --page 1 --page-size 50
```

不传交易日查询当日实时全市场聚合数据，传入历史交易日查询历史数据；响应为 `code/message/data` 分页信封，分钟记录位于 `data.records`，包含 overall、xshg、xshe 和 bjse 四个市场维度。
