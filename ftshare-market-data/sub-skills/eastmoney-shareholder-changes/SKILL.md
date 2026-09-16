---
name: eastmoney-shareholder-changes
description: 查询东方财富股东增减持。Use when user asks about 股东增持、股东减持或东方财富股东变动。
---

# 东方财富股东增减持

接口：`GET /api/v1/market/data/holder/stock-ggcg-em`。通过 `symbol` 筛选全部、股东增持或股东减持，返回分页明细。

```bash
python <RUN_PY> eastmoney-shareholder-changes --symbol 全部 --page 1 --page-size 20
python <RUN_PY> eastmoney-shareholder-changes --symbol 股东减持 --all
```

- `--symbol`：可选，`全部`、`股东增持` 或 `股东减持`，默认全部。
- `--page`：页码，默认 1。
- `--page-size`：每页条数，默认 50，最大 200。
- `--all`：自动翻页合并全部记录。

响应为 `code/message/data`，记录位于 `data.records`，包括 `stock_code`、`stock_name`、`holder_name`、变动数量/比例、变动后持股及起止日期、公告日期等字段。
