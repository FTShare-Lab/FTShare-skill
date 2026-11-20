---
name: futures-realtime-minute-kline
description: 查询期货合约当前交易日的实时 1 分钟 K 线（futures_minutes_realtime，GET /api/v4/market/data/futures_minutes/realtime）。用户问期货实时分钟行情、当下期货分钟走势、多只期货合约盘中分钟 K 线时使用。必填 --symbols，逗号分隔，1～20 个。
---

# 期货实时分钟K线

接口：`GET /api/v4/market/data/futures_minutes/realtime`。在线文档：[《期货实时分钟K线》](https://market.ft.tech/gateway/doc/pages/tvhg1858.md)

查询期货合约当前交易日截至请求时刻的实时 1 分钟 K 线。必填 `--symbols`，逗号分隔，1～20 个。

外部接口：`GET /api/v4/market/data/futures_minutes/realtime`。

| 项目 | 说明 |
|------|------|
| 输入参数 | `symbols`（必填）：1～20 个不带交易所后缀的合约代码，请求不区分大小写，CZCE 真实合约须用四位年份代码；接口侧以逗号分隔发送，如 `symbols=A2611,CU2611`，兼容旧的重复参数格式 |
| 响应结构 | `code` / `message` / `data`；`data` 为按请求顺序排列的分组数组，每项含 `symbol`、`items`、`total` |
| 分组字段 | `symbol`（请求中合约代码规范化后的裸代码，大小写沿用对应交易所官网格式）、`items`（该合约实时 1 分钟 K 线列表，按时间升序）、`total`（`items` 条数，无行情时为 0） |
| 每根 K 线字段 | bar_interval / symbol / variety / exchange / datetime / trade_date / open / high / low / close / volume / amount / vwap / open_interest / pre_settlement_price / settlement_price / high_limit_price / low_limit_price / pre_close_price / updated_at |
| 单次限量 | 一次支持 1～20 个合约；不提供 limit / start / end / 周期参数 |

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> futures-realtime-minute-kline --symbols A2611,CU2611
```

## 注意事项

- **合约代码口径（必读）**：合约代码使用不带交易所后缀的裸代码，请求不区分大小写；CZCE 真实合约必须使用四位年份代码（如 `AP2612`），三位代码不符合接口代码规范。
- 不变参数：本接口固定返回当前交易日实时 1 分钟 K 线，不支持 `limit`、`start`、`end` 或分钟周期参数，也不能指定历史日期。
- 外层分组的 `symbol` 和 K 线的 `symbol` 均为不带交易所后缀的官网合约代码，大小写沿用对应交易所官网格式。
- 每组的 `total` 等于该组 `items` 的条数（不是分页总量）。
- 每个合约返回截至请求时刻的全部可用记录，结果按时间升序；无可用行情时该组 `items` 为 `[]`、`total` 为 0。
- 历史分钟 K 线请使用 `futures-minutes`；实时日 K 线请使用 `futures-realtime-day-kline`。
