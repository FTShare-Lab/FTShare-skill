---
name: daec-market-snapshot
description: "查询全市场或单个交易所的行情快照，返回市场状态、涨跌幅、成交量、成交额，以及按涨跌幅区间统计的涨跌分布（9 档）。可用参数：--scope。接口：GET /api/v1/market/data/daec/market/snapshot。"
---

# 市场行情快照

接口：GET `/api/v1/market/data/daec/market/snapshot`。参数和响应以 [《市场行情快照》](https://market.ft.tech/gateway/doc/pages/6fn39pnw.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--scope` | 否 | 市场范围：`ChinaStock`（默认）/ `Xshg` / `Xshe` / `Bjse` |

## 返回

- 记录字段：`status`、`change_rate`、`volume`、`turnover`、`prev_turnover`、`distribution`、`up_limited`、`up_5pct_to_limited`、`up_1pct_to_5pct`、`up_0pct_to_1pct`、`flat`、`down_0pct_to_1pct`、`down_1pct_to_5pct`、`down_5pct_to_limited`、`down_limited`

## 调用示例

```bash
python <RUN_PY> daec-market-snapshot
```
