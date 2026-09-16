---
name: stock-income-all-stocks-specific-period
description: Get income statement (利润表) for all stocks in a specific reporting period. Use when user asks about 指定报告期利润表, 全市场利润表, all stocks income for a specific year and period.
---

# 查询单报告期全市场利润表（分页）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单报告期所有票利润表 |
| 外部接口 | GET /api/v1/market/data/finance/income |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定报告期所有股票的利润表，支持沪深京股票，支持分页 |

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
  "items": [ { "stock_code", "stock_name", "year", "report_type", "report_type_cn", "publish_date", "report_form_type", "t_revenue", "n_profit", ... } ],
  "total_pages": 283,
  "total_items": 5652
}
```

### 字段说明（IncomeItem）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| stock_code | String | 否 | 股票交易代码，带 .SZ/.SH/.BJ 后缀 | - |
| stock_name | String | 否 | 上市公司股票名称 | - |
| year | int | 否 | 报告所属年度 | - |
| report_type | String | 否 | 报告期类型：q1/q2/q3/annual | - |
| report_type_cn | String | 否 | 报告期类型中文：一季报/半年报/三季报/年报 | - |
| publish_date | String | 否 | 报告发布日期，YYYY-MM-DD | - |
| report_form_type | String | 否 | 报表类型：合并未调整/合并调整 | - |
| t_revenue | float | 否 | 营业总收入 | 元 |
| t_revenue_yoy | float | 是 | 营业总收入同比增长率，无上期时为 null | % |
| cost | float | 否 | 营业支出（主营业务成本） | 元 |
| cost_yoy | float | 是 | 主营业务成本同比增长率 | % |
| t_cost | float | 否 | 营业总支出 | 元 |
| t_cost_yoy | float | 是 | 营业总支出同比增长率 | % |
| sale_expense | float | 否 | 销售费用 | 元 |
| sale_expense_yoy | float | 是 | 销售费用同比增长率 | % |
| manag_expense | float | 否 | 管理费用 | 元 |
| manag_expense_yoy | float | 是 | 管理费用同比增长率 | % |
| financial_cost | float | 否 | 财务费用 | 元 |
| financial_cost_yoy | float | 是 | 财务费用同比增长率 | % |
| profit | float | 否 | 营业利润 | 元 |
| profit_yoy | float | 是 | 营业利润同比增长率 | % |
| t_profit | float | 否 | 利润总额 | 元 |
| t_profit_yoy | float | 是 | 利润总额同比增长率 | % |
| n_profit | float | 否 | 净利润 | 元 |
| n_profit_yoy | float | 是 | 净利润同比增长率 | % |
| parcomp_n_profit | float | 否 | 扣非归母净利润 | 元 |
| parcomp_n_profit_yoy | float | 是 | 扣非归母净利润同比增长率 | % |

## 注意事项

- report_type 取值：q1（一季报）、q2（半年报）、q3（三季报）、annual（年报）。
- 需要全量数据时，按 page 递增请求直到 page > total_pages。

## 调用示例

```bash
python <RUN_PY> stock-income-all-stocks-specific-period --year 2025 --report-type annual --page 1 --page-size 5
```
