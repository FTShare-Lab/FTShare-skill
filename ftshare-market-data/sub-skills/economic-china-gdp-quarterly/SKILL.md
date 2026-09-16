---
name: economic-china-gdp-quarterly
description: Get China GDP quarterly data (中国 GDP 季度数据). Use when user asks about 中国 GDP, 季度 GDP, 三次产业, 中国经济 GDP, China GDP quarterly, GDP 同比, 第一二三产业.
---

# 中国经济 - GDP（季度）

## 参数

无需任何参数。

## 用法

直接执行：

```bash
python script/handler.py
```

脚本输出 JSON 数组，按时间倒序，每项含 `period`（如 2025年第1-4季度）、`gdp`、`gdp_yoy`（GDP 同比 %）、`primary`/`secondary`/`tertiary`（三次产业值）及对应累计同比、`unit`（亿元）、`currency`（人民币），以表格展示给用户。

## 注意

- 返回按 `period` 季度汇总，如「2025年第1季度」「2025年第1-3季度」「2025年第1-4季度」
- 数值单位见 `unit`（亿元），同比类字段单位为 %
- 列表已按时间倒序，最新季度在前

## 调用示例

```bash
python <RUN_PY> economic-china-gdp-quarterly
```
