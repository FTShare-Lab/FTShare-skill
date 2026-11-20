---
name: limit-up-briefs
description: "查询指定交易日全部涨停简报，每条为一段 Markdown 文本；成功时 `data.items` 为简报列表，元素含 `security_code`、`trade_date` 和 `brief_text`。可用参数：--date。接口：GET /api/v3/market/data/limit-up-reports/briefs。同义：打板。"
---

# 涨停简报

接口：GET `/api/v3/market/data/limit-up-reports/briefs`。参数和响应以 [《涨停简报》](https://market.ft.tech/gateway/doc/pages/ycngxjlu.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--date` | 是 | 交易日期，格式 `YYYYMMDD`，如 `20260724`；最早 20260424 |

## 返回

- 记录容器：`data.items`
- 记录字段：`security_code`、`trade_date`、`brief_text`

## 调用示例

```bash
python <RUN_PY> limit-up-briefs --date 20260828
```
