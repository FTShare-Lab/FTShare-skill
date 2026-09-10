---
name: ths-industry-daily-flow
description: 查询同花顺行业板块资金流日度。用户问同花顺行业板块资金流、行业板块每日净流入、行业资金流向、领涨股涨跌幅时使用。
---

# 同花顺行业板块资金流日度

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 同花顺行业板块资金流日度 |
| 外部接口 | `GET /api/v1/market/data/ths-industry-daily-flow` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 按日期范围查询同花顺行业板块日度资金流，含板块指数、涨跌幅、流入/流出/净额、领涨股及涨跌幅 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| start_date | string | 否 | 开始日期 | 20260805 | YYYYMMDD |
| end_date | string | 否 | 结束日期 | 20260805 | YYYYMMDD |
| board_name | string | 否 | 行业板块名称，精确匹配 | 证券 | 不能是空白字符串；不传返回日期范围内全部行业板块 |
| page | int | 否 | 页码 | 1 | - |
| page_size | int | 否 | 每页条数 | 100 | - |

## 3. 响应说明

返回分页结构。records 元素核心字段：`board_name`（行业板块名称）、`trade_date`、`board_index`（板块指数，可为 null）、`change_pct`、`company_count`、`inflow`、`outflow`、`net_amount`、`leader_name`、`leader_change_pct`、`leader_price`。

## 4. 调用方式

```bash
python <RUN_PY> ths-industry-daily-flow --start-date 20260805 --end-date 20260805 --board-name 证券 --page 1 --page-size 100
python <RUN_PY> ths-industry-daily-flow --start-date 20260801 --end-date 20260805 --page 1 --page-size 100
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 板块名称参数为 `board_name`（原 `sector_name` 已更名，不再使用旧参数名），输出字段同步为 `board_name` / `board_index`。
- 结果按 `trade_date` 降序、`board_name` 升序排列。
- 源数据缺项返回 `null`，接口不做聚合、单位转换或缺失值补算。
