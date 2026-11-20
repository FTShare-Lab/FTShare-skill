---
name: daec-prev-closes
description: "查询指定标的在一段日期区间内每个交易日的昨收价（前收盘价）。可用参数：--symbol、--since、--until。接口：GET /api/v1/market/data/daec/history/prev-closes。"
---

# 标的昨收价

接口：GET `/api/v1/market/data/daec/history/prev-closes`。参数和响应以 [《标的昨收价》](https://market.ft.tech/gateway/doc/pages/0tati78l.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 是 | 标的代码，如 `600000.XSHG` |
| `--since` | 是 | 起始日期 `YYYYMMDD`，如 `20240501` |
| `--until` | 是 | 结束日期 `YYYYMMDD`，如 `20240531` |

## 返回

- 记录字段：`date`、`prev_close`

## 调用示例

```bash
python <RUN_PY> daec-prev-closes --symbol 600000.XSHG --since 20240501 --until 20240531
```
