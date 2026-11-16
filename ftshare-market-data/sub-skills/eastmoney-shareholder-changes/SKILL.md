---
name: eastmoney-shareholder-changes
description: 查询东方财富股东增减持。Use when user asks about 股东增持、股东减持或东方财富股东变动。
---

# 东方财富股东增减持

接口：`GET /api/v1/market/data/holder/stock-ggcg-em`。通过 `symbol` 筛选全部、股东增持或股东减持，返回分页明细。在线文档：[《东方财富股东增减持》](https://market.ft.tech/gateway/doc/pages/t9hrpidk.md)

```bash
python <RUN_PY> eastmoney-shareholder-changes --symbol 全部 --page 1 --page-size 20
python <RUN_PY> eastmoney-shareholder-changes --symbol 股东减持 --all
```

- `--symbol`：可选，`全部`、`股东增持` 或 `股东减持`，默认全部。
- `--page`：页码，默认 1。
- `--page-size`：每页条数，默认 50，最大 200。
- `--all`：自动翻页合并全部记录。

响应为 `code/message/data`，记录位于 `data.records`，包括 `stock_code`、`stock_name`、`holder_name`、变动数量/比例、变动后持股及起止日期、公告日期等字段。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 否 | 数据类型：全部 / 股东增持 / 股东减持，默认全部 |
| `--page` | 否 | 页码，默认 1 |
| `--page-size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`stock_code`、`stock_name`、`latest_price`、`price_change_rate`、`holder_name`、`change_num_symbol`、`change_num`、`change_total_ratio`、`change_free_ratio`、`after_holder_num`、`hold_ratio`、`free_shares`、`free_shares_ratio`、`start_date`、`end_date`、`notice_date`
