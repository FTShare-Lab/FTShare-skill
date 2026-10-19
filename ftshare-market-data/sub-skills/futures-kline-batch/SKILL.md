---
name: futures-kline-batch
description: 批量查询多个期货合约的历史 K 线（futures_kline_batch，GET /api/v2/market/data/futures/kline/batch）。用户问多只期货合约日/周/月/季 K 线、批量期货开高低收、期货批量行情、多合约对比 K 线时使用。
---

# 批量期货合约历史K线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 批量期货合约历史K线（futures_kline_batch） |
| 外部接口 | `GET /api/v2/market/data/futures/kline/batch` |
| 请求方式 | GET（query 参数，`symbols` 使用逗号分隔） |
| 适用场景 | 一次批量获取多个期货合约的历史 K 线（开高低收、成交量、成交额、vwap、持仓量），支持日/周/月/季周期 |
| 数据范围 | 支持日、周、月、季 K 线；周、月、季 K 线由历史日 K 线聚合生成 |
| 单次限量 | `symbols` 支持 1～20 个合约；每个合约 `limit` 默认 500；时间范围不超过 12 个自然月 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbols | string | 是 | 期货合约代码列表，逗号分隔传给 CLI | A2611.DCE,M2611.DCE | 1～20 个；接口侧以逗号分隔发送，兼容旧的重复参数格式 |
| interval | string | 否 | K 线周期 | daily | `daily`/`weekly`/`monthly`/`quarterly`；默认 `daily` |
| start | int | 否 | 起始时间戳（毫秒） | 1790784000000 | 闭区间；按北京时间解释 |
| end | int | 否 | 结束时间戳（毫秒） | 1791647999000 | 闭区间；不能单独传入 |
| limit | int | 否 | **每个合约**返回的最新 K 线条数 | 5 | 默认 500 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`。`data` 为按请求顺序排列的标的分组数组（非分页），每项结构为 `{symbol, items, total}`：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 请求中的合约代码（保留请求值） |
| items | array | 该合约符合条件且经 `limit` 截断后的 K 线记录列表 |
| total | integer | `items` 中的 K 线记录数（已应用 `limit`）；无数据时为 0 |

分组内每根 K 线字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 去除交易所后缀并转小写后的合约代码 |
| datetime | int | K 线时间戳（毫秒） |
| trade_date | int | 交易日 YYYYMMDD |
| open / high / low / close | number | 开盘价 / 最高价 / 最低价 / 收盘价 |
| volume | int | 成交量 |
| amount | number | 成交额 |
| vwap | number | 成交量加权均价 |
| open_interest | number | 持仓量 |
| dominant_contract | string / null | 主力合约；当前接口返回 `null` |
| forward_factor | number / null | 前复权因子；当前接口返回 `null` |
| backward_factor | number / null | 后复权因子；当前接口返回 `null` |

## 4. 调用方式

```bash
python <RUN_PY> futures-kline-batch --symbols A2611.DCE,M2611.DCE --interval daily --start 1790784000000 --end 1791647999000 --limit 5
python <RUN_PY> futures-kline-batch --symbols A2611.DCE,M2611.DCE,CU2611.SHFE --interval weekly --limit 5
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- **交易所后缀规则（必读）**：合约代码格式为 `<合约代码>.<交易所代码>`，只接受交易所全称后缀 `.SHFE`、`.INE`、`.DCE`、`.CZCE`、`.CFFEX`、`.GFEX`；短后缀 `.SHF`、`.CZC`、`.CFE`、`.GFE` 及其它未列出的后缀会返回 HTTP 400；无后缀的裸合约代码仍兼容。
- `symbols` 使用逗号分隔发送（`symbols=A2611.DCE,M2611.DCE`），兼容旧的重复参数格式。
- 外层分组的 `symbol` 保留请求值；分组内 K 线记录的 `symbol` 为去除交易所后缀并转小写后的合约代码。
- `start` 与 `end` 均为 Unix 毫秒时间戳，按北京时间解释；`end` 不能单独传入，必须与 `start` 同时使用（handler 会本地校验）。
- `start` 与 `end` 的时间跨度不得超过 12 个自然月。
- 单合约历史 K 线请使用 `futures-kline`；历史分钟 K 线请使用 `futures-minutes`。
