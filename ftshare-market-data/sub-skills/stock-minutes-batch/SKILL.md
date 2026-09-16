---
name: stock-minutes-batch
description: 批量查询 股票历史分钟 K 线。用户询问多只股票的分钟行情时使用。
---

# 批量股票历史分钟行情

接口：`GET /api/v2/market/data/stock_minutes/batch`。必填 `--symbols`、`--since-ts-millis`、`--until-ts-millis`；`--symbols` 使用逗号分隔，最多 20 只；可选 `--interval-value`、`--limit`，时间跨度不超过 3 天，`limit` 范围 1~1000。

```bash
python <RUN_PY> stock-minutes-batch --symbols 600519.SH,000001.SZ --since-ts-millis 1788919020000 --until-ts-millis 1788920820000 --limit 5
```

返回 `code/message/data`，`data` 为每只标的的 `symbol`、`total` 和 `items` 列表；不是分页接口。每根 K 线字段：open / high / low / close / ts_millis / ts_millis_open / turnover / volume / turnover_rate（换手率）。
