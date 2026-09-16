---
name: etf-realtime-day-kline
description: 查询 ETF 当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/etf-realtime-day-kline。
---

# ETF实时日K线

查询 ETF 当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/etf-realtime-day-kline。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> etf-realtime-day-kline --symbols 510300.SH 159915.SZ --symbols 510300.SH 159915.SZ
```
