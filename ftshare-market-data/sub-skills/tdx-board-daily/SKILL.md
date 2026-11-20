---
name: tdx-board-daily
description: "按日期范围查询通达信板块日线，返回板块标识、板块类型、开高低收、成交量和成交额等原始字段。接口：GET /api/v1/market/data/tdx-board-daily。"
---

# 通达信板块日线

接口：GET `/api/v1/market/data/tdx-board-daily`。参数和响应以 [《通达信板块日线》](https://market.ft.tech/gateway/doc/pages/otlferf5.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start_date` | 是 | 开始日期，格式 YYYYMMDD |
| `--end_date` | 是 | 结束日期，格式 YYYYMMDD，不能早于 start_date |
| `--ts_code` | 否 | TDX 板块代码，精确匹配 |
| `--board_name` | 否 | 板块名称，精确匹配 |
| `--board_type` | 否 | 板块类型，精确匹配，常见值：`HY`、`HY2`、`GN`、`FG`、`DQ` |
| `--board_type_code` | 否 | 板块类型枚举原始值，精确匹配，范围 0–255 |
| `--market` | 否 | TDX K 线市场代码原始值，精确匹配，范围 0–255；板块日线当前通常为 1 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`ts_code`、`board_name`、`board_type`、`board_type_code`、`market`、`open`、`high`、`low`、`close`、`vol`、`amount`、`float_shares`

## 调用示例

```bash
python <RUN_PY> tdx-board-daily --start_date 20260828 --end_date 20260828 --page 1
```
