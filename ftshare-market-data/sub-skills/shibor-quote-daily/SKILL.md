---
name: shibor-quote-daily
description: "按日期范围查询 Shibor 报价行日度报价。接口：GET /api/v1/market/data/shibor-quote-daily。"
---

# SHIBOR报价日度

接口：GET `/api/v1/market/data/shibor-quote-daily`。参数和响应以 [《SHIBOR报价日度》](https://market.ft.tech/gateway/doc/pages/optr82sd.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start_date` | 是 | 开始日期，格式 YYYYMMDD |
| `--end_date` | 是 | 结束日期，格式 YYYYMMDD，不能早于 start_date |
| `--bank` | 否 | 报价行名称，精确匹配，不能是空白字符串 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`bank`、`bank_en`、`on_rate`、`w1`、`w2`、`m1`、`m3`、`m6`、`m9`、`y1`

## 调用示例

```bash
python <RUN_PY> shibor-quote-daily --start_date 20260828 --end_date 20260828 --page 1 --bank 汇丰银行
```
