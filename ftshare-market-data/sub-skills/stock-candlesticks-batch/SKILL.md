---
name: stock-candlesticks-batch
description: 批量获取多只股票/ETF/可转债/指数 K 线 GET 接口（market.ft.tech，stock-candlesticks/batch）。用户问多只标的的日/周/月/年 K 线、批量开高低收、混合多类证券的 K 线时使用。必填 --symbols、--interval-unit、--since-ts-millis、--until-ts-millis；可选 --adjust-kind、--limit。
---

# 批量股票K线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 批量股票K线（stock_candlesticks_batch） |
| 外部接口 | `GET /api/v2/market/data/stock-candlesticks/batch` |
| 请求方式 | GET（query 参数，`symbols` 可重复传入） |
| 适用场景 | 一次批量查询股票 / ETF / 可转债 / 指数等多只标的的历史 K 线（开高低收、成交量、成交额、换手率），支持日/周/月/年周期与前复权/后复权。通用语义，允许不同证券类别混合查询，不做类别校验 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbols | string[] | 是 | 标的代码列表，逗号分隔传给 CLI | 600519.SH,510300.SH,113027.SH,000300.SH | 可混合股票/ETF/可转债/指数；沪市 `.XSHG`/`.SH`、深市 `.XSHE`/`.SZ`、北交所 `.BJSE`/`.BJ`；接口侧以重复 query 参数发送 |
| interval_unit | string | 是 | 周期单位 | Day | Day/Week/Month/Year，大小写不敏感；**不支持 Minute** |
| adjust_kind | string | 否 | 复权类型 | Forward | None（默认）/Forward（前复权）/Backward（后复权） |
| since_ts_millis | int | 是 | 开始时间戳（毫秒） | 1756431000000 | 与 until 的跨度不得超过 12 个日历月；不得晚于 until |
| until_ts_millis | int | 是 | 结束时间戳（毫秒） | 1756791000000 | - |
| limit | int | 否 | 每个标的返回条数上限 | 3 | 不传时返回请求时间范围内的全部数据 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`（失败时为 `null`）。`data` 为非分页嵌套数组，外层每项为 `[symbol, K线数组]`，每根 K 线字段：

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| symbol | string | 标的代码，响应统一使用 `.SH`、`.SZ`、`.BJ` 短后缀 | - |
| open / high / low / close | number | 开/高/低/收盘价 | 元 |
| ts_millis | string | 收盘时间戳 | 毫秒 |
| ts_millis_open | string | 开盘时间戳 | 毫秒 |
| turnover | number | 成交额 | 元 |
| volume | integer | 成交量 | - |
| turnover_rate | number | 换手率 | % |

注：`open/high/low/close`、`turnover` 在 JSON 中实际以字符串返回（避免精度丢失）；`ts_millis` 为数字。

## 4. 调用方式

```bash
python <RUN_PY> stock-candlesticks-batch --symbols 600519.SH,000001.SZ --interval-unit Day --since-ts-millis 1756431000000 --until-ts-millis 1756791000000 --limit 2
python <RUN_PY> stock-candlesticks-batch --symbols 600519.SH,510300.SH,113027.SH --interval-unit Week --adjust-kind Forward --since-ts-millis 1756431000000 --until-ts-millis 1756791000000 --limit 3
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `symbols`、`interval_unit`、`since_ts_millis`、`until_ts_millis` 必填；所有 `symbols` 使用相同周期。
- 接口仅支持 GET；`symbols` 在查询参数中以重复参数形式发送（`symbols=600519.SH&symbols=000001.SZ`）。
- 时间跨度最多 12 个日历月；需要更长历史时按窗口分段多次调用。
- 不支持分钟 K 线；分钟数据请使用 `stock-minutes-batch` 子 skill。
- 混合证券类别不做校验；换手率仅股票标的有值，ETF/可转债/指数标的当前为 `null`。
- 输入 `.XSHG`/`.XSHE`/`.BJSE` 长后缀时，响应中的 symbol 会规范化为 `.SH`、`.SZ`、`.BJ` 短后缀。
- 默认不复权（None）；仅使用历史日 K 数据计算，不含实时行情，实际起始日期以行情数据源覆盖为准。
