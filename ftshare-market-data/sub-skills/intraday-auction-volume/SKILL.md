---
name: intraday-auction-volume
description: "查询单只标的的连续竞价成交量/成交额占比分时序列（按分钟）。不传 --trade-date 返回当日实时，传入历史日期返回当日分时；必填 --symbol。"
---

# 单标的连续竞价成交量

接口：`GET /api/v1/market/data/intraday-auction-volume/symbol`。必填 `--symbol`；可选 `--trade-date`（YYYYMMDD）、`--page` 和 `--page-size`，每页最多 200 条。在线文档：[《单标的连续竞价成交量》](https://market.ft.tech/gateway/doc/pages/bskofshl.md)

```bash
python <RUN_PY> intraday-auction-volume --symbol 600000.SH --page 1 --page-size 50
```

不传交易日查询当日实时数据，传入历史交易日查询历史分钟数据；响应为 `code/message/data` 分页信封，分钟记录位于 `data.records`。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 是 | 标的代码，格式 code.suffix（XSHG/SH、XSHE/SZ、BJSE/BJ） |
| `--trade-date` | 否 | 交易日期 YYYYMMDD；不传返回当日实时数据 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页数量，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`ts_millis`、`volume`、`volume_ratio`、`turnover`、`turnover_ratio`
