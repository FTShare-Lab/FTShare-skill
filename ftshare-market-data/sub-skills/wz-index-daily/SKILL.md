---
name: wz-index-daily
description: "按日期范围查询温州民间融资综合利率指数及分项利率。可用参数：--start_date、--end_date、--page、--page_size。接口：GET /api/v1/market/data/wz-index-daily。"
---

# 温州民间融资综合利率指数日度

接口：GET `/api/v1/market/data/wz-index-daily`。参数和响应以 [《温州民间融资综合利率指数日度》](https://market.ft.tech/gateway/doc/pages/e4w9tgm2.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start_date` | 是 | 开始日期，格式 YYYYMMDD |
| `--end_date` | 是 | 结束日期，格式 YYYYMMDD，不能早于 start_date |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`date`、`comp_rate`、`center_rate`、`micro_rate`、`sdb_rate`、`m1_rate`、`m3_rate`、`m6_rate`、`m12_rate`、`long_rate`、`market`、`pawnshop`、`farmer`、`folk`、`finance`、`finance_lease`、`commercial_factoring`、`one_day`、`one_week`

## 调用示例

```bash
python <RUN_PY> wz-index-daily --start_date 20260828 --end_date 20260828 --page 1
```
