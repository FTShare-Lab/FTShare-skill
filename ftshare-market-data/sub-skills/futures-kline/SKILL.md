---
name: futures-kline
description: 查询期货合约历史 K 线（期货合约日/周/月/季/年 K 线，futures_kline）。用户问期货合约 K 线、期货日K/周K/月K、合约开高低收、期货成交量持仓量、vwap、持仓量时使用。
---

# 期货合约历史K线

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 期货合约历史K线（futures_kline） |
| 外部接口 | `GET /api/v1/market/data/futures/kline` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 查询单个期货合约的历史日、周、月、季、年 K 线，含开高低收、成交量、成交额、vwap、持仓量 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 期货合约代码 | A2605.DCE | 使用 3 字符短后缀 `.DCE`/`.SHF`/`.CZC`/`.INE`/`.GFE`/`.CFE`；长后缀会返回 HTTP 400 |
| interval | string | 否 | K 线周期 | daily | `daily`、`weekly`、`monthly`、`quarterly`、`yearly`，兼容 `1d`/`1w`/`1mo`/`1q`/`1y`；默认 `daily` |
| start | int | 否 | 起始时间戳（毫秒） | 1756431000000 | 按北京时间解释，闭区间；可省略时间范围 |
| end | int | 否 | 结束时间戳（毫秒） | 1756791000000 | 闭区间；不能单独传入，须与 `start` 同时使用，跨度不超过 12 个自然月 |
| limit | int | 否 | 返回条数 | 5 | 默认 500，保留查询范围内最新记录 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为对象：`items`（K 线记录列表，按时间升序）和 `total`（查询范围内符合条件的记录数）。

items 数组：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 去除交易所后缀并转小写的合约代码 |
| datetime | int | K 线时间戳（毫秒） |
| trade_date | int | 交易日 YYYYMMDD |
| open / high / low / close | number | 开盘价 / 最高价 / 最低价 / 收盘价 |
| volume | int | 成交量 |
| amount | number | 成交额 |
| vwap | number | 成交量加权均价 |
| open_interest | number | 持仓量 |
| dominant_contract | string / null | 主力合约；当前合约历史 K 线返回 `null` |
| forward_factor | number / null | 前复权因子；当前接口返回 `null` |
| backward_factor | number / null | 后复权因子；当前接口返回 `null` |

## 4. 调用方式

```bash
python <RUN_PY> futures-kline --symbol A2605.DCE --interval daily --limit 5
python <RUN_PY> futures-kline --symbol A2605.DCE --interval weekly --limit 5
python <RUN_PY> futures-kline --symbol A2605.DCE --start 1756431000000 --end 1756791000000
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 合约代码使用 3 字符短后缀（`.DCE`/`.SHF`/`.CZC`/`.INE`/`.GFE`/`.CFE`），长后缀（`.SHFE`/`.CZCE`/`.GFEX`/`.CFFEX`）不支持，会返回 HTTP 400。
- 周、月、季、年 K 线由历史日 K 线按北京时间聚合生成。
- `end` 不能单独传入，必须与 `start` 同时使用（handler 会本地校验并拒绝）；同时传入时跨度不得超过 12 个自然月。
- 返回结果按 K 线时间升序排列；`limit` 保留查询范围内最新的记录。
