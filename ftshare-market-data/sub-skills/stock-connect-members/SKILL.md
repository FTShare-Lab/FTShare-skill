---
name: stock-connect-members
description: "按互联互通方向和交易通道查询沪股通、深股通、沪市港股通或深市港股通的最新成份名单。可用参数：--direction、--channel、--page、--page_size。接口：GET /api/v1/market/data/stock-connect-members。"
---

# 互联互通成份

接口：GET `/api/v1/market/data/stock-connect-members`。参数和响应以 [《互联互通成份》](https://market.ft.tech/gateway/doc/pages/vu1fxtpg.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--direction` | 是 | 互联互通方向：`north` 北向或 `south` 南向，大小写不敏感 |
| `--channel` | 是 | 交易通道：`SH` 上交所通道或 `SZ` 深交所通道，大小写不敏感 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`symbol`

## 调用示例

```bash
python <RUN_PY> stock-connect-members --direction north --channel SH --page 1
```
