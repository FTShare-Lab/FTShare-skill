---
name: economic-china-cpi-monthly
description: Get China CPI monthly data (居民消费价格指数 月度). Use when user asks about CPI, 居民消费价格指数, 消费价格指数, 中国CPI, 全国CPI, 城市农村CPI, China CPI.
---

# 中国经济 - 居民消费价格指数（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 居民消费价格指数（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-cpi |
| 请求方式 | GET |
| 适用场景 | 获取中国居民消费价格指数 CPI 月度汇总数据，含全国/城市/农村当月值及同比、环比等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`national_cpi`/`national_yoy`/`national_mom`（全国 CPI 及同比、环比）、`cumulative`（累计）、`city_cpi`/`city_yoy`/`city_mom`（城市）、`rural_cpi`/`rural_yoy`/`rural_mom`（农村），以表格展示给用户。

## 4. 响应说明

返回值为居民消费价格指数月度计算结果列表，按时间倒序。

### ComputedCpi 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 月份，格式如 2025年03月份 | - |
| national_cpi | float | 是 | 全国 CPI 当月值 | - |
| national_yoy | float | 是 | 全国同比 | % |
| national_mom | float | 是 | 全国环比 | % |
| cumulative | float | 是 | 累计值 | - |
| city_cpi | float | 是 | 城市 CPI 当月值 | - |
| city_yoy | float | 是 | 城市同比 | % |
| city_mom | float | 是 | 城市环比 | % |
| rural_cpi | float | 是 | 农村 CPI 当月值 | - |
| rural_yoy | float | 是 | 农村同比 | % |
| rural_mom | float | 是 | 农村环比 | % |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-cpi
```

## 6. 注意事项

- 返回按月份汇总，格式如「2025年03月份」，列表已按时间倒序，最新月份在前。
- CPI 为指数（基期 100），同比/环比单位为 %，各数值字段可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-cpi-monthly
```
