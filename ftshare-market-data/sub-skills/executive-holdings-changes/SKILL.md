---
name: executive-holdings-changes
description: 查询董监高持股变动明细。用户询问董监高、高管持股变动、增持减持、变动股数或变动日期时使用。
---

# 董监高持股变动

接口：`GET /api/v1/market/data/holder/stock-ggmx`。支持按股票代码、变动方向和变动日期范围筛选，返回分页数据。

## 调用示例

```bash
python <RUN_PY> executive-holdings-changes --stock-code 600001 --change-direction 增持 --start-date 20260101 --end-date 20260601 --page 1 --page-size 20
python <RUN_PY> executive-holdings-changes --stock-code 600519 --all
```

## 参数

- `--stock-code`：股票代码，如 `600001`，可选。
- `--change-direction`：变动方向，可填 `增持` 或 `减持`，可选。
- `--start-date`：变动日期起始日，可使用 `YYYYMMDD` 或 `YYYY-MM-DD`，可选。
- `--end-date`：变动日期截止日，可使用 `YYYYMMDD` 或 `YYYY-MM-DD`，可选。
- `--page`：页码，默认 1。
- `--page-size`：每页条数，默认 50，范围为 1～200。
- `--all`：自动翻页并合并所有记录。

所有筛选参数均可省略。响应为 `code/message/data` 信封，分页记录位于 `data.records`。

## 记录字段

记录包含 `stock_code`、`stock_name`、`change_date`、`notice_date`、`register_date`、`changer`、`executive_name`、`relation`、`position`、`change_direction`、`change_shares`、`change_quantity`、`avg_price`、`change_amount`、`change_reason`、`shares_after`、`change_ratio`、`close_price`、`price_change`、`total_share`、`data_time`、`quote_price`、`quote_change`、`crawl_date`、`source` 和 `crawl_batch_ts` 等字段。

日期参数按变动日期筛选；源接口同时兼容下划线参数名及对应的 camelCase 别名，handler 使用文档中的下划线参数名。
