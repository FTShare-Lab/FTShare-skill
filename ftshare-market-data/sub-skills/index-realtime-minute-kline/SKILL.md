---
name: index-realtime-minute-kline
description: 查询指数当前交易日实时 1 分钟 K 线。必填 --symbols，按空格分隔，单次最多 20 个。接口：GET /api/v4/market/data/index-realtime-minute-kline。
---

# 指数实时分钟K线

查询指数当前交易日实时 1 分钟 K 线。必填 --symbols，按空格分隔，单次最多 20 个。接口：GET /api/v4/market/data/index-realtime-minute-kline。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> index-realtime-minute-kline --symbols 000300.SH 399001.SZ
```
