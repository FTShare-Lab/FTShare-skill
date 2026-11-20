---
name: index-realtime-minute-kline
description: 查询指数当前交易日实时 1 分钟 K 线。必填 --symbols，按空格分隔，单次最多 20 个。接口：GET /api/v4/market/data/index-realtime-minute-kline。
---

# 指数实时分钟K线

接口：`GET /api/v4/market/data/index-realtime-minute-kline`。在线文档：[《指数实时分钟K线》](https://market.ft.tech/gateway/doc/pages/bzo0v549.md)

查询指数当前交易日实时 1 分钟 K 线。必填 `--symbols`，CLI 按空格分隔，单次最多 20 个；接口侧以逗号分隔发送（如 `000300.CSI,000905.CSI`），也兼容旧的 JSON 字符串数组格式，支持 `.SH`/`.XSHG`、`.SZ`/`.XSHE`、`.BJ`/`.BJSE`、`.CSI` 后缀和可推断市场的六码裸代码。接口：GET /api/v4/market/data/index-realtime-minute-kline。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> index-realtime-minute-kline --symbols 000300.CSI 000905.CSI
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbols` | 是 | 逗号分隔的指数代码列表，如 `000300.CSI,000905.CSI`；也兼容 JSON 字符串数组格式；支持带交易所后缀和可推断市场的六码裸代码；单次 1 至 20 个 |

## 返回

- 返回：`data` 为记录数组（无外层容器，直接遍历）
- 分页字段：`total`
- 记录字段：`symbol`、`open`、`high`、`low`、`close`、`ts_millis`、`ts_millis_open`、`turnover`、`volume`
