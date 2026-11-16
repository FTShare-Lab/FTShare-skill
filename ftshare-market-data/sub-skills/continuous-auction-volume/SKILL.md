---
name: continuous-auction-volume
description: 查询全市场连续竞价成交量和成交额占比。用户询问全市场、沪深北市场的分时成交占比时使用。
---

# 连续竞价成交量

接口：`GET /api/v2/market/data/intraday-auction-volume`。可选 `--trade-date`（YYYYMMDD）、`--page` 和 `--page-size`，每页最多 200 条；支持 `--all` 自动翻页。在线文档：[《连续竞价成交量》](https://market.ft.tech/gateway/doc/pages/6xp6q54v.md)

```bash
python <RUN_PY> continuous-auction-volume --trade-date 20260918 --page 1 --page-size 50
```

不传交易日查询当日实时全市场聚合数据，传入历史交易日查询历史数据；响应为 `code/message/data` 分页信封，分钟记录位于 `data.records`，包含 overall、xshg、xshe 和 bjse 四个市场维度。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-date` | 否 | 交易日期 YYYYMMDD；不传返回当日实时数据 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页数量，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`ts_millis`、`overall`、`xshg`、`xshe`、`bjse`、`volume`、`volume_ratio`、`turnover`、`turnover_ratio`
