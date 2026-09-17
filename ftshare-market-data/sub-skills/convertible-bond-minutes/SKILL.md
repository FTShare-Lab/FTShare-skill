---
name: convertible-bond-minutes
description: 可转债历史分钟 K 线，单只或批量（convertible_bond_minute_candlesticks，GET /api/v2/market/data/convertible-bond-minute-candlesticks）。用户问可转债分钟行情、1/5/15 分钟 K 线、多只可转债分钟走势时使用。必填 --since-ts-millis、--until-ts-millis 与 --symbol / --symbols 之一；可选 --interval-value、--limit。
---

# 可转债历史分钟K线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 可转债历史分钟K线（convertible_bond_minute_candlesticks） |
| 外部接口 | `GET /api/v2/market/data/convertible-bond-minute-candlesticks` |
| 请求方式 | GET（query 参数，`symbols` 以重复参数发送） |
| 适用场景 | 获取单只或批量可转债的分钟 K 线；同一路径通过 `symbol` / `symbols` 区分查询形式 |
| 数据范围 | 按时间窗口返回可用历史分钟行情，窗口包含当日时可包含当日已生成分钟行情 |
| 单次限量 | 批量最多 20 个标的；单次最多 3 个北京时间自然日；`limit` 为每只标的 1～1000 条 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 二选一 | 单只可转债代码 | 113042.SH | 与 `symbols` 不能同时传 |
| symbols | string[] | 二选一 | 1～20 个可转债代码，逗号分隔传给 CLI | 113042.SH,123107.SZ | 接口侧以重复参数发送；也支持 JSON 字符串数组 |
| interval_value | int | 否 | 分钟周期 | 1 | 仅支持 1、5、15；不传等同于 1 |
| since_ts_millis | int | 是 | 起始时间戳（毫秒） | 1786291200000 | 单只、批量都必须提供；不得晚于 `until` |
| until_ts_millis | int | 是 | 结束时间戳（毫秒） | 1786377599999 | 与起始时间相差不超过 3 个北京时间自然日 |
| limit | int | 否 | **每只标的**聚合后返回条数上限 | 1 | 范围 1～1000；省略返回窗口内全部记录 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`。`data` 结构随查询形式变化：

- **单只查询**（`--symbol`）：`data` 直接为 K 线数组，无数据为 `[]`。
- **批量查询**（`--symbols`）：`data` 为分组对象数组；**即使只传 1 个标的也采用分组格式**，每项：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 可转债代码，响应使用 `.SH`/`.SZ` 短后缀 |
| items | array | 该标的 K 线数组，按时间升序排列 |
| total | int | `items` 的条数，不是分页总量 |

K 线字段：

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| open / high / low / close | string | 开/高/低/收盘价；进行中的 K 线 `close` 为最新价 | 元 |
| ts_millis | int | K 线结束时间戳 | 毫秒 |
| ts_millis_open | int | K 线开始时间戳 | 毫秒 |
| turnover | string | 成交额 | 元 |
| volume | int | 成交量 | - |

注：价格与成交额在 JSON 中为字符串（避免精度丢失），不是 number；`ts_millis` 为数字。

## 4. 调用方式

```bash
# 单只：2026-08-10 最后 1 根 1 分钟 K
python <RUN_PY> convertible-bond-minutes --symbol 113042.SH --since-ts-millis 1786291200000 --until-ts-millis 1786377599999 --limit 1

# 批量：每只最后 1 根 1 分钟 K
python <RUN_PY> convertible-bond-minutes --symbols 113042.SH,123107.SZ --since-ts-millis 1786291200000 --until-ts-millis 1786377599999 --limit 1

# 5 分钟聚合
python <RUN_PY> convertible-bond-minutes --symbol 113042.SH --interval-value 5 --since-ts-millis 1786291200000 --until-ts-millis 1786377599999
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `--symbol` / `--symbols` 缺省或同时传入、非可转债、缺少开始时间、时间倒序、超过 3 个自然日均会请求失败。
- `interval_value` 仅支持 1、5、15，其它取值请求失败；`limit` 必须在 1～1000，批量超过 20 个标的请求失败（CLI 会提前拦截标的数量）。
- 返回不复权分钟行情，接口不提供 `interval_unit` 与 `adjust_kind` 参数（CLI 也未暴露）。
- 自然日范围包含首尾日期：周一至周三为 3 个自然日，不是按交易日计数。
- 多分钟 K 在交易日内聚合，OHLC 分别取区间首根开盘、区间最高、区间最低、末根收盘，成交量和成交额求和。
- 设置 `limit` 时截取最新若干根，并按时间升序返回。
- 错误应同时检查 HTTP 状态与业务 `code`，不应仅凭 HTTP 200 判断成功。
- 实时分钟 K 线请使用 `convertible-bond-realtime-minute-kline`；日/周/月/年 K 线请使用 `convertible-bond-candlesticks`。