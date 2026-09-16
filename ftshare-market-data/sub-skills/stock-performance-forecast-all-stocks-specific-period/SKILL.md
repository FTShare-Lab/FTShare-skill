---
name: stock-performance-forecast-all-stocks-specific-period
description: Get performance forecast (业绩预告) for all stocks in a specific reporting period. Use when user asks about 指定报告期业绩预告, 全市场业绩预告, all stocks performance forecast for a specific year and period.
---

# 查询指定报告期全市场业绩预告（分页）

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--year` | int | 是 | 报告所属年度 | `2024` |
| `--report-type` | string | 是 | 报告期类型：`q1`/`q2`/`q3`/`annual` | `annual` |
| `--page` | int | 否 | 页码，从 1 开始（默认 1） | `1` |
| `--page-size` | int | 否 | 每页记录数（默认 20） | `20` |

## 用法

从用户问题中提取年度和报告期类型，执行：

```bash
python scripts/handler.py --year 2024 --report-type annual --page 1 --page-size 20
```

脚本输出带分页信息的 JSON，每项含 `stock_code`、`stock_name`、`forecast_type`、`net_profit_min`、`net_profit_max`、`net_profit_yoy` 等字段，以表格展示给用户。

## 注意

- `report-type` 取值：`q1`（一季报）、`q2`（中报）、`q3`（三季报）、`annual`（年报）
- 需要全量数据时，循环请求直到 `page > total_pages`

## 调用示例

```bash
python <RUN_PY> stock-performance-forecast-all-stocks-specific-period --year 2025 --report-type annual --page 1 --page-size 5
```
