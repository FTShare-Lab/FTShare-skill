---
name: convertible-bond-candlesticks
description: 单只可转债历史 K 线 GET 接口（market.ft.tech，convertible-bond-candlesticks）。用户问某只可转债的分/日/周/月/年 K 线、开高低收、前/后复权、分钟级 K 线时使用。必填 --symbol、--interval-unit、--until-ts-millis；可选 --interval-value、--adjust-kind、--since-ts-millis、--limit。
---

# 可转债 K 线 - 查询单只可转债 K 线（convertible-bond-candlesticks）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只可转债历史 K 线 |
| 外部接口 | `GET /api/v1/market/data/convertible-bond-candlesticks` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 获取指定可转债的分/日/周/月/年 K 线，含开高低收、成交量、成交额；支持前复权 / 后复权 / 不复权。仅接受可转债标的 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 可转债代码（带市场后缀） | 113027.SH、123001.SZ | 也接受 `.XSHG`/`.SH`、`.XSHE`/`.SZ` 短后缀；非可转债标的当前返回系统错误 |
| interval_unit | string | 是 | 周期单位 | Day | Minute/Day/Week/Month/Year |
| interval_value | int | 否 | 间隔数值 | 1 | 默认 1；Minute+5 表示 5 分钟 K 线 |
| adjust_kind | string | 否 | 复权类型 | Forward | None（默认）/Forward（前复权）/Backward（后复权） |
| since_ts_millis | int | 否 | 开始时间戳（毫秒） | 1756700000000 | 分钟 K 线与 until 跨度 ≤3 天，其余周期不受 3 天限制 |
| until_ts_millis | int | 是 | 结束时间戳（毫秒） | 1756791000000 | - |
| limit | int | 否 | 返回条数上限 | 5 | 未传 since 和 limit 时默认最多返回 50 根 |

## 3. 响应说明

返回裸数组，每根 K 线包含：

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| open | string | 开盘价 | 元 |
| high | string | 最高价 | 元 |
| low | string | 最低价 | 元 |
| close | string | 收盘价（或最新价） | 元 |
| ts_millis | int | 收盘时间戳 | 毫秒 |
| ts_millis_open | int | 开盘时间戳 | 毫秒 |
| turnover | string | 成交额 | 元 |
| volume | int64 | 成交量 | 张 |

## 4. 调用方式

```bash
python <RUN_PY> convertible-bond-candlesticks --symbol 113027.SH --interval-unit Day --since-ts-millis 1756700000000 --until-ts-millis 1756791000000 --limit 5
python <RUN_PY> convertible-bond-candlesticks --symbol 113027.SH --interval-unit Minute --interval-value 5 --adjust-kind Forward --since-ts-millis 1756700000000 --until-ts-millis 1756791000000
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON，请求头已内置 `X-Client-Name: ft-claw`。

## 5. 注意事项

- `symbol`、`interval_unit`、`until_ts_millis` 必填。
- `symbol` 必须是可转债代码，格式 `{代码}.{市场}`；非可转债标的当前外部接口返回系统错误。
- 分钟 K 线（`interval_unit=Minute`）的 `since/until` 跨度硬限制 ≤3 天，超过需分段调用。
- `interval_value` 仅在 `interval_unit=Minute` 时生效：不传或传 1 为 1 分钟 K，传 5/15/30/60/120 为对应多分钟 K；其他周期忽略该字段。
- 多分钟 K 按北京时间的每个交易日分别聚合，不跨交易日；以 5 分钟 K 为例，首根为 09:30—09:35，开高低收取区间首根开盘价、最高价、最低价、末根收盘价，成交量和成交额按区间求和。
- 默认不复权（None），`Forward` 前复权、`Backward` 后复权。
- 价格字段 JSON 中为字符串以避免精度丢失。
