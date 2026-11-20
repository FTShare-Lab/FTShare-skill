---
name: stock-institution-holdings-detail
description: "查询 A 股单票机构持仓详细信息。接口：GET /api/v2/market/data/share/stock-institution-holdings-detail。"
---

# 机构持股明细

接口：GET `/api/v2/market/data/share/stock-institution-holdings-detail`。参数和响应以 [《机构持股明细》](https://market.ft.tech/gateway/doc/pages/ov1vnlsg.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--stock_code` | 是 | 股票代码 |
| `--year` | 是 | 年份 |
| `--report_type` | 是 | 报告类型：q1 / q2 / q3 / annual / announcement |
| `--institution_type` | 是 | 机构类型，仅支持 all_inst |
| `--page` | 否 | 页码，默认 1 |
| `--page_size` | 否 | 每页条数，默认 20 |

## 返回

- 记录容器：`data.items`
- 分页字段：`total_pages`、`total_items`、`total_pages`、`page_size`、`total_pages`、`page_size`（`total_pages` 依赖 `page_size`）
- 记录字段：`stock_code`、`stock_name`、`end_date`、`report_type`、`year`、`institution_type`、`institution_id`、`institution_main_id`、`institution_name`、`holding_shares`、`market_value`、`net_value_ratio`、`circulating_shares`、`total_shares`

## 调用示例

```bash
python <RUN_PY> stock-institution-holdings-detail --stock_code 600519 --year 2025 --report_type annual --institution_type all_inst --page 1 --page_size 5
```
