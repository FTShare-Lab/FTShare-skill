---
name: limit-event-timeline
description: "查询个股涨跌停事件 3 秒级时间线。可用参数：--symbol、--trade_date、--page、--page_size。接口：GET /api/v2/market/data/limit-event-timeline-3s。同义：打板。"
---

# 涨跌停事件时间线

接口：GET `/api/v2/market/data/limit-event-timeline-3s`。参数和响应以 [《涨跌停事件时间线》](https://market.ft.tech/gateway/doc/pages/wykygobl.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 否 | 标的代码，如 000001.XSHE；不传返回全市场（暂不支持北交所信息） |
| `--trade_date` | 否 | 交易日期，格式 `YYYYMMDD`；不传或传当日时查询实时数据 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`symbol`、`trade_date`、`ready`、`status`、`limit_up_price`、`limit_down_price`、`limit_up_enter`、`limit_up_break`、`limit_down_enter`、`limit_down_break`、`first_limit_up_time`、`limit_up_break_count`、`last_limit_down_time`、`limit_down_break_count`、`limit_up_seal_value`、`limit_down_seal_value`

## 调用示例

```bash
python <RUN_PY> limit-event-timeline --symbol 000002.SZ --trade_date 20260918 --page 1 --page_size 50
```

接口仅返回当日真正触及涨跌停的标的；未触板的代码（如 `600519.SH`）`data` 为 `null`。不传 `--symbol` 时返回当日全部涨跌停标的。
