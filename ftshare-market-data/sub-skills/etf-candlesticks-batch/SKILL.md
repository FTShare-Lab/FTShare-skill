---
name: etf-candlesticks-batch
description: 批量查询多只 ETF 的历史 K 线（etf_candlesticks_batch）。用户问多只 ETF 日/周/月/年 K 线、批量 ETF 开高低收、ETF 批量行情、多 ETF 对比 K 线时使用。
---

# 批量ETFK线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 批量ETFK线（etf_candlesticks_batch） |
| 外部接口 | `GET /api/v2/market/data/etf-candlesticks/batch` |
| 请求方式 | GET（query 参数，`symbols` 可重复传入） |
| 适用场景 | 一次批量获取多只 ETF 的历史 K 线（开高低收、成交量、成交额、换手率），支持日/周/月/年周期与前复权/后复权 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbols | string[] | 是 | ETF 代码列表，逗号分隔传给 CLI | 510300.SH,159915.SZ | 沪市支持 `.XSHG`/`.SH`，深市支持 `.XSHE`/`.SZ`；接口侧以重复 query 参数发送 |
| interval_unit | string | 是 | 周期单位 | Day | Day/Week/Month/Year，大小写不敏感；**不支持 Minute** |
| adjust_kind | string | 否 | 复权类型 | Forward | None（默认）/Forward（前复权）/Backward（后复权） |
| since_ts_millis | int | 是 | 开始时间戳（毫秒） | 1756431000000 | 与 until 的跨度不得超过 12 个日历月；不得晚于 until |
| until_ts_millis | int | 是 | 结束时间戳（毫秒） | 1756791000000 | - |
| limit | int | 否 | 每个标的返回条数上限 | 2 | 不传时返回请求时间范围内的全部数据 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`（失败时为 `null`）。`data` 为非分页嵌套数组，外层每项为 `[symbol, K线数组]`，每根 K 线字段：

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| symbol | string | ETF 代码，响应统一使用 `.SH`、`.SZ` 短后缀 | - |
| open / high / low / close | number | 开/高/低/收盘价 | 元 |
| ts_millis | string | 收盘时间戳 | 毫秒 |
| ts_millis_open | string | 开盘时间戳 | 毫秒 |
| turnover | number | 成交额 | 元 |
| volume | integer | 成交量 | - |
| turnover_rate | number | 换手率；ETF 标的当前为 `null` | % |

注：`open/high/low/close`、`turnover` 在 JSON 中实际以字符串返回（避免精度丢失）；`ts_millis` 为数字。

## 4. 调用方式

```bash
python <RUN_PY> etf-candlesticks-batch --symbols 510300.SH,159915.SZ --interval-unit Day --since-ts-millis 1756431000000 --until-ts-millis 1756791000000 --limit 2
python <RUN_PY> etf-candlesticks-batch --symbols 510300.XSHG,159915.XSHE --interval-unit Week --adjust-kind Forward --since-ts-millis 1754092800000 --until-ts-millis 1756791000000
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `symbols`、`interval_unit`、`since_ts_millis`、`until_ts_millis` 必填；所有 `symbols` 使用相同周期。
- 接口仅支持 GET；`symbols` 在查询参数中以重复参数形式发送（`symbols=510300.SH&symbols=159915.SZ`）。
- 时间跨度最多 12 个日历月；需要更长历史时按窗口分段多次调用。
- 不支持分钟 K 线；分钟数据请使用 `etf-minutes-batch` 子 skill。
- `symbols` 中每项必须是 ETF 标的：若混入非 ETF（如股票），整个批量请求失败，不静默过滤（当前返回系统错误）。
- 输入 `.XSHG`/`.XSHE` 长后缀时，响应中的 symbol 会规范化为 `.SH`、`.SZ` 短后缀。
- 默认不复权（None）；仅使用历史日 K 数据计算，不含实时行情，实际起始日期以行情数据源覆盖为准。
