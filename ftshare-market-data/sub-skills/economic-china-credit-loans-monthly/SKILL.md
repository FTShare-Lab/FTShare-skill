---
name: economic-china-credit-loans-monthly
description: Get China credit/loans monthly data (中国信贷数据 月度). Use when user asks about 信贷, 新增信贷, 信贷数据, 中国信贷, 贷款增量, China credit loans, 社会融资.
---

# 中国经济 - 信贷（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 信贷数据（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-credit-loans |
| 请求方式 | GET |
| 适用场景 | 获取中国信贷数据月度汇总，含新增信贷、同比、环比、当年累计及累计同比等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`new_loans`（本月新增信贷）、`yoy`（同比 %）、`mom`（环比 %）、`cumulative`（当年累计）、`cumulative_yoy`（累计同比 %）、`unit`（亿元）、`currency`（CNY），以表格展示给用户。

## 4. 响应说明

返回值为信贷月度计算结果列表，按时间倒序。

### CreditComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| new_loans | float | 是 | 本月新增信贷 | 见 unit |
| yoy | float | 是 | 同比增长 | % |
| mom | float | 是 | 环比增长 | % |
| cumulative | float | 是 | 当年累计（1 月到当前月之和） | 见 unit |
| cumulative_yoy | float | 是 | 累计同比增长 | % |
| unit | String | 否 | 货币单位 | - |
| currency | String | 否 | 货币种类 | - |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-credit-loans
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- 金额单位见 `unit`（通常为亿元），同比/环比单位为 %，各数值字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-credit-loans-monthly
```
