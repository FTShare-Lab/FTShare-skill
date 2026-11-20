---
name: sw-industry-daily-metrics
description: "查询单个申万行业的日频估值/资金/量价指标时间序列，包含 PE（LYR/TTM 及分位/中位数）、PB、股息率、换手率、总市值、收盘价、破净比例、指数收盘、成交额及拥挤度等共 42 项字段，其中部分字段可能为 null。接口：GET /api/v1/market/data/sw-industry/daily-metrics。"
---

# 申万行业日度指标

接口：GET `/api/v1/market/data/sw-industry/daily-metrics`。参数和响应以 [《申万行业日度指标》](https://market.ft.tech/gateway/doc/pages/9p19gdz0.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--level` | 否 | 行业层级：1/2/3；不传按 industry_code 自动匹配层级 |
| `--start_date` | 是 | 起始日期，YYYYMMDD |
| `--end_date` | 是 | 截止日期，YYYYMMDD |
| `--industry_code` | 是 | 行业代码，带 .SI 后缀，如 801010.SI |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`industryCode`、`industryName`、`tradeDate`、`lyrPe`、`lyrPeQuantile`、`ttmPe`、`ttmPeQuantile`、`pb`、`pbQuantile`、`dvRatio`、`dvRatioQuantile`、`dvTtm`、`dvTtmQuantile`、`addLyrPe`、`addLyrPeQuantile`、`addTtmPe`、`addTtmPeQuantile`、`addPb` …共 42 个

## 调用示例

```bash
python <RUN_PY> sw-industry-daily-metrics --start_date 20260828 --end_date 20260828 --industry_code 801010.SI --page 1
```
