---
name: convertible-bond-szse-negotiated-trades
description: "查询深交所可转债协议成交公开信息。可用参数：--security-code、--trade-date、--page、--page-size。接口：GET /api/v1/market/data/convertible-bond/szse/negotiated-trades。"
---

# 深交所可转债协议成交

接口：`GET /api/v1/market/data/convertible-bond/szse/negotiated-trades`。在线文档：[《深交所可转债协议成交》](https://market.ft.tech/gateway/doc/pages/s3qatfk2.md)

外部接口：`GET /api/v1/market/data/convertible-bond/szse/negotiated-trades`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--security-code` | 否 | 六位可转债证券代码，例如 `123001`。 |
| `--trade-date` | 否 | 单个交易日，格式 `YYYYMMDD`；不能与 `start_date`、`end_date` 同时使用。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page-size` | 否 | 每页条数，默认 `50`，最大 `200`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`security_code`、`security_name`、`turnover_10k_yuan`、`face_value_million_yuan`、`negotiated_detail_api`、`after_hours_detail_api`、`summary_detail_api`、`created_at`

## 调用示例

```bash
python <RUN_PY> convertible-bond-szse-negotiated-trades --page 1 --page-size 5
```
