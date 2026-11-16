---
name: wallstreetcn-financial-calendar
description: "查询华尔街见闻（wallstreetcn）财经日历，按日期范围返回该区间内的经济事件。可用参数：--start_date、--end_date、--page、--page_size。接口：GET /api/v1/market/data/finance/financial-calendar/wallstreetcn。"
---

# 华尔街见闻财经日历

接口：GET `/api/v1/market/data/finance/financial-calendar/wallstreetcn`。参数和响应以 [《华尔街见闻财经日历》](https://market.ft.tech/gateway/doc/pages/jvg7kkmv.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start_date` | 是 | 起始日期，格式为 `YYYYMMDD` |
| `--end_date` | 是 | 结束日期，格式为 `YYYYMMDD`（与 start_date 间隔 ≤ 3 天） |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`stat_date`、`tab_type`、`event_time`、`region`、`event`、`importance`、`actual_value`、`forecast_value`、`previous_value`、`link`

## 调用示例

```bash
python <RUN_PY> wallstreetcn-financial-calendar --start_date 20260828 --end_date 20260828 --page 1
```
