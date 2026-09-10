---
name: etf-share
description: 查询 ETF 份额变动（etf_share）。用户问 ETF 份额、期末份额、申购赎回份额、份额净变动、份额变动率、ETF 份额历史时使用。
---

# ETF 份额变动

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | ETF 份额（etf_share） |
| 外部接口 | `GET /api/v2/market/data/etf-share` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 按 ETF 代码分页查询份额变动：统计周期、统计日期、期末/期初份额、申购/赎回份额、份额净变动和份额变动率，支持按统计周期和日期范围筛选 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf_code | string | 是 | ETF 代码 | 510300 | 兼容参数名 `fund_code`，建议使用 `etf_code` |
| stati_perd | string | 否 | 统计周期 | 全部 | `日`/`季度`/`年度`/`截止时点`/`半年`/`全部`；不传默认 `全部` |
| start_date | int | 否 | 开始日期 | 20250101 | YYYYMMDD，按 `trade_date` 过滤 |
| end_date | int | 否 | 结束日期 | 20260909 | YYYYMMDD，按 `trade_date` 过滤；不早于 `start_date` |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 50 | 默认 50，最大 200 |
| --all | - | 否 | 自动翻页拉全量 | - | 仅本子 skill 扩展参数 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为分页对象：`items`（列表）、`total_pages`、`total_items`。

items 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| trade_code | string | ETF 交易代码 |
| statistics_period | string | 统计周期 |
| trade_date | int | 统计日期 YYYYMMDD |
| fund_share | string | 期末份额（份） |
| begin_shares | string / null | 期初份额（份） |
| purchase_shares | string / null | 申购份额（份） |
| redemption_shares | string / null | 赎回份额（份） |
| shares_change | string / null | 份额净变动（份） |
| shares_change_ratio | string / null | 份额变动率（%） |

## 4. 调用方式

```bash
python <RUN_PY> etf-share --etf-code 510300 --page 1 --page-size 5
python <RUN_PY> etf-share --etf-code 510300 --stati-perd 日 --start-date 20250101 --end-date 20260909
python <RUN_PY> etf-share --etf-code 510300 --all
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 份额字段单位为份；数值字段以字符串形式返回，以保留小数精度。
- `start_date` / `end_date` 可单独提供；同时提供时 `start_date` 不得晚于 `end_date`。
- `--all` 会按 `total_pages` 自动翻页，把所有 `items` 合并为一个数组返回。
