---
name: economic-china-tax-revenue-monthly
description: Get China tax revenue monthly data (全国税收收入 月度). Use when user asks about 全国税收收入, 税收收入, 税收月度, 中国税收, China tax revenue.
---

# 中国经济 - 全国税收收入（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 全国税收收入（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-tax-revenue |
| 请求方式 | GET |
| 适用场景 | 获取中国全国税收收入月度数据，含当月值、累计值、累计同比、月度环比、月度同比等 |

## 2. 请求参数

说明：该接口无需请求参数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| - | - | - | 无需参数 | - | - |

## 3. 用法

直接执行：

```bash
python script/handler.py
```

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年05月）、`monthly_revenue`（当月税收，亿元）、`cumulative_revenue`（累计税收，亿元）、`yoy_growth`（累计同比 %）、`mom_growth`（月度环比 %）、`monthly_yoy_growth`（月度同比 %），以表格展示给用户。

## 4. 响应说明

返回值为全国税收收入月度计算结果列表，按时间倒序。

### TaxRevenueComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年05月 | - |
| monthly_revenue | float | 是 | 税收收入合计当月值 | 亿元 |
| cumulative_revenue | float | 是 | 税收收入合计累计值 | 亿元 |
| yoy_growth | float | 是 | 税收收入合计累计同比 | % |
| mom_growth | float | 是 | 月度环比（(当月值 - 上月值) / 上月值 × 100） | % |
| monthly_yoy_growth | float | 是 | 月度同比（(当月值 - 去年同月值) / 去年同月值 × 100） | % |

注：金额单位为亿元。

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-tax-revenue
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年05月」，列表已按时间倒序，最新月份在前。
- 金额单位为亿元，同比/环比单位为 %，各数值字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-tax-revenue-monthly
```
