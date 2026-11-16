---
name: stock-reports
description: 查询 A 股研报列表。按 stock-code 查询个股历史，或按 type 与日期范围查询；page 和 page-size 必填。
---

# 研报列表

接口：`GET /api/v2/market/data/report/stock-reports`。在线文档：[《研报列表》](https://market.ft.tech/gateway/doc/pages/g7615auf.md)

外部接口：`GET /api/v2/market/data/report/stock-reports`。

支持两种模式：

- 按个股查询：`--stock-code`，`--type` 可省略，传入时必须为 `StockReport`。
- 按类型和日期查询：不传 `--stock-code` 时，必须提供 `--type` 与 `--start-date`；`--end-date` 可省略，日期范围最多 3 天。

`--page` 与 `--page-size` 必填。返回 `code`、`message` 和分页 `data`，记录含研报评级、研究机构、研究员及用于下载正文的 `url_hash`。所有请求必须设置 `FTSHARE_API_KEY`，缺失凭据时不会发起请求。

```bash
python <RUN_PY> stock-reports --stock-code 600036.SH --page 1 --page-size 20
python <RUN_PY> stock-reports --type MacroReport --start-date 20260821 --page 1 --page-size 20
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--stock-code` | 否 | 证券代码（带交易所后缀，如 `600036.SH`、`000001.SZ`、`920258.BJ`）。按个股查询所有年份时使用 |
| `--type` | 否 | 研报类型：`StockReport` / `MacroReport` / `IndustryReport` / `BrokerMorningReport` / `StrategyReport` / `NewStockReport`（不区分大小写）。按 `stock_code` 查询时可选（缺省为 `StockReport`，若传必须为 `StockReport`）；未传 `stock_code` 时必选 |
| `--start-date` | 否 | 开始日期 YYYYMMDD。未传 `stock_code` 时必选，最多支持 3 天查询区间 |
| `--end-date` | 否 | 结束日期 YYYYMMDD。选填，未传 `stock_code` 且不传 `end_date` 时默认等于 `start_date` |
| `--page` | 是 | 页码（从 1 开始） |
| `--page-size` | 是 | 每页条数 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`stock_code`、`stock_name`、`report_id`、`report_title`、`report_time`、`report_institution`、`report_rating_name`、`report_rating_value`、`last_report_rating_name`、`last_report_rating_value`、`rating_change`、`rating_researcher`、`url_hash`
