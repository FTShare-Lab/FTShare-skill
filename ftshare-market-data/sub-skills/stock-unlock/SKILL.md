---
name: stock-unlock
description: "按证券代码查询限售解禁批次及股东明细，或按解禁日期范围查询全市场批次，批次维度分页。接口：GET /api/v1/market/data/unlock/stock_unlock。"
---

# 限售解禁

接口：GET `/api/v1/market/data/unlock/stock_unlock`。参数和响应以 [《限售解禁》](https://market.ft.tech/gateway/doc/pages/a3qlyxpp.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--stock-code` | 否 | 证券代码；与日期范围互斥 |
| `--start-date` | 否 | 解禁日期起始值；需与 `end_date` 同时传入 |
| `--end-date` | 否 | 解禁日期结束值；需与 `start_date` 同时传入 |
| `--page` | 否 | 页码，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`stockCode`、`stockName`、`unlockDate`、`holderCount`、`ableFreeShares`、`currentFreeShares`、`nonFreeShares`、`liftMarketCap`、`totalRatio`、`freeRatio`、`newPrice`、`freeSharesType`、`b20Adjchrate`、`a20Adjchrate`、`crawlDate`、`source`、`holders`、`holderName` …共 24 个

## 调用示例

查询条件二选一：传 `--stock-code`，或同时传 `--start-date` 与 `--end-date`；两种模式不能混用。

按证券代码查询单票解禁批次：

```bash
python <RUN_PY> stock-unlock --stock-code 000001 --page 1 --page_size 10
```

按解禁日期区间查询全市场解禁日历：

```bash
python <RUN_PY> stock-unlock --start-date 20260901 --end-date 20260930 --page 1 --page_size 100
```
