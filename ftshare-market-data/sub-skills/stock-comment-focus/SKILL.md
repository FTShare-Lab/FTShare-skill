---
name: stock-comment-focus
description: 查询指定股票的千股千评市场热度用户关注指数及排名变动（market.ft.tech）。用户问用户关注指数、市场关注度排名时使用。
---

# 千股千评 — 市场热度用户关注指数

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 市场热度用户关注指数 |
| 外部接口 | `GET /api/v1/market/data/stock-comment/focus` |
| 请求方式 | GET |
| 适用场景 | 查询指定股票的用户关注指数、排名及变动情况 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 股票代码 | `000001` | 6 位数字代码，不带交易所后缀 |

## 3. 响应说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| data.symbol | string | 否 | 股票代码 |
| data.total | int | 否 | 总记录数 |
| data.items[].trade_date | string | 是 | 交易日期 |
| data.items[].market_focus | string | 是 | 市场关注度 |
| data.items[].market_focus_rank | string | 是 | 关注度排名 |
| data.items[].total_market | string | 是 | 全市场关注度 |
| data.items[].market_focus_change | string | 是 | 关注度变动 |
| data.items[].close_price | string | 是 | 收盘价 |

## 4. 用法

```bash
python <RUN_PY> stock-comment-focus --symbol 000001
```

## 5. 注意事项

- `symbol` 为 6 位数字股票代码，不带交易所后缀。
- 指数及价格字段以字符串形式返回以保持精度。
