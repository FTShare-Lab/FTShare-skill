---
name: sw-index-history-minutes
description: "按指数代码与日期区间查询申万指数的一分钟 K 线历史行情，返回分页结构（指数代码/名称、交易时间、开高低收、成交量额），支持 --all 自动翻页。"
---

# 申万指数历史分钟 K 线

接口：`GET /api/v1/market/data/sw-index/history-minutes`。必填 `--index-code`、`--start-date`、`--end-date`；可选 `--page` 和 `--page-size`（最大 200），支持 `--all` 自动翻页。在线文档：[《申万指数历史分钟K线》](https://market.ft.tech/gateway/doc/pages/vltgbxfw.md)

```bash
python <RUN_PY> sw-index-history-minutes --index-code 801001 --start-date 20260811 --end-date 20260811 --page 1 --page-size 50
```

返回 `code/message/data` 分页信封，分钟记录位于 `data.records`。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--index-code` | 是 | 申万指数代码，如 `801001`；也可带 `.SI` 后缀，如 `801001.SI` |
| `--start-date` | 是 | 起始日期，格式 `YYYYMMDD`，包含当天 |
| `--end-date` | 是 | 截止日期，格式 `YYYYMMDD`，包含当天 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页数量，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`index_code`、`index_name`、`trade_time`、`open`、`high`、`low`、`close`、`amount`、`volume`
