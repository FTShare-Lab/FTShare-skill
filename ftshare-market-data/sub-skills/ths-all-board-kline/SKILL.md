---
name: ths-all-board-kline
description: Get THS all boards K-line by date range (同花顺全板块 K 线). Use when user asks about 同花顺全板块行情、近N天板块K线、某日期范围所有板块K线.
---

# 同花顺全板块 K 线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询同花顺全板块 K 线 |
| 外部接口 | `GET /api/v1/market/data/ths-all-board-kline` |
| 请求方式 | GET |
| 适用场景 | 查询同花顺所有板块在指定日期范围内的 K 线数据（分页） |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| start_date | string | 否 | 起始日期（含） | 2021-10-01 | 格式 YYYY-MM-DD |
| end_date | string | 否 | 截止日期（含） | 2021-10-31 | 格式 YYYY-MM-DD |
| page | int | 否 | 页码，从 1 开始 | 1 | 默认 1 |
| page_size | int | 否 | 每页数量 | 50 | 默认 50 |

## 3. 响应说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| items | array | 分页数据列表 |
| items[].board_code | string | 板块代码 |
| items[].board_name | string | 板块名称 |
| items[].module | string | 所属模块 |
| items[].date | string | 日期 YYYY-MM-DD |
| items[].open | string | 开盘价 |
| items[].high | string | 最高价 |
| items[].low | string | 最低价 |
| items[].close | string | 收盘价 |
| items[].volume | string | 成交量 |
| total_pages | int | 总页数 |
| total_items | int | 总记录数 |

## 4. 用法

```bash
python <RUN_PY> ths-all-board-kline --start-date 2026-05-20 --end-date 2026-05-22 --page 1 --page-size 20
python <RUN_PY> ths-all-board-kline --start-date 2026-05-20 --page 1 --page-size 20
```

## 5. 请求示例

```
GET /api/v1/market/data/ths-all-board-kline?start_date=2026-05-20&end_date=2026-05-22&page=1&page_size=50
```

## 6. 注意事项

- 与 `ths-board-kline` 的区别：本接口按日期范围返回所有板块的 K 线，无需指定 `board_code`
- 日期格式为 `YYYY-MM-DD`，均可选
- K 线数值均为字符串
- 支持分页
