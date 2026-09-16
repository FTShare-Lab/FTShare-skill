---
name: stock-realtime-day-kline
description: 查询股票当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/stock-realtime-day-kline。
---

# 股票实时日K线

查询股票当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/stock-realtime-day-kline。

每根 K 线字段：symbol / open / high / low / close / ts_millis / ts_millis_open / turnover / volume / turnover_rate（换手率），返回当前交易日截至最新行情时刻的数据。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-realtime-day-kline --symbols 600519.SH 000001.SZ --symbols 600519.SH 000001.SZ
```
