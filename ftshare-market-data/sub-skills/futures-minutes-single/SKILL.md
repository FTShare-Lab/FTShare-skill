---
name: futures-minutes-single
description: 查询单个期货合约的历史分钟 K 线（futures_minutes_single，GET /api/v2/market/data/futures_minutes/single）。用户问某个期货合约的 1/5/15/30/60 分钟历史行情、指定时间段的期货分钟走势时使用。必填 --symbol、--start、--end；可选 --interval、--limit。
---

# 期货历史分钟K线单合约

接口：`GET /api/v2/market/data/futures_minutes/single`。在线文档：[《期货历史分钟K线单合约》](https://market.ft.tech/gateway/doc/pages/1r54drig.md)

查询单个期货合约的历史分钟 K 线。必填 `--symbol`、`--start`、`--end`；`--interval` 默认 `1min`，`--limit` 默认 500（范围 1～10000）。

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 期货历史分钟K线单合约（futures_minutes_single） |
| 外部接口 | `GET /api/v2/market/data/futures_minutes/single` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 单个期货合约历史分钟 K 线；不支持批量 |
| 数据范围 | 历史 1 分钟原始 K 线，可聚合为 1、5、15、30、60 分钟 K 线；不返回实时分钟数据 |
| 单次限量 | `limit` 默认 500，范围 1～10000；时间跨度不超过 3 个自然日（含首尾） |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|--------|------|----------|------|----------|
| symbol | string | 是 | 单个期货合约代码，使用不带交易所后缀的裸代码，不区分大小写 | A2611 |
| interval | string | 否 | 分钟周期，默认 `1min`；可选 `1min`、`5min`、`15min`、`30min`、`60min` | 5min |
| start | int | 是 | 起始时间戳（毫秒，闭区间），按北京时间解释 | 1791475200000 |
| end | int | 是 | 结束时间戳（毫秒，闭区间）；与 `start` 跨度不超过 3 个自然日 | 1791647999000 |
| limit | int | 否 | 返回的最新 K 线条数，默认 500，范围 1～10000 | 500 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`。`data` 对象：

| 字段 | 类型 | 说明 |
|------|------|------|
| items | array | 分钟 K 线记录，按时间升序 |
| total | integer | 查询范围内聚合后的总记录数，不受 `limit` 截断 |

`items` 字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| bar_interval | string | 返回周期，例如 `5min` |
| symbol | string | 不带交易所后缀的官网合约代码，大小写沿用交易所官网格式；CZCE 真实合约返回四位年份代码 |
| variety | string | 期货品种标识 |
| exchange | string | 交易所标识 |
| datetime | integer | K 线时间戳（毫秒） |
| trade_date | integer | 交易日 `YYYYMMDD` |
| open / high / low / close | number | 开高低收价格 |
| volume | integer | 成交量 |
| amount | number | 成交额 |
| vwap | number | 成交量加权均价 |
| open_interest | number | 持仓量 |
| pre_settlement_price | number | 昨日结算价 |
| settlement_price | number | 结算价；未结算时可能为 0 |
| high_limit_price | number | 涨停价 |
| low_limit_price | number | 跌停价 |
| pre_close_price | number | 昨收价 |
| updated_at | integer | 数据更新时间戳（毫秒） |

## 4. 调用方式

```bash
# 5 分钟 K 线
python <RUN_PY> futures-minutes-single --symbol A2611 --interval 5min --start 1791475200000 --end 1791647999000 --limit 500

# 1 分钟 K 线（默认周期）
python <RUN_PY> futures-minutes-single --symbol A2611 --start 1791475200000 --end 1791647999000
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- **只接受单个合约**：本接口只接受 `symbol`，传 `symbols` 会返回 HTTP 400；需要多合约请按合约逐个查询，或使用 `futures-minutes` 的批量模式。
- **裸代码**：合约代码不带交易所后缀，请求不区分大小写。CZCE 真实合约必须使用四位年份代码（如 `AP2612`），三位代码不符合接口规范。
- `start` 与 `end` 必须同时传入，单位毫秒、闭区间；时间跨度不得超过 3 个自然日（含首尾），超出返回 HTTP 400。
- 当前北京时间日期的数据在当日 16:30 前不可查询。
- `--limit` 超过 10000 或小于 1 时接口返回 HTTP 400，CLI 会提前拦截；`data.total` 不受 `limit` 截断，`items` 条数是截断后的结果。
- 多合约历史分钟 K 线请使用 `futures-minutes`；实时分钟 K 线请使用 `futures-realtime-minute-kline`；日 K 请使用 `futures-daily-kline` 或 `futures-kline`。