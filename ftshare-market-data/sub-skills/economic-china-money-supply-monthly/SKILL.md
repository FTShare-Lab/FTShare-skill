---
name: economic-china-money-supply-monthly
description: Get China money supply monthly data (货币供应量 M0/M1/M2 月度). Use when user asks about M0, M1, M2, 货币供应量, 广义货币, 狭义货币, 中国货币供应, China money supply.
---

# 中国经济 - 货币供应量（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 货币供应量（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-money-supply |
| 请求方式 | GET |
| 适用场景 | 获取中国 M0、M1、M2 货币供应量月度数据，含当月值、同比、环比等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`m2_current`/`m2_yoy`/`m2_mom`（M2 当月及同比、环比）、`m1_current`/`m1_yoy`/`m1_mom`（M1）、`m0_current`/`m0_yoy`/`m0_mom`（M0）、`unit`（亿元）、`currency`（CNY），以表格展示给用户。

## 4. 响应说明

返回值为货币供应量月度计算结果列表，按时间倒序。

### MoneySupplyComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| m2_current | float | 是 | M2 当月数量 | 见 unit |
| m2_yoy | float | 是 | M2 同比增长 | % |
| m2_mom | float | 是 | M2 环比增长 | % |
| m1_current | float | 是 | M1 当月数量 | 见 unit |
| m1_yoy | float | 是 | M1 同比增长 | % |
| m1_mom | float | 是 | M1 环比增长 | % |
| m0_current | float | 是 | M0 当月数量 | 见 unit |
| m0_yoy | float | 是 | M0 同比增长 | % |
| m0_mom | float | 是 | M0 环比增长 | % |
| unit | String | 否 | 货币单位 | - |
| currency | String | 否 | 货币种类 | - |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-money-supply
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- 金额单位见 `unit`（通常为亿元），同比/环比单位为 %，各数值字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-money-supply-monthly
```
