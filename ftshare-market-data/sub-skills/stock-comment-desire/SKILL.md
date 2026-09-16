---
name: stock-comment-desire
description: 查询指定股票的千股千评市场参与意愿及5日均值变化（market.ft.tech）。用户问市场参与意愿、散户参与度时使用。
---

# 千股千评 — 市场参与意愿

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 市场参与意愿 |
| 外部接口 | `GET /api/v1/market/data/stock-comment/desire` |
| 请求方式 | GET |
| 适用场景 | 查询指定股票的市场参与意愿及 5 日均值变化 |

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
| data.items[].security_code | string | 是 | 股票代码 |
| data.items[].participation_wish | string | 是 | 参与意愿 |
| data.items[].participation_wish_5days | string | 是 | 5 日平均参与意愿 |
| data.items[].participation_wish_change | string | 是 | 参与意愿变化 |
| data.items[].participation_wish_5days_change | string | 是 | 5 日平均参与意愿变化 |

## 4. 用法

```bash
python <RUN_PY> stock-comment-desire --symbol 000001
```

## 5. 注意事项

- `symbol` 为 6 位数字股票代码，不带交易所后缀。
- 意愿指数字段以字符串形式返回以保持精度。
