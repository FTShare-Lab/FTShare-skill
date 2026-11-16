---
name: chinabond-yield-daily
description: "按日期范围查询中债收益率曲线日度数据。接口：GET /api/v1/market/data/chinabond-yield-daily。"
---

# 中债收益率曲线日度

接口：GET `/api/v1/market/data/chinabond-yield-daily`。参数和响应以 [《中债收益率曲线日度》](https://market.ft.tech/gateway/doc/pages/fubopatp.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start_date` | 是 | 开始日期，格式 YYYYMMDD |
| `--end_date` | 是 | 结束日期，格式 YYYYMMDD，不能早于 start_date |
| `--curve_name` | 否 | 收益率曲线名称，精确匹配，不能是空白字符串 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`curve_name`、`trade_date`、`y_3m`、`y_6m`、`y_1y`、`y_3y`、`y_5y`、`y_7y`、`y_10y`、`y_30y`

## 调用示例

```bash
python <RUN_PY> chinabond-yield-daily --start_date 20260828 --end_date 20260828 --page 1
```
