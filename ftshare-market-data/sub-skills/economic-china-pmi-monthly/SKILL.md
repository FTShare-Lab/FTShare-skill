---
name: economic-china-pmi-monthly
description: Get China PMI monthly data (中国 PMI 月度). Use when user asks about PMI, 制造业PMI, 非制造业PMI, 中国PMI, 采购经理指数, China PMI, manufacturing PMI.
---

# 中国经济 - PMI（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | PMI 数据（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-pmi |
| 请求方式 | GET |
| 适用场景 | 获取中国制造业与非制造业 PMI 月度数据，含当月值、同比、环比等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`manufacturing_pmi`（制造业 PMI）、`manufacturing_yoy`/`manufacturing_mom`（制造业同比/环比 %）、`non_manufacturing_pmi`（非制造业 PMI）、`non_manufacturing_yoy`/`non_manufacturing_mom`（非制造业同比/环比 %），以表格展示给用户。

## 4. 响应说明

返回值为 PMI 月度计算结果列表，按时间倒序。

### PmiComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| manufacturing_pmi | float | 是 | 制造业 PMI | - |
| manufacturing_yoy | float | 是 | 制造业同比 | % |
| manufacturing_mom | float | 是 | 制造业环比 | % |
| non_manufacturing_pmi | float | 是 | 非制造业 PMI | - |
| non_manufacturing_yoy | float | 是 | 非制造业同比 | % |
| non_manufacturing_mom | float | 是 | 非制造业环比 | % |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-pmi
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- PMI 为指数（通常 50 为荣枯线），同比/环比单位为 %，各字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-pmi-monthly
```
