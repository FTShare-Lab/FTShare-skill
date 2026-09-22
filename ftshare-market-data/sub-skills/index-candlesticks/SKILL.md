---
name: index-candlesticks
description: 单只指数历史日/周/月/年 K 线 GET 接口（market.ft.tech，index-candlesticks）。用户问某只指数的日/周/月/年 K 线、开高低收点位、前/后复权、沪深300/上证指数日 K 时使用。必填 --symbol、--interval-unit、--since-ts-millis、--until-ts-millis；可选 --adjust-kind、--limit。分钟级 K 线请用 index-minutes。
---

# 指数 K 线 - 查询单只指数 K 线（index-candlesticks）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只指数历史 K 线 |
| 外部接口 | `GET /api/v1/market/data/index-candlesticks` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 获取指定指数的日/周/月/年 K 线，含开高低收点位、成交量、成交额；支持前复权 / 后复权 / 不复权。仅接受指数标的 |

> 与 `index-ohlcs`（`GET daec/history/ohlcs`，YYYYMMDD 日期区间，仅日/周/月）区别：本接口走 GET query 参数，参数为毫秒时间戳，支持日/周/月/年 K。分钟级 K 线请使用 `index-minutes` 子 skill。

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 指数代码（带市场后缀） | 000300.XSHG、399001.XSHE | 也接受 `.SH`/`.SZ` 短后缀；非指数标的当前返回系统错误 |
| interval_unit | string | 是 | 周期单位 | day | day/week/month/year（大小写不敏感，不支持 minute） |
| adjust_kind | string | 否 | 复权类型 | forward | none（默认，不复权）/forward（前复权）/backward（后复权） |
| since_ts_millis | int | 是 | 开始时间戳（毫秒） | 1756700000000 | 与 until 的跨度不得超过 12 个自然月 |
| until_ts_millis | int | 是 | 结束时间戳（毫秒） | 1756791000000 | - |
| limit | int | 否 | 返回条数上限 | 5 | 不传时返回请求时间范围内的全部数据 |

## 3. 响应说明

返回裸数组，每根 K 线包含：

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| open | string | 开盘点位 | 指数点 |
| high | string | 最高点位 | 指数点 |
| low | string | 最低点位 | 指数点 |
| close | string | 收盘点位（或最新点位） | 指数点 |
| ts_millis | int | 收盘时间戳 | 毫秒 |
| ts_millis_open | int | 开盘时间戳 | 毫秒 |
| turnover | string | 成交额（成分股合计） | 元 |
| volume | int64 | 成交量（成分股合计） | - |

## 4. 调用方式

```bash
python <RUN_PY> index-candlesticks --symbol 000300.XSHG --interval-unit day --since-ts-millis 1756700000000 --until-ts-millis 1756791000000 --limit 5
python <RUN_PY> index-candlesticks --symbol 399001.XSHE --interval-unit week --adjust-kind forward --since-ts-millis 1756700000000 --until-ts-millis 1756791000000
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 注意事项

- `symbol`、`interval_unit`、`since_ts_millis`、`until_ts_millis` 必填。
- `symbol` 必须是指数代码，格式 `{代码}.{市场}`；非指数标的当前外部接口返回系统错误。
- 本接口不支持分钟周期：`interval_unit=minute` 会返回参数错误（提示使用 `/index_minutes`），分钟数据请使用 `index-minutes` 子 skill。
- 时间跨度最多 12 个自然月；需要更长历史时按窗口分段多次调用。
- 默认不复权（`none`），`forward` 前复权、`backward` 后复权（取值大小写不敏感）。
- 价格字段（点位）JSON 中为字符串以避免精度丢失。
