---
name: economic-china-industrial-added-value-monthly
description: Get China industrial added value growth monthly data (工业增加值增长 月度). Use when user asks about 工业增加值, 工业增加值同比, 工业增长, 中国工业, China industrial added value.
---

# 中国经济 - 工业增加值（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 中国工业增加值增长（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-industrial-added-value |
| 请求方式 | GET |
| 适用场景 | 获取中国工业增加值月度数据，含同比增长、累计同比增长等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`yoy`（同比增长 %）、`cumulative_yoy`（累计同比增长 %），以表格展示给用户。

## 4. 响应说明

返回值为工业增加值月度计算结果列表，按时间倒序。

### IndustrialAddedValueComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| yoy | float | 是 | 同比增长 | % |
| cumulative_yoy | float | 是 | 累计同比增长 | % |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-industrial-added-value
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- 同比单位为 %，各数值字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-industrial-added-value-monthly
```
