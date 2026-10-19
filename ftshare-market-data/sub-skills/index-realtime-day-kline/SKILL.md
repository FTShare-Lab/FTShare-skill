---
name: index-realtime-day-kline
description: 查询指数当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/index-realtime-day-kline。
---

# 指数实时日K线

查询指数当前交易日实时日 K 线。必填 `--symbols`，CLI 按空格分隔；接口侧以逗号分隔发送（如 `000300.CSI,000905.CSI`），也兼容旧的 JSON 字符串数组格式，支持 `.SH`/`.XSHG`、`.SZ`/`.XSHE`、`.BJ`/`.BJSE`、`.CSI` 后缀和可推断市场的六码裸代码。接口：GET /api/v4/market/data/index-realtime-day-kline。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> index-realtime-day-kline --symbols 000300.CSI 000905.CSI
```
