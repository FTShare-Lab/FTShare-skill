---
name: stk-alert-broker
description: "查询交易所重点提示证券及提示有效期间。接口：GET /api/v2/market/data/stk-alert-broker。同义：打板。"
---

# 交易所重点提示证券

接口：GET `/api/v2/market/data/stk-alert-broker`。参数和响应以 [《交易所重点提示证券》](https://market.ft.tech/gateway/doc/pages/pp359u6x.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--ts_code` | 否 | 证券代码，精确匹配，例如 `513310.SH`。 |
| `--start_date` | 否 | 查询区间起始日期，格式 `YYYYMMDD`，需与 `end_date` 一起传入。 |
| `--end_date` | 否 | 查询区间结束日期，格式 `YYYYMMDD`，需与 `start_date` 一起传入。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page_size` | 否 | 每页数量，默认 `100`，范围 `1`–`1000`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`ts_code`、`name`、`start_date`、`end_date`、`type`

## 调用示例

```bash
python <RUN_PY> stk-alert-broker --page 1
```
