---
name: convertible-bond-candlesticks-batch
description: 批量查询多只可转债历史日/周/月/年 K 线（convertible_bond_candlesticks_batch，GET /api/v2/market/data/convertible-bond-candlesticks/batch）。用户问多只可转债的日/周/月/年 K 线、批量可转债开高低收、多只转债对比 K 线时使用。必填 --symbols、--interval-unit、--since-ts-millis、--until-ts-millis；可选 --adjust-kind、--limit。分钟 K 线请改用 convertible-bond-minutes。
---

# 批量可转债历史K线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 批量可转债历史K线（convertible_bond_candlesticks_batch） |
| 外部接口 | `GET /api/v2/market/data/convertible-bond-candlesticks/batch` |
| 请求方式 | GET（query 参数，`symbols` 使用逗号分隔） |
| 适用场景 | 一次批量获取 1～20 只可转债的历史日/周/月/年 K 线（开高低收、成交量、成交额），支持前复权/后复权/不复权 |
| 数据范围 | 以各标的实际历史行情覆盖为准；**不含当日盘中实时行情** |
| 单次限量 | 每次 1～20 个标的；无分页；所有周期单次时间跨度不超过 12 个自然月 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbols | string | 是 | 可转债代码列表，逗号分隔传给 CLI | 113042.SH,123107.SZ | 1～20 只；也接受 `.XSHG`/`.SH`、`.XSHE`/`.SZ`；接口侧以逗号分隔发送，兼容旧的重复参数和 JSON 字符串数组格式 |
| interval_unit | string | 是 | 周期单位 | day | day/week/month/year（大小写不敏感）；**不支持 minute** |
| adjust_kind | string | 否 | 复权类型 | forward | none（默认，不复权）/forward（前复权）/backward（后复权） |
| since_ts_millis | int | 是 | 开始时间戳（毫秒） | 1786291200000 | 不得晚于 `until_ts_millis` |
| until_ts_millis | int | 是 | 结束时间戳（毫秒） | 1786377599999 | 与起始时间相差不超过 12 个自然月 |
| limit | int | 否 | **每个标的**返回条数上限 | 1 | 省略时返回窗口内全部记录 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`（失败时为 `null`）。`data` 为按请求顺序排列的非分页分组数组，每项结构为 `{symbol, items, total}`：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 可转债代码，使用 `.SH`/`.SZ` 短后缀 |
| items | array | 该标的的 K 线数组；无数据时为 `[]` |
| total | integer | `items` 的 K 线条数；无数据时为 0 |

`items` 中每根 K 线字段：

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| open / high / low / close | string | 开/高/低/收盘价；进行中的 K 线 `close` 为最新价；JSON 中为字符串以保留精度 | 元 |
| ts_millis | integer | K 线结束时间戳 | 毫秒 |
| ts_millis_open | integer | K 线开始时间戳 | 毫秒 |
| turnover | string | 成交额；JSON 中为字符串以保留精度 | 元 |
| volume | integer | 成交量 | - |
| turnover_rate | number / null | 换手率；可转债批量历史 K 线当前固定为 `null` | % |

## 4. 调用方式

```bash
python <RUN_PY> convertible-bond-candlesticks-batch --symbols 113042.SH,123107.SZ --interval-unit day --since-ts-millis 1786291200000 --until-ts-millis 1786377599999 --limit 1
python <RUN_PY> convertible-bond-candlesticks-batch --symbols 113042.XSHG,123107.XSHE --interval-unit week --adjust-kind forward --since-ts-millis 1783000000000 --until-ts-millis 1786377599999
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `symbols`、`interval_unit`、`since_ts_millis`、`until_ts_millis` 必填；空 `symbols` 或超过 20 个标的会请求失败。
- 接口仅支持 GET；`symbols` 使用逗号分隔发送（`symbols=113042.SH,123107.SZ`），兼容旧的重复参数和 JSON 字符串数组格式。
- 所有标的共用同一周期与复权参数，不能逐只指定。
- 仅接受可转债标的；混入股票等其它类别时整个请求失败，不静默过滤。
- 分钟 K 线不在本接口，请改用 `convertible-bond-minutes` 子 skill。
- 单次时间跨度上限 12 个自然月；更长历史需分段调用。
- 周、月、年 K 按请求范围内的历史日 K 聚合；窗口未覆盖完整周期时，该周期不是完整周期数据。
- 无数据不等于请求失败，应同时检查 `code` 与 `data`。