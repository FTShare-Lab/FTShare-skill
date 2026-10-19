---
name: futures-realtime-day-kline
description: 查询期货合约当前交易日的实时日 K 线（futures_realtime_day_kline，GET /api/v4/market/data/futures-realtime-day-kline）。用户问期货实时日 K、当下期货开高低收、多只期货合约今日行情时使用。必填 --symbols，逗号分隔，1～20 个。
---

# 期货实时日K线

查询期货合约当前交易日截至请求时刻的实时日 K 线。接口以实时 1 分钟 K 线聚合生成当日日 K。必填 `--symbols`，逗号分隔，1～20 个。

外部接口：`GET /api/v4/market/data/futures-realtime-day-kline`。

| 项目 | 说明 |
|------|------|
| 输入参数 | `symbols`（必填）：1～20 个合约代码；接口侧以逗号分隔发送，如 `symbols=A2611.DCE,CU2611.SHFE`，兼容旧的重复参数格式 |
| 响应结构 | `code` / `message` / `data`；`data` 为按请求顺序排列的分组数组，每项含 `symbol`、`items`、`total` |
| 分组字段 | `symbol`（请求中的合约代码）、`items`（该合约实时日 K 线列表）、`total`（`items` 条数，无行情时为 0） |
| 每根 K 线字段 | symbol / datetime / trade_date / open / high / low / close / volume / amount / vwap / open_interest / dominant_contract / forward_factor / backward_factor |
| 单次限量 | 一次支持 1～20 个合约；不提供 limit / start / end / 周期参数 |

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> futures-realtime-day-kline --symbols A2611.DCE,CU2611.SHFE
```

## 注意事项

- **交易所后缀规则（必读）**：合约代码格式为 `<合约代码>.<交易所代码>`，只接受交易所全称后缀 `.SHFE`、`.INE`、`.DCE`、`.CZCE`、`.CFFEX`、`.GFEX`；短后缀 `.SHF`、`.CZC`、`.CFE`、`.GFE` 及其它未列出的后缀会返回 HTTP 400；无后缀的裸合约代码仍兼容。
- 不变参数：本接口固定返回当前交易日实时日 K 线，不支持 `limit`、`start`、`end` 或周期参数，也不能指定历史日期。
- 外层分组的 `symbol` 保留请求值；内层 K 线的 `symbol` 为去除交易所后缀并转小写后的合约代码。
- 每组的 `total` 等于该组 `items` 的条数，无行情时为 0；每个合约通常返回 0 或 1 条记录。
- 盘中 `close` 为截至请求时刻的最新价，`volume`、`amount`、`vwap`、`open_interest` 均为截至请求时刻的累计值，不应当作当日最终收盘数据。
- `dominant_contract`、`forward_factor`、`backward_factor` 当前返回 `null`。
- 历史日 K 线请使用 `futures-kline`（单合约）或 `futures-kline-batch`（批量）；实时分钟 K 线请使用 `futures-realtime-minute-kline`。
