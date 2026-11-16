---
name: ths-board-kline
description: "获取单个同花顺板块的历史日 K 线（开高低收 + 成交量），全部数值按字符串返回。可用参数：--board_code、--page、--page_size。接口：GET /api/v1/market/data/ths-board-kline。"
---

# 同花顺板块K线

接口：GET `/api/v1/market/data/ths-board-kline`。参数和响应以 [《同花顺板块K线》](https://market.ft.tech/gateway/doc/pages/ck1zehfw.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--board_code` | 是 | 板块代码，如 886056 |
| `--page` | 否 | 页码，从 1 开始 |
| `--page_size` | 否 | 每页数量 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`board_code`、`board_name`、`module`、`date`、`open`、`high`、`low`、`close`、`volume`

## 调用示例

```bash
python <RUN_PY> ths-board-kline --board_code 886056 --page 1
```
