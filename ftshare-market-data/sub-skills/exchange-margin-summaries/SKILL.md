---
name: exchange-margin-summaries
description: "查询交易所融资融券汇总日度数据。用户询问沪深北交易所融资融券余额、买入额、偿还额或融券数据时使用。同义：两融。"
---

# 交易所融资融券汇总日度

接口：`GET /api/v1/market/data/exchange-margin-summaries`。在线文档：[《交易所融资融券汇总日度》](https://market.ft.tech/gateway/doc/pages/1gb9y7b9.md)

外部接口：`GET /api/v1/market/data/exchange-margin-summaries`

必填：`--start-date`、`--end-date`（YYYYMMDD）。可选：`--exchange`、`--page`、`--page-size`、`--all`。

```bash
python <RUN_PY> exchange-margin-summaries --start-date 20260701 --end-date 20260731 --page 1 --page-size 100
```

返回分页 JSON，记录位于 `records`，包含 `exchange`、`trade_date`、`rzye`、`rzmre`、`rzche`、`rqyl`、`rqylje`、`rqmcl`、`rzrqjyzl`。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start-date` | 是 | 开始日期，格式 YYYYMMDD |
| `--end-date` | 是 | 结束日期，格式 YYYYMMDD，不能早于 start_date |
| `--exchange` | 否 | 交易所代码，精确匹配，不能是空白字符串 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`exchange`、`trade_date`、`rzye`、`rzmre`、`rzche`、`rqyl`、`rqylje`、`rqmcl`、`rzrqjyzl`
