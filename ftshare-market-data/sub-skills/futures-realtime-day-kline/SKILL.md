---
name: futures-realtime-day-kline
description: 查询期货合约当前交易日的实时日 K 线（futures_realtime_day_kline，GET /api/v4/market/data/futures-realtime-day-kline）。用户问期货实时日 K、当下期货开高低收、多只期货合约今日行情时使用。必填 --symbols，逗号分隔，1～20 个。
---

# 期货实时日K线

查询期货合约当前交易日截至请求时刻的实时日 K 线。接口以实时 1 分钟 K 线聚合生成当日日 K。必填 `--symbols`，逗号分隔，1～20 个。

外部接口：`GET /api/v4/market/data/futures-realtime-day-kline`。

| 项目 | 说明 |
|------|------|
| 输入参数 | `symbols`（必填）：1～20 个合约代码；接口侧以重复参数发送，如 `symbols=A2611.DCE&symbols=CU2611.SHF` |
| 响应结构 | `code` / `message` / `data`；`data` 为对象，含 `items`（分组数组）与 `total`（请求的合约数量） |
| 分组字段 | `symbol`（请求中的合约代码）、`items`（该合约实时日 K 线列表）、`total`（该合约返回的日 K 条数） |
| 每根 K 线字段 | symbol / datetime / trade_date / open / high / low / close / volume / amount / vwap / open_interest / dominant_contract / forward_factor / backward_factor |
| 单次限量 | 一次支持 1～20 个合约；不提供 limit / start / end / 周期参数 |

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> futures-realtime-day-kline --symbols A2611.DCE,CU2611.SHF
```

## 注意事项

- **交易所后缀规则（必读）**：合约代码格式为 `<合约代码>.<三字符交易所后缀>`，本接口支持 `.DCE`、`.SHF`、`.CZC`、`.INE`、`.GFE`、`.CFE`；长后缀 `.SHFE`、`.CZCE`、`.GFEX`、`.CFFEX` 等不支持，会返回 HTTP 400，请勿照搬公开行情数据源写法。
- 不变参数：本接口固定返回当前交易日实时日 K 线，不支持 `limit`、`start`、`end` 或周期参数，也不能指定历史日期。
- 外层分组的 `symbol` 保留请求值；内层 K 线的 `symbol` 为去除交易所后缀并转小写后的合约代码。
- `data.total` 为请求的合约数量；每组的 `total` 为该合约返回的日 K 条数。每个合约通常返回 0 或 1 条记录。
- 盘中 `close` 为截至请求时刻的最新价，`volume`、`amount`、`vwap`、`open_interest` 均为截至请求时刻的累计值，不应当作当日最终收盘数据。
- `dominant_contract`、`forward_factor`、`backward_factor` 当前返回 `null`。
- 历史日 K 线请使用 `futures-kline`（单合约）或 `futures-kline-batch`（批量）；实时分钟 K 线请使用 `futures-realtime-minute-kline`。
