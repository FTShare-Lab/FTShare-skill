---
name: stock-institution-holdings
description: "查询 A 股指定报告期机构持股汇总信息。接口：GET /api/v2/market/data/share/stock-institution-holdings。"
---

# 机构持股

接口：GET `/api/v2/market/data/share/stock-institution-holdings`。参数和响应以 [《机构持股》](https://market.ft.tech/gateway/doc/pages/nrsskpy6.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--year` | 是 | 年份 |
| `--report_type` | 是 | 报告类型：q1 / q2 / q3 / annual / announcement |
| `--institution_type` | 是 | 机构类型，仅支持 all_inst |
| `--page` | 否 | 页码，默认 1 |
| `--page_size` | 否 | 每页条数，默认 20 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`stock_code`、`stock_name`、`report_type`、`year`、`institution_type`、`total_institution_count`、`holding_shares`、`market_value`、`change_type`、`change_shares`、`change_shares_ratio`

## 调用示例

```bash
python <RUN_PY> stock-institution-holdings --year 2025 --report_type annual --institution_type all_inst --page 1 --page_size 5
```
