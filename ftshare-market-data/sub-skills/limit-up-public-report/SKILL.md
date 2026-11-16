---
name: limit-up-public-report
description: "查询指定标的的对外涨停归因报告，成功时 `data.text` 为报告 Markdown 原文。可用参数：--date、--security_code。接口：GET /api/v3/market/data/limit-up-reports/public-report。同义：打板。"
---

# 涨停对外归因报告

接口：GET `/api/v3/market/data/limit-up-reports/public-report`。参数和响应以 [《涨停对外归因报告》](https://market.ft.tech/gateway/doc/pages/thz9lvyg.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--date` | 是 | 交易日期，格式 `YYYYMMDD`，如 `20260724`；最早 20260424 |
| `--security_code` | 是 | 标的代码，格式为六位代码加 `.SZ`、`.SH` 或 `.BJ`，不接受 `.XSHE`、`.XSHG` 或小写后缀，如 `603976.SH` |

## 返回

- 记录字段：`text`

## 调用示例

```bash
python <RUN_PY> limit-up-public-report --date 20260724 --security_code 603976.SH
```
