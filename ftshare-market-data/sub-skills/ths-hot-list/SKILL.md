---
name: ths-hot-list
description: "查询同花顺股票、ETF、债券、港股、美股、公募基金和期货热榜，支持按交易日分页查询。可用参数：--list_type、--trade_date、--page、--page_size。接口：GET /api/v1/market/data/ths-hot-list。"
---

# 同花顺热榜

接口：GET `/api/v1/market/data/ths-hot-list`。参数和响应以 [《同花顺热榜》](https://market.ft.tech/gateway/doc/pages/fbvl8umv.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--list_type` | 是 | 榜单类型，可选值见下表。 |
| `--trade_date` | 否 | 交易日期，格式为 `YYYYMMDD`；不传时使用最新有数据的交易日。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page_size` | 否 | 每页条数，默认 `100`，取值范围为 `1` 到 `200`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`rank`、`name`、`hotValue`、`riseAndFall`

## 调用示例

```bash
python <RUN_PY> ths-hot-list --list_type stock_day --page 1
```
