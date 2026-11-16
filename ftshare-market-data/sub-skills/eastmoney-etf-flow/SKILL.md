---
name: eastmoney-etf-flow
description: "查询东方财富 ETF 日资金流。接口：GET /api/v1/market/data/eastmoney-etf-flow。用户问 ETF 资金流、ETF 主力净流入、ETF 超大单/大单/中单/小单净流入及净占比时使用。"
---

# 东方财富 ETF 资金流

接口：GET `/api/v1/market/data/eastmoney-etf-flow`。参数和响应以 [《东方财富ETF资金流》](https://market.ft.tech/gateway/doc/pages/nh3wc690.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 请求参数

| 参数 | 是否必填 | 说明 |
|---|---|---|
| `--symbol` | 否 | ETF 代码，如 `159231`；也接受带交易所后缀的写法，如 `159231.SZ` |
| `--trade_date` | 否 | 交易日，格式 `YYYYMMDD` |
| `--start_date` | 否 | 区间起始日，格式 `YYYYMMDD`；需与 `--end_date` 同时提供 |
| `--end_date` | 否 | 区间结束日，格式 `YYYYMMDD`；需与 `--start_date` 同时提供 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页条数，默认 100，范围 1–1000 |

`trade_date`、`start_date`、`end_date` 按 AND 条件组合过滤；结果按交易日倒序、代码升序排列。不传任何日期条件时返回接口全部可用记录，数据从 20260316 起。

## 响应说明

返回 `code`/`message`/`data` 信封，`data` 为分页对象：`pageNum`、`pageSize`、`total`、`pages`、`records`。

`records` 每行字段：

| 字段 | 说明 |
|---|---|
| `code` | ETF 六位代码 |
| `trade_date` | 交易日期，`YYYYMMDD` |
| `close` | 收盘价，单位元 |
| `change_pct` | 涨跌幅，单位 % |
| `main_net` / `main_pct` | 主力净流入（元）/ 主力净占比（%） |
| `xl_net` / `xl_pct` | 超大单净流入（元）/ 净占比（%） |
| `l_net` / `l_pct` | 大单净流入（元）/ 净占比（%） |
| `m_net` / `m_pct` | 中单净流入（元）/ 净占比（%） |
| `s_net` / `s_pct` | 小单净流入（元）/ 净占比（%） |

## 调用示例

```bash
python <RUN_PY> eastmoney-etf-flow --symbol 159231.SZ --start_date 20260920 --end_date 20260921 --page 1 --page_size 2
```
