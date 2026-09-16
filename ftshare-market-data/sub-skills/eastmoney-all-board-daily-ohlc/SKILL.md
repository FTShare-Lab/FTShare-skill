---
name: eastmoney-all-board-daily-ohlc
description: 分页查询东方财富全部板块历史日线 OHLC（板块代码/名称/市场/日期/开高低收/成交量/成交额/振幅/涨跌幅/涨跌额/换手率）。用户提到「东财全板块日线」「全部板块 OHLC」「eastmoney all board daily ohlc」时使用。结果按板块代码、日期排序，分页返回；起止日期同时给定时跨度不得超过 3 个自然日，page_size 最大 200，支持 --all 翻页。
---

# 查询东方财富全板块日线 OHLC

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询东方财富全板块日线 OHLC |
| 外部接口 | GET /api/v1/market/data/eastmoney-all-board-daily-ohlc |
| 请求方式 | GET |
| 适用场景 | 获取东方财富全部板块的历史日线 OHLC，结果按板块代码、日期排序并分页返回 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| start_date | string | 否 | 起始日期（含） | `20251127` | YYYY-MM-DD 或 YYYYMMDD |
| end_date | string | 否 | 截止日期（含） | `2025-11-28` | YYYY-MM-DD 或 YYYYMMDD |
| page | uint | 否 | 页码 | `1` | 从 1 开始，默认 1；传 0 时按 1 处理 |
| page_size | uint | 否 | 每页数量 | `50` | 默认 50；传 0 时按 1 处理，最大 200 |

> `start_date` 与 `end_date` 同时给出时，结束日期与开始日期相差不得超过 3 个自然日。

## 执行方式

```bash
# 取一页
python <RUN_PY> eastmoney-all-board-daily-ohlc --start_date 2025-11-27 --end_date 2025-11-28 --page 1 --page_size 1
# 翻全量
python <RUN_PY> eastmoney-all-board-daily-ohlc --all
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

外层 `code/message/data`，分页数据位于 `data.records`。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pageNum": 1, "pageSize": 1, "total": 3, "pages": 3,
    "records": [
      {
        "板块代码": "BK1024",
        "板块名称": "绿色电力",
        "市场": "90",
        "日期": "2025-11-27",
        "开盘": "1001.53",
        "收盘": "1037.67",
        "最高": "1041.82",
        "最低": "1001.53",
        "成交量": "52669555",
        "成交额": "43012845568.00",
        "振幅": "4.03",
        "涨跌幅": "3.77",
        "涨跌额": "37.67",
        "换手率": "1.03"
      }
    ]
  }
}
```

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| pageNum | int | 当前页码 |
| pageSize | int | 每页数量 |
| total | int | 命中总记录数 |
| pages | int | 总页数 |
| records | array | 当前页行情记录 |

### records 元素字段（中文键）

| 字段 | 类型 | 说明 |
|------|------|------|
| 板块代码 | string | 板块代码 |
| 板块名称 | string | 板块名称 |
| 市场 | string | 东方财富市场代码 |
| 日期 | string | 日期，YYYY-MM-DD |
| 开盘 / 收盘 / 最高 / 最低 | string | 开 / 收 / 高 / 低 |
| 成交量 / 成交额 | string | 成交量 / 成交额 |
| 振幅 / 涨跌幅 / 涨跌额 / 换手率 | string | 振幅(%) / 涨跌幅(%) / 涨跌额 / 换手率(%) |

## 注意事项

- 数据范围 2013-04-09 至今，不同板块的起始日期可能不同。
- `start_date`、`end_date` 均可选；仅在二者同时传入时校验 3 个自然日的跨度。
- `page`、`page_size` 必须是非负整数；值为 0 时按 1 处理，`page_size` 大于 200 时按 200 处理。
- 行情记录的字段名及数值均按字符串返回；**字段名为中文**。
