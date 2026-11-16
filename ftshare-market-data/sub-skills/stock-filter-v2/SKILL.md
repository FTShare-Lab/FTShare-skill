---
name: stock-filter-v2
description: "A 股实时行情筛选接口：可按 symbol 精确查单标的，或按 board（板块/交易所）与 listing_date_since（上市日期起点）筛选；传 symbol 时忽略后两者。用户问按板块筛股票、某板块有哪些标的、上市日期过滤时使用。"
---

# 股票筛选

接口：GET `/api/v2/market/data/stock-list/filter`。参数和响应以 [《股票筛选》](https://market.ft.tech/gateway/doc/pages/r7bgm5w0.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 否 | 单标的代码（如 `600519`、`600519.SH`）；传入后忽略 board 与 listing_date_since |
| `--board` | 否 | 板块/交易所筛选：`star` / `chi_next` / `bjse` / `xshg` / `xshe` / `main` |
| `--listing_date_since` | 否 | 上市日期起点 YYYYMMDD，筛选此后上市的股票 |
| `--page` | 否 | 页码 |
| `--page_size` | 否 | 每页条数 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`type`、`symbol`、`symbol_id`、`symbol_name`、`board`、`close`、`open`、`high`、`low`、`prev_close`、`change`、`change_rate`、`amplitude`、`volume`、`turnover`、`change_rate_day5`、`change_rate_day10`、`change_rate_day20` …共 21 个

## 调用示例

```bash
python <RUN_PY> stock-filter-v2 --symbol 600519.SH --page 1
```
