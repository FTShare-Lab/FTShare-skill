---
name: economic-china-reserve-ratio-monthly
description: Get China reserve requirement ratio monthly data (存款准备金率 月度). Use when user asks about 存款准备金率, 准备金率, 大型金融机构准备金率, 中小型金融机构准备金率, China reserve ratio.
---

# 中国经济 - 存款准备金率（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 准备金率（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-reserve-ratio |
| 请求方式 | GET |
| 适用场景 | 获取中国人民币存款准备金率月度数据，含大型与中小型金融机构准备金率等 |

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

脚本输出 JSON 数组，按时间倒序，每项含 `date`（如 2025年12月）、`reserve_ratio_small_medium`（中小型金融机构准备金率 %）、`reserve_ratio_large`（大型金融机构准备金率 %），以表格展示给用户。

## 4. 响应说明

返回值为准备金率按日期计算结果列表，按时间倒序。

### ReserveRatioComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| date | String | 否 | 日期，格式如 2025年12月 | - |
| reserve_ratio_small_medium | float | 是 | 准备金率中小型金融机构 | % |
| reserve_ratio_large | float | 是 | 准备金率大型金融机构 | % |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-reserve-ratio
```

## 6. 注意事项

- 返回按日期汇总（通常为调准日所在月份），格式如「2025年12月」，列表已按时间倒序，最新在前。
- 准备金率单位为 %，各数值字段可为 null；仅当央行调整时会有新记录。

## 调用示例

```bash
python <RUN_PY> economic-china-reserve-ratio-monthly
```
