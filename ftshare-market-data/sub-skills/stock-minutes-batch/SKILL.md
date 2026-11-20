---
name: stock-minutes-batch
description: "批量查询多只 A 股的历史分钟 K 线（1 分钟及多分钟周期），含开高低收、成交量额、换手率与复权处理；必填 --symbols（逗号分隔）及起止毫秒时间戳。"
---

# 批量股票历史分钟行情

接口：`GET /api/v2/market/data/stock_minutes/batch`。必填 `--symbols`、`--since-ts-millis`、`--until-ts-millis`；`--symbols` 使用逗号分隔，最多 20 只；可选 `--interval-value`、`--limit`，时间跨度不超过 30 个北京时间自然日（包含起止日期），`limit` 范围 1~1000，省略 `limit` 时返回范围内全部记录。在线文档：[《批量股票历史分钟行情》](https://market.ft.tech/gateway/doc/pages/n12sln7b.md)

```bash
python <RUN_PY> stock-minutes-batch --symbols 600519.SH,000001.SZ --since-ts-millis 1788919020000 --until-ts-millis 1788920820000 --limit 5
```

返回 `code/message/data`，`data` 为每只标的的 `symbol`、`total` 和 `items` 列表；不是分页接口。每根 K 线字段：open / high / low / close / ts_millis / ts_millis_open / turnover / volume / turnover_rate（换手率）。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbols` | 是 | 逗号分隔的股票代码列表（1~20只，如 `600519.SH,000001.SZ`；兼容重复参数） |
| `--interval-value` | 否 | 分钟周期数值，必须大于 0 的整数；缺省为 `1`（1 分钟 K 线） |
| `--adjust-kind` | 否 | 复权类型：`None`（默认，不复权）/ `Forward`（前复权）/ `Backward`（后复权） |
| `--since-ts-millis` | 是 | 开始时间戳（毫秒）；与 until_ts_millis 跨度不超过 30 个北京时间自然日（包含起止日期） |
| `--until-ts-millis` | 是 | 结束时间戳（毫秒） |
| `--limit` | 否 | 每只标的的返回条数上限（1~1000）；不传时返回查询范围内全部记录 |

## 返回

- 返回：`data` 为记录数组（无外层容器，直接遍历）
- 分页字段：`total`
- 记录字段：`symbol`、`open`、`high`、`low`、`close`、`ts_millis`、`ts_millis_open`、`turnover`、`volume`、`turnover_rate`
