---
name: economic-china-fiscal-revenue-monthly
description: Get China fiscal revenue monthly data (中国财政收入月度). Use when user asks about 中国财政收入, 财政收入月度, 财政收支, fiscal revenue, 当月同比环比, 累计财政收入.
---

# 中国经济 - 财政收入（月度）

## 参数

无需任何参数。

## 用法

直接执行：

```bash
python script/handler.py
```

脚本输出 JSON 数组，按时间倒序，每项含 `month`（如 2025年03月份）、`revenue_current`（当月财政收入）、`yoy`（当月同比 %）、`mom`（当月环比 %）、`cumulative`（累计）、`cumulative_yoy`（累计同比 %）、`unit`（亿元）、`currency`（CNY），以表格展示给用户。

## 注意

- 返回按月份汇总，格式如「2025年03月份」
- 数值单位见 `unit`（亿元），同比/环比单位为 %
- 列表已按时间倒序，最新月份在前

## 调用示例

```bash
python <RUN_PY> economic-china-fiscal-revenue-monthly
```
