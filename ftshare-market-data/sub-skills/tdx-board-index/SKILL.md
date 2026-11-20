---
name: tdx-board-index
description: "查询最新一期通达信板块指数快照，返回板块指数价格、昨收、涨速及领涨证券信息，无需传入日期。接口：GET /api/v1/market/data/tdx-board-index。"
---

# 通达信板块指数最新快照

接口：GET `/api/v1/market/data/tdx-board-index`。参数和响应以 [《通达信板块指数最新快照》](https://market.ft.tech/gateway/doc/pages/tuzgkfun.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--ts_code` | 否 | TDX 板块代码，精确匹配 |
| `--board_name` | 否 | 板块名称，精确匹配 |
| `--board_type` | 否 | 板块类型，精确匹配，常见值：`HY`、`HY2`、`GN`、`FG`、`DQ` |
| `--board_type_code` | 否 | 板块类型枚举原始值，精确匹配，范围 0–255 |
| `--market` | 否 | TDX 市场代码原始值，精确匹配，范围 0–255 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`ts_code`、`board_name`、`board_type`、`board_type_code`、`market`、`price`、`rise_speed`、`pre_close`、`lead_market`、`lead_code`、`lead_name`、`lead_price`、`lead_rise_speed`、`lead_pre_close`

## 调用示例

```bash
python <RUN_PY> tdx-board-index --page 1
```
