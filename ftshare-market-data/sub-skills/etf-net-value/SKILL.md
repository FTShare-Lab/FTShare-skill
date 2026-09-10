---
name: etf-net-value
description: 查询 ETF 历史净值（etf_net_value）。用户问 ETF 净值、单位净值、累计净值、净值增长率、复权净值、每万份收益、7 日年化收益率时使用。
---

# ETF 历史净值

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | ETF 净值（etf_net_value） |
| 外部接口 | `GET /api/v2/market/data/etf-net-value` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 按 ETF 代码分页查询历史净值：发布日、净值日期、资产净值、单位净值、累计净值、净值增长率、复权净值、每万份收益、7 日年化收益率；支持单日或日期区间查询 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf_code | string | 是 | ETF 代码 | 510300 | 兼容参数名 `fund_code`，建议使用 `etf_code` |
| nav_date | int | 二选一 | 净值日期 | 20260909 | YYYYMMDD；与日期区间参数互斥 |
| start_date | int | 二选一 | 净值开始日期 | 20260901 | 须与 `end_date` 同时提供 |
| end_date | int | 二选一 | 净值结束日期 | 20260909 | 须与 `start_date` 同时提供 |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 50 | 默认 50，最大 200 |
| --all | - | 否 | 自动翻页拉全量 | - | 仅本子 skill 扩展参数 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为分页对象：`items`（列表）、`total_pages`、`total_items`。

items 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| trade_code | string | ETF 交易代码 |
| publish_date | int | 发布日期 YYYYMMDD |
| nav_date | int | 净值日期 YYYYMMDD |
| net_asset | string | 资产净值 |
| unit_nav | string | 单位净值 |
| unit_nav_growth | string | 单位净值增长率（%） |
| accumulated_nav | string | 累计单位净值 |
| adjustment_factor | string | 复权因子 |
| adjusted_unit_nav | string | 复权单位净值 |
| adjusted_unit_nav_growth | string | 复权单位净值增长率（%） |
| daily_profit | string | 每万份基金收益 |
| seven_day_annualized_return | string | 7 日年化收益率（%） |

## 4. 调用方式

```bash
python <RUN_PY> etf-net-value --etf-code 510300 --nav-date 20260909
python <RUN_PY> etf-net-value --etf-code 510300 --start-date 20260901 --end-date 20260909 --page 1 --page-size 5
python <RUN_PY> etf-net-value --etf-code 510300 --start-date 20260801 --end-date 20260909 --all
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 必须提供 `nav_date`，或同时提供 `start_date` 和 `end_date`；二者互斥（handler 会在本地校验并拒绝）。
- 日期格式 YYYYMMDD；区间查询包含开始和结束日期，`start_date` 不得晚于 `end_date`。
- 数值字段以字符串形式返回，以保留小数精度。
- `--all` 会按 `total_pages` 自动翻页，把所有 `items` 合并为一个数组返回。
