---
name: eastmoney-dapan-flow
description: "获取东方财富大盘指数（沪深两市）日资金流数据，含主力/超大单/大单/中单/小单五档净流入及净占比，以及上证/深证收盘价与涨跌幅。接口：GET /api/v1/market/data/eastmoney-dapan-flow。"
---

# 东方财富大盘资金流

接口：GET `/api/v1/market/data/eastmoney-dapan-flow`。参数和响应以 [《东方财富大盘资金流》](https://market.ft.tech/gateway/doc/pages/v32o6wwz.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade_date` | 否 | 交易日 YYYYMMDD |
| `--start_date` | 否 | 区间起始日 YYYYMMDD |
| `--end_date` | 否 | 区间结束日 YYYYMMDD |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 500 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_date`、`sh_close`、`sh_change_pct`、`sz_close`、`sz_change_pct`、`main_net`、`main_pct`、`xlarge_net`、`xlarge_pct`、`large_net`、`large_pct`、`mid_net`、`mid_pct`、`small_net`、`small_pct`、`name`

## 调用示例

```bash
python <RUN_PY> eastmoney-dapan-flow --page 1 --trade_date 20260828
```
