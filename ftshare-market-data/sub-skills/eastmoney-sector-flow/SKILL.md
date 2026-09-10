---
name: eastmoney-sector-flow
description: 查询东方财富板块资金流（行业/概念/地域日资金流）。用户问东财板块资金流、板块主力净流入、行业/概念/地域资金流向、BK 板块代码资金流、超大单大单净流入时使用。
---

# 东方财富板块资金流

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 东方财富板块资金流（get_eastmoney_sector_flow） |
| 外部接口 | `GET /api/v1/market/data/eastmoney-sector-flow` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 获取东方财富板块（行业/概念/地域）日资金流，含主力/超大单/大单/中单/小单净流入及净占比；支持按板块代码、板块类型、行业层级、交易日或日期区间过滤 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| board_code | string | 否 | 板块代码 | BK0488 | 东财板块代码，BK 开头 |
| board_type | string | 否 | 板块类型 | industry | industry（行业）/ concept（概念）/ regional（地域） |
| board_level | int | 否 | 行业层级 | 2 | 1=一级、2=二级、3=三级；不传返回全部层级，仅匹配 industry |
| trade_date | string | 否 | 交易日 | 20260623 | YYYYMMDD |
| start_date | string | 否 | 区间起始日 | 20260601 | YYYYMMDD |
| end_date | string | 否 | 区间结束日 | 20260630 | YYYYMMDD |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 50 | 默认 50，最大 500 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为分页对象：`pageNum` / `pageSize` / `total` / `pages` / `records`。

records 元素核心字段：`board_code`、`board_name`、`board_type`（industry/concept/regional）、`board_level`（industry 为 1/2/3，concept/regional 为 0）、`trade_date`（YYYYMMDD），以及 `main_net`/`main_pct`、`super_large_net`/`super_large_pct`、`large_net`/`large_pct`、`medium_net`/`medium_pct`、`small_net`/`small_pct`（净流入单位亿元，净占比单位 %）。

## 4. 调用方式

```bash
python <RUN_PY> eastmoney-sector-flow --board-type industry --board-level 2 --page 1 --page-size 5
python <RUN_PY> eastmoney-sector-flow --board-code BK0488 --trade-date 20260623
python <RUN_PY> eastmoney-sector-flow --board-type concept --start-date 20260601 --end-date 20260630
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 请求参数为 `board_code` / `board_type` / `board_level`（原 `sector_code` / `sector_type` / `sector_level` 已更名，不再使用旧参数名）。
- 概念和地域板块的层级为 0，传入 `board_level` 时不会匹配 concept/regional 数据。
- `trade_date`、`start_date`、`end_date` 可同时使用，按全部条件过滤。
