---
name: futures-minutes
description: 期货历史分钟 K 线，单合约或批量（futures_minutes，GET /api/v2/market/data/futures_minutes）。用户问期货分钟行情、1/5/15/30/60 分钟 K 线、多只期货合约分钟走势时使用。必填 --start、--end 与 --symbol / --symbols 之一；可选 --interval、--limit。
---

# 期货历史分钟K线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 期货历史分钟K线（futures_minutes） |
| 外部接口 | `GET /api/v2/market/data/futures_minutes` |
| 请求方式 | GET（query 参数，`symbols` 以重复参数发送） |
| 适用场景 | 获取单个或批量期货合约的历史分钟 K 线；同一路径通过 `symbol` / `symbols` 区分查询形式 |
| 数据范围 | 历史 1 分钟原始 K 线，可聚合为 1、5、15、30、60 分钟 K 线；不返回实时分钟数据 |
| 单次限量 | 单合约查询 `limit` 默认 500，范围 1～1000；批量查询支持 1～20 个合约；时间跨度不超过 3 个自然日（含首尾） |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 二选一 | 单个期货合约代码 | A2611.DCE | 与 `symbols` 不能同时传 |
| symbols | string[] | 二选一 | 1～20 个合约代码，逗号分隔传给 CLI | A2611.DCE,CU2611.SHF | 接口侧以重复参数发送 |
| interval | string | 否 | 分钟周期 | 5min | `1min`/`5min`/`15min`/`30min`/`60min`；兼容 `1m`/`5m`/`15m`/`30m`/`1h`；默认 `1min` |
| start | int | 是 | 起始时间戳（毫秒） | 1791475200000 | 闭区间；必须与 `end` 同时传入 |
| end | int | 是 | 结束时间戳（毫秒） | 1791647999000 | 闭区间；与 `start` 跨度不超过 3 个自然日 |
| limit | int | 否 | **每个合约**返回的最新 K 线条数 | 5 | 默认 500，范围 1～1000 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`。`data` 结构随查询形式变化：

- **单合约查询**（`--symbol`）：`data` 为对象 `{items, total}`；`total` 为查询范围内符合条件的原始分钟记录数，**不受 `limit` 截断影响**，不一定等于 `items` 条数。
- **批量查询**（`--symbols`）：`data.items` 为分组对象数组，每项含 `symbol`（请求中的合约代码）、`items`（该合约符合条件且经 `limit` 截断后的分钟 K 线列表）、`total`（该合约**符合条件的记录总数**，不受 `limit` 截断影响）。

真机验证：`limit=3` 时单合约 `items` 为 3 条而 `total` 为 73；批量 `limit=1` 时每组 `items` 为 1 条而 `total` 为 73/110。`limit` 只截断 `items` 条数，不改变 `total`。

每根分钟 K 线字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| bar_interval | string | 返回周期，例如 `5min` |
| symbol | string | 去除交易所后缀并转小写后的合约代码 |
| variety | string | 期货品种标识 |
| exchange | string | 交易所标识 |
| datetime | int | K 线时间戳（毫秒） |
| trade_date | int | 交易日 YYYYMMDD |
| open / high / low / close | number | 开盘、最高、最低、收盘价格 |
| volume | int | 成交量 |
| amount | number | 成交额 |
| vwap | number | 成交量加权均价 |
| open_interest | number | 持仓量 |
| pre_settlement_price | number | 昨日结算价 |
| settlement_price | number | 结算价；未结算时可能为 0 |
| high_limit_price | number | 涨停价 |
| low_limit_price | number | 跌停价 |
| pre_close_price | number | 昨收价 |
| updated_at | int | 数据更新时间戳（毫秒） |

## 4. 调用方式

```bash
# 单合约：5 分钟 K
python <RUN_PY> futures-minutes --symbol A2611.DCE --interval 5min --start 1791475200000 --end 1791647999000 --limit 5

# 批量：每合约最新 5 根 5 分钟 K
python <RUN_PY> futures-minutes --symbols A2611.DCE,CU2611.SHF --interval 5min --start 1791475200000 --end 1791647999000 --limit 5
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- **交易所后缀规则（必读）**：合约代码格式为 `<合约代码>.<三字符交易所后缀>`，本接口支持 `.DCE`、`.SHF`、`.CZC`、`.INE`、`.GFE`、`.CFE`；长后缀 `.SHFE`、`.CZCE`、`.GFEX`、`.CFFEX` 等不支持，会返回 HTTP 400，请勿照搬公开行情数据源写法。
- `--symbol` / `--symbols` 二选一，至少提供一个且不能同时传入；`start` 与 `end` 必须同时传入，时间跨度不得超过 3 个北京时间自然日。
- 批量查询时 `symbols` 以重复参数发送（`symbols=A2611.DCE&symbols=CU2611.SHF`）；逗号分隔在接口侧也兼容。
- `limit` 必须在 1～1000；批量超过 20 个合约请求失败（CLI 会提前拦截合约数量）。
- 当前北京时间日期当天的数据在 16:30 前不可查询。
- 多分钟 K 在交易日内聚合，`bar_interval` 标识返回周期；`settlement_price` 未结算时可能为 0。
- 历史周期 K 线请使用 `futures-kline`（单合约）或 `futures-kline-batch`（批量）；实时分钟 K 线请使用 `futures-realtime-minute-kline`。
