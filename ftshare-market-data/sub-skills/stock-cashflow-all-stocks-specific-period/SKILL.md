---
name: stock-cashflow-all-stocks-specific-period
description: Get cash flow statement (现金流量表) for all stocks in a specific reporting period. Use when user asks about 指定报告期现金流量表, 全市场现金流量表, all stocks cashflow for a specific year and period.
---

# 查询单报告期全市场现金流量表（分页）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单报告期所有票现金流量表 |
| 外部接口 | GET /api/v1/market/data/finance/cashflow |
| 请求方式 | GET |
| 适用场景 | 获取 A 股指定报告期所有股票的现金流量表，支持沪深京股票，支持分页 |

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
  "items": [ { "stock_code", "stock_name", "year", "report_type", "report_type_cn", "publish_date", "detail_report_type", "cash_equ_inc", ... } ],
  "total_pages": 279,
  "total_items": 5565
}
```

### 字段说明（CashflowItem）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| stock_code | String | 否 | 股票交易代码，带 .SZ/.SH/.BJ 后缀 | - |
| stock_name | String | 否 | 上市公司股票名称 | - |
| year | int | 否 | 报告所属年度 | - |
| report_type | String | 否 | 报告期类型：q1/q2/q3/annual | - |
| report_type_cn | String | 否 | 报告期类型中文：一季报/半年报/三季报/年报 | - |
| publish_date | String | 否 | 报告发布日期，YYYY-MM-DD | - |
| detail_report_type | String | 否 | 报告明细类型：合并未调整/合并调整 | - |
| cash_equ_inc | float | 否 | 现金及现金等价物净增加额（核心净现金流） | 元 |
| cash_equ_inc_yoy | float | 是 | 净现金流同比增长率，无上期时为 null | % |
| net_oper_cash_flow | float | 否 | 经营活动产生的现金流量净额 | 元 |
| net_oper_cash_flow_ratio | float | 是 | 经营性现金流量净额占净现金流比例 | % |
| goods_sale_render_service_cash | float | 否 | 销售商品、提供劳务收到的现金 | 元 |
| goods_sale_render_service_cash_ratio | float | 是 | 销售商品、提供劳务收到现金占净现金流比例 | % |
| net_invest_cash_flow | float | 否 | 投资活动产生的现金流量净额 | 元 |
| net_invest_cash_flow_ratio | float | 是 | 投资性现金流量净额占净现金流比例 | % |
| invest_proceeds | float | 否 | 取得投资收益收到的现金 | 元 |
| invest_proceeds_ratio | float | 是 | 取得投资收益收到现金占净现金流比例 | % |
| fix_intan_long_pay_cash | float | 否 | 购建固定资产、无形资产等长期资产支付的现金 | 元 |
| fix_intan_long_pay_cash_ratio | float | 是 | 购建长期资产支付现金占净现金流比例 | % |
| net_fin_cash_flow | float | 否 | 筹资活动产生的现金流量净额 | 元 |
| net_fin_cash_flow_ratio | float | 是 | 融资性现金流量净额占净现金流比例 | % |

## 注意事项

- report_type 取值：q1（一季报）、q2（半年报）、q3（三季报）、annual（年报）。
- 需要全量数据时，按 page 递增请求直到 page > total_pages。

## 调用示例

```bash
python <RUN_PY> stock-cashflow-all-stocks-specific-period --year 2025 --report-type annual --page 1 --page-size 5
```
