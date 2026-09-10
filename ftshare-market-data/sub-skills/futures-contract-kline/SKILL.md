---
name: futures-contract-kline
description: 查询期货行情（期货合约日/周/月/季/年 K 线，futures_contract_kline）。用户问期货合约 K 线、期货日K/周K/月K、合约开高低收、期货成交量持仓量、vwap、主力合约复权因子时使用。
---

# 期货行情（期货合约 K 线）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 期货行情（futures_contract_kline） |
| 外部接口 | `GET /api/v1/market/data/futures/kline` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 查询期货合约日、周、月、季、年 K 线，含开高低收、成交量、成交额、vwap、持仓量、主力合约与前/后复权因子 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 期货合约代码 | A2605.DCE | 支持交易所短后缀 |
| interval | string | 否 | K 线周期 | daily | `daily`/`1d`、`weekly`/`1w`/`week`、`monthly`/`1mo`/`month`、`quarterly`/`1q`/`quarter`、`yearly`/`1y`/`year`；默认 `daily` |
| start | int | 否 | 起始时间戳（毫秒） | 1756431000000 | 闭区间；可省略时间范围 |
| end | int | 否 | 结束时间戳（毫秒） | 1756791000000 | 闭区间；不能单独传入 |
| limit | int | 否 | 返回条数 | 5 | 默认 500，最小值 1，传 0 时按 1 处理 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为对象：`items`（K 线记录列表）和 `total`（符合条件记录总数）。

items 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 规范化后的合约代码 |
| datetime | int64 | K 线时间戳（毫秒） |
| trade_date | int | 交易日 YYYYMMDD |
| open / high / low / close | number | 开盘价 / 最高价 / 最低价 / 收盘价 |
| volume | int64 | 成交量 |
| amount | number | 成交额 |
| vwap | number | 成交均价 |
| open_interest | number | 持仓量 |
| dominant_contract | string / null | 主力合约；合约 K 线不返回该字段值 |
| forward_factor | number / null | 前复权因子；合约 K 线不返回该字段值 |
| backward_factor | number / null | 后复权因子；合约 K 线不返回该字段值 |

## 4. 调用方式

```bash
python <RUN_PY> futures-contract-kline --symbol A2605.DCE --interval daily --limit 5
python <RUN_PY> futures-contract-kline --symbol A2605.DCE --interval weekly --limit 5
python <RUN_PY> futures-contract-kline --symbol A2605.DCE --start 1756431000000 --end 1756791000000
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 周、月、季、年 K 线基于日 K 线按北京时间聚合。
- `end` 不能单独传入，必须与 `start` 同时使用（handler 会本地校验并拒绝）；仅传 `start` 时查询 `start` 之后的数据。
- 同时传入 `start` 和 `end` 时，跨度不得超过 12 个日历月。
- 本接口查询的是具体合约 K 线；`dominant_contract` 和复权因子字段对合约 K 线不返回值。
