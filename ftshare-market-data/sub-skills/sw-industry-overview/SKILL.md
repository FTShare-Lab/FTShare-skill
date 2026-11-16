---
name: sw-industry-overview
description: "按交易日查询申万行业全部层级（一、二、三级行业）的估值概况快照，含成份股数、PE（LYR/TTM）及历史分位、PB 及分位、股息率及分位。可用参数：--date、--level、--page、--page_size。接口：GET /api/v1/market/data/sw-industry/overview。"
---

# 申万行业总览

接口：GET `/api/v1/market/data/sw-industry/overview`。参数和响应以 [《申万行业总览》](https://market.ft.tech/gateway/doc/pages/x1q1shn7.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--date` | 是 | 交易日，格式 YYYYMMDD |
| `--level` | 否 | 行业层级：1/2/3，不传返回全部 |
| `--page` | 否 | 页码，默认 1，从 1 开始 |
| `--page_size` | 否 | 每页数量，默认 50，上限 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`industryCode`、`industryName`、`level`、`parentIndustryName`、`constituentCount`、`tradeDate`、`lyrPe`、`lyrPePercentile`、`ttmPe`、`ttmPePercentile`、`pb`、`pbPercentile`、`dvRatio`、`dvRatioPercentile`

## 调用示例

```bash
python <RUN_PY> sw-industry-overview --date 20260828 --page 1 --level 1
```
