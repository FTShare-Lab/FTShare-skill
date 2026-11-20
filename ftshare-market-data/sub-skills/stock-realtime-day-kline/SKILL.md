---
name: stock-realtime-day-kline
description: 查询股票当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/stock-realtime-day-kline。
---

# 股票实时日K线

接口：`GET /api/v4/market/data/stock-realtime-day-kline`。在线文档：[《股票实时日K线》](https://market.ft.tech/gateway/doc/pages/pe9d82db.md)

查询股票当前交易日实时日 K 线。必填 `--symbols`，CLI 按空格分隔；接口侧以逗号分隔发送（如 `600519.SH,000001.SZ`），也兼容旧的 JSON 字符串数组格式，支持交易所后缀和可推断市场的六码裸代码。接口：GET /api/v4/market/data/stock-realtime-day-kline。

每根 K 线字段：symbol / open / high / low / close / ts_millis / ts_millis_open / turnover / volume / turnover_rate（换手率），返回当前交易日截至最新行情时刻的数据。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-realtime-day-kline --symbols 600519.SH 000001.SZ
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbols` | 是 | 逗号分隔的股票代码列表，如 `600519.SH,000001.SZ`；也兼容 JSON 字符串数组格式；支持带交易所后缀和可推断市场的六码裸代码 |

## 返回

- 返回：`data` 为记录数组（无外层容器，直接遍历）
- 分页字段：`total`
- 记录字段：`symbol`、`open`、`high`、`low`、`close`、`ts_millis`、`ts_millis_open`、`turnover`、`volume`、`turnover_rate`
