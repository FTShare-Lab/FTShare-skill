---
name: economic-china-customs-trade-monthly
description: Get China customs import/export monthly data (海关进出口 月度). Use when user asks about 海关进出口, 出口, 进口, 进出口, 外贸, 中国出口进口, China customs trade.
---

# 中国经济 - 海关进出口（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 海关进出口增减情况（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-customs-trade |
| 请求方式 | GET |
| 适用场景 | 获取中国海关进出口月度数据，含出口/进口当月值、同比、环比及累计与累计同比等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`export_current`/`export_yoy`/`export_mom`（当月出口及同比、环比）、`import_current`/`import_yoy`/`import_mom`（当月进口）、`cumulative_export`/`cumulative_export_yoy`、`cumulative_import`/`cumulative_import_yoy`（累计及同比）、`unit`、`currency`，以表格展示给用户。

## 4. 响应说明

返回值为海关进出口月度计算结果列表，按时间倒序。

### CustomsTradeComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| export_current | float | 是 | 当月出口额 | 见 unit |
| export_yoy | float | 是 | 当月出口额同比 | % |
| export_mom | float | 是 | 当月出口额环比 | % |
| import_current | float | 是 | 当月进口额 | 见 unit |
| import_yoy | float | 是 | 当月进口额同比 | % |
| import_mom | float | 是 | 当月进口额环比 | % |
| cumulative_export | float | 是 | 累计出口额 | 见 unit |
| cumulative_export_yoy | float | 是 | 累计出口额同比 | % |
| cumulative_import | float | 是 | 累计进口额 | 见 unit |
| cumulative_import_yoy | float | 是 | 累计进口额同比 | % |
| unit | String | 否 | 货币单位 | - |
| currency | String | 否 | 货币种类 | - |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-customs-trade
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- 金额单位见 `unit`（通常为亿美元），同比/环比单位为 %，各数值字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-customs-trade-monthly
```
