---
name: stock-comment-index
description: 查询东方财富千股千评综合诊断主表（market.ft.tech），含收盘价、涨跌幅、换手率、市盈率、主力成本、机构参与度、综合评分、排名、关注指数。用户问千股千评、股票综合诊断、股票评分排名时使用。
---

# 千股千评主表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 千股千评综合诊断主表 |
| 外部接口 | `GET /api/v1/market/data/stock-comment/index` |
| 请求方式 | GET |
| 适用场景 | 查询东方财富千股千评综合诊断主表，获取全市场股票的综合评分与排名 |

## 2. 请求参数

无参数，返回全量数据。

## 3. 响应说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| data.total | int | 否 | 总记录数 |
| data.items[].seq | int | 否 | 序号 |
| data.items[].security_code | string | 否 | 股票代码 |
| data.items[].security_name_abbr | string | 是 | 股票简称 |
| data.items[].trade_date | string | 是 | 交易日期 |
| data.items[].close_price | string | 是 | 收盘价 |
| data.items[].change_rate | string | 是 | 涨跌幅 |
| data.items[].turnover_rate | string | 是 | 换手率 |
| data.items[].pe_dynamic | string | 是 | 动态市盈率 |
| data.items[].prime_cost | string | 是 | 主力成本 |
| data.items[].org_participate | string | 是 | 机构参与度 |
| data.items[].total_score | string | 是 | 综合评分 |
| data.items[].rank | string | 是 | 当前排名 |
| data.items[].focus | string | 是 | 关注指数 |

## 4. 用法

```bash
python <RUN_PY> stock-comment-index
```

## 5. 注意事项

- 返回全量数据（约 5000+ 条），数据量较大，**可能因响应过大导致服务端截断**（HTTP/2 限制）。如遇到 JSON 解析失败，说明数据被截断，需等服务端修复或通过单股接口（`stock-comment-score` / `stock-comment-focus` 等）按个股查询。
- 数值类字段以字符串形式返回以保持精度。
