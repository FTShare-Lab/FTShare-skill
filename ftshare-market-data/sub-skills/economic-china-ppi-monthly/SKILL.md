---
name: economic-china-ppi-monthly
description: Get China PPI monthly data (中国 PPI 工业品出厂价格指数 月度). Use when user asks about PPI, 工业品出厂价格指数, 生产者价格指数, 中国PPI, China PPI, 工业品价格.
---

# 中国经济 - PPI（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | PPI 数据（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-ppi |
| 请求方式 | GET |
| 适用场景 | 获取中国工业品出厂价格指数 PPI 月度数据，含当月值、同比、环比及当年累计平均等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`ppi`（当月工业品出厂价格指数）、`yoy`（同比 %）、`mom`（环比 %）、`cumulative_avg`（当年累计平均），以表格展示给用户。

## 4. 响应说明

返回值为 PPI 月度计算结果列表，按时间倒序。

### PpiComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| ppi | float | 是 | 当月工业品出厂价格指数 | - |
| yoy | float | 是 | 同比增长 | % |
| mom | float | 是 | 环比增长 | % |
| cumulative_avg | float | 是 | 当年累计平均（1 月到当前月平均） | - |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-ppi
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- PPI 为指数（基期 100），同比/环比单位为 %，各字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-ppi-monthly
```
