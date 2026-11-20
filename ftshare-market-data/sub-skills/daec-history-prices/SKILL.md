---
name: daec-history-prices
description: "查询指定标的的 1 分钟分时数据（价格、均价、成交量、成交额）。可用参数：--symbol、--range、--days、--ts_ms。接口：GET /api/v4/market/data/daec/history/prices。"
---

# 标的分时数据

接口：GET `/api/v4/market/data/daec/history/prices`。参数和响应以 [《标的分时数据》](https://market.ft.tech/gateway/doc/pages/2fc0d5ut.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 是 | 标的代码，如 `600000.XSHG` |
| `--range` | 否 | 预置时间区间：`Today`（当日）/ `FiveDays`（近 5 日，默认） |
| `--days` | 否 | 近 N 个交易日至今，如 `10`；与 `range` / `ts_ms` 互斥 |
| `--ts_ms` | 否 | 起始毫秒时间戳，如 `1779931980000`；与 `range` / `days` 互斥 |

## 返回

- 记录字段：`ts_ms`、`price`、`avg_price`、`volume`、`turnover`

## 调用示例

```bash
python <RUN_PY> daec-history-prices --symbol 600519.SH
```
