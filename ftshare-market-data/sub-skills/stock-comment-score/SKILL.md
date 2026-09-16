---
name: stock-comment-score
description: 查询指定股票的千股千评历史综合评分走势（market.ft.tech）。用户问某股票历史评分、综合评分走势时使用。
---

# 千股千评 — 综合评价历史评分

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 综合评价历史评分 |
| 外部接口 | `GET /api/v1/market/data/stock-comment/score` |
| 请求方式 | GET |
| 适用场景 | 查询指定股票的历史综合评分走势 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 股票代码 | `000001` | 6 位数字代码，不带交易所后缀 |

## 3. 响应说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| data.symbol | string | 否 | 股票代码 |
| data.total | int | 否 | 总记录数 |
| data.items[].diagnose_date | string | 是 | 诊断日期 |
| data.items[].total_score | string | 是 | 综合评分 |

## 4. 用法

```bash
python <RUN_PY> stock-comment-score --symbol 000001
```

## 5. 注意事项

- `symbol` 为 6 位数字股票代码，不带交易所后缀。
- 评分字段以字符串形式返回以保持精度。
