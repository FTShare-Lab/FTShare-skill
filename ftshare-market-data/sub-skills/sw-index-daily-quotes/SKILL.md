---
name: sw-index-daily-quotes
description: 查询申万指数日行情（sw_index_daily_quotes，GET /api/v1/market/data/sw-index/daily-quotes）。用户问申万指数某天/某区间的收盘点位、成交量额、涨跌幅、换手率、市盈率、市净率、市值或股息率，或按申万行业分类（一级/二级/三级行业、市场表征、风格指数等）筛选指数时使用。支持 --all 自动翻页。
---

# 申万指数日行情

接口：`GET /api/v1/market/data/sw-index/daily-quotes`。在线文档：[《申万指数日行情》](https://market.ft.tech/gateway/doc/pages/59aeqfx9.md)

查询申万指数日行情，支持单指数历史序列、单日全市场截面与按指数分类过滤，返回分页结构。

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 申万指数日行情（sw_index_daily_quotes） |
| 外部接口 | `GET /api/v1/market/data/sw-index/daily-quotes` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 单指数历史日行情；单日全市场截面；按 `index_type` 分类过滤 |
| 数据范围 | 1999-12-30 起至最新入库交易日；起止日期均包含在查询范围内 |
| 单次限量 | 分页返回，`page` 默认 1，`page_size` 默认 50、最大 200；超出末页返回空记录 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|--------|------|----------|------|----------|
| index_code | string | 否 | 申万指数代码，可带 `.SI` 后缀（不区分大小写） | 801001、801001.SI |
| trade_date | string | 单日模式必填 | 单个交易日 `YYYYMMDD`，查询当日全市场截面；与 `start_date`/`end_date` 互斥 | 20261111 |
| start_date | string | 区间模式必填 | 起始日期 `YYYYMMDD`，包含当天；需与 `end_date` 同时提供 | 20261101 |
| end_date | string | 区间模式必填 | 截止日期 `YYYYMMDD`，包含当天；需与 `start_date` 同时提供 | 20261111 |
| index_type | string | 否 | 指数分类：`一级行业`、`二级行业`、`三级行业`、`市场表征`、`风格指数`、`量化策略`、`新三板`、`大类风格`；空串视同未传 | 市场表征 |
| page | int | 否 | 页码，从 1 开始，默认 1；超出末页返回空记录 | 1 |
| page_size | int | 否 | 每页数量，默认 50，最大 200 | 50 |

不传 `--trade-date` 时必须同时提供 `--start-date` 与 `--end-date`，且起始日期不能晚于结束日期。

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`。`data` 分页对象：

| 字段 | 类型 | 说明 |
|------|------|------|
| pageNum | integer | 当前页码 |
| pageSize | integer | 当前每页数量 |
| total | integer | 符合条件的总记录数 |
| pages | integer | 总页数；无匹配记录时为 0 |
| records | array | 当前页的日行情记录 |

`records` 字段（数值字段均以字符串返回）：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| index_code / index_name | string | 指数代码 / 名称（名称缺失为 `null`） |
| index_type | string | 指数分类；缺失为 `null` |
| index_level | integer | 行业层级：一级 1、二级 2、三级 3，非行业指数为 `null` |
| trade_date | string | 交易日，格式 `YYYY-MM-DD` |
| open_index / high_index / low_index / close_index | string | 开高低收指数 |
| volume | string | 成交量（亿股） |
| amount | string | 成交额（亿元） |
| pct_change | string | 涨跌幅（%） |
| turnover_rate | string | 换手率（%） |
| pe / pb | string | 市盈率 / 市净率（倍） |
| avg_price | string | 均价（元） |
| amount_ratio | string | 成交额占比（%） |
| float_mv / avg_float_mv | string | 流通市值 / 平均流通市值（亿元） |
| dividend_yield | string | 股息率（%） |

## 4. 调用方式

```bash
# 单指数区间序列
python <RUN_PY> sw-index-daily-quotes --index-code 801001 --start-date 20261101 --end-date 20261111 --page 1 --page-size 2

# 单日全市场截面，按分类过滤
python <RUN_PY> sw-index-daily-quotes --trade-date 20261111 --index-type 一级行业 --page 1 --page-size 50

# 自动翻页取全部记录
python <RUN_PY> sw-index-daily-quotes --index-code 801001 --start-date 20261101 --end-date 20261111 --all
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `--trade-date` 与 `--start-date`/`--end-date` 互斥，CLI 会提前拦截混用和缺参。
- `index_type` 为空的指数只在未传 `--index-type` 时返回；少数分类没有对应日期的行情时返回空页（`total=0`、`pages=0`、`records=[]`），这不是错误。
- 记录按交易日、指数代码升序排列；`trade_date` 是 `YYYY-MM-DD` 字符串，与期货/股票接口的 `YYYYMMDD` 或毫秒时间戳不同。
- 数值字段是**字符串**，做数值计算前需自行转换（如 `float(close_index)`）。
- `--page-size` 最大 200；`--all` 按 `pages` 逐页取，第 0 页或空 `records` 时停止。
- 需要申万指数分钟 K 线请使用 `sw-index-history-minutes`；申万行业总览/成份股/日度指标请使用 `sw-industry-overview`、`sw-industry-constituent-history`、`sw-industry-daily-metrics`。