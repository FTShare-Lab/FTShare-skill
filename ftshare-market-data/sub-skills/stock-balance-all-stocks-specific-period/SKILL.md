---
name: stock-balance-all-stocks-specific-period
description: Get balance sheet (资产负债表) for all stocks in a specific reporting period. Use when user asks about 指定报告期资产负债表, 全市场资产负债表, all stocks balance sheet for a specific year and period.
---

# 查询单报告期全市场资产负债表（分页）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单报告期所有票资产负债表 |
| 外部接口 | GET /api/v1/market/data/finance/balance |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定报告期所有股票的资产负债表，支持沪深京股票，支持分页 |

## 请求参数

说明：year、report_type、page、page_size 为必填项。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| year | int | 是 | 报告所属年度 | 2025 | 必填 |
| report_type | string | 是 | 报告期类型标识 | q2 | q1（一季报）、q2（半年报）、q3（三季报）、annual（全年报） |
| page | int | 是 | 页码 | 1 | 从 1 开始 |
| page_size | int | 是 | 每页记录数 | 20 | 建议 10–100 |

## 执行方式

```bash
python scripts/handler.py --year 2025 --report-type q2 --page 1 --page-size 20
```

## 响应结构

```json
{
  "items": [ { "stock_code", "stock_name", "publish_date", "year", "report_type", "report_type_cn", "report_form_type", "t_assets", "t_equity", "asset_liability_ratio", ... } ],
  "total_pages": 279,
  "total_items": 5565
}
```

### 字段说明（BalanceItem）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| stock_code | String | 否 | 股票交易代码，带 .SZ/.SH/.BJ 后缀 | - |
| stock_name | String | 否 | 上市公司股票名称 | - |
| publish_date | String | 否 | 报告发布日期，YYYY-MM-DD | - |
| year | int | 否 | 报告所属年度 | - |
| report_type | String | 否 | 报告期类型：q1/q2/q3/annual | - |
| report_type_cn | String | 否 | 报告期类型中文：一季报/半年报/三季报/年报 | - |
| report_form_type | String | 否 | 报表类型：合并未调整/合并调整 | - |
| t_assets | float | 否 | 资产总计 | 元 |
| total_assets_yoy | float | 是 | 总资产同比增长率，无上期时为 null | % |
| t_fixed_assets | float | 否 | 固定资产合计 | 元 |
| cash_equivalents | float | 否 | 货币资金 | 元 |
| monetary_funds_yoy | float | 是 | 货币资金同比增长率 | % |
| account_receivable | float | 否 | 应收账款 | 元 |
| accounts_receivable_yoy | float | 是 | 应收账款同比增长率 | % |
| inventory | float | 否 | 存货 | 元 |
| inventory_yoy | float | 是 | 存货同比增长率 | % |
| t_liability | float | 否 | 负债总计 | 元 |
| total_liabilities_yoy | float | 是 | 总负债同比增长率 | % |
| accounts_payable | float | 否 | 应付账款 | 元 |
| accounts_payable_yoy | float | 是 | 应付账款同比增长率 | % |
| advance_receipts | float | 是 | 预收账款 | 元 |
| advance_receipts_yoy | float | 是 | 预收账款同比增长率 | % |
| t_equity | float | 否 | 所有者权益合计 | 元 |
| total_equity_yoy | float | 是 | 所有者权益合计同比增长率 | % |
| asset_liability_ratio | float | 是 | 资产负债率（衍生） | % |

## 注意事项

- report_type 取值：q1（一季报）、q2（半年报）、q3（三季报）、annual（年报）。
- 需要全量数据时，按 page 递增请求直到 page > total_pages。

## 调用示例

```bash
python <RUN_PY> stock-balance-all-stocks-specific-period --year 2025 --report-type annual --page 1 --page-size 5
```
