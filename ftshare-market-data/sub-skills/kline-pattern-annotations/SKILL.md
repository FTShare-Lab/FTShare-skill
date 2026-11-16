---
name: kline-pattern-annotations
description: "查询指定快照日的 K 线形态识别标注，包含形态名、窗口区间、方向、状态、置信度和识别理由。接口：GET /api/v3/market/data/kline-pattern-annotations。"
---

# K线形态标注

接口：GET `/api/v3/market/data/kline-pattern-annotations`。参数和响应以 [《K线形态标注》](https://market.ft.tech/gateway/doc/pages/l31zj3q1.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--date` | 否 | 快照日期，格式 `YYYYMMDD`；缺省为当天，按 CST 自然日计算。 |
| `--symbol` | 否 | 证券代码，六位数字，例如 `000002`；不带交易所后缀。 |
| `--pattern` | 否 | 形态名等值筛选，例如 `黄金坑`、`W底`、`V形底`、`上升旗形`、`双重顶`。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page_size` | 否 | 每页条数，默认 `50`，最大 `4000`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`date`、`stock_code`、`stock_name`、`start_time`、`end_time`、`pattern`、`direction`、`status`、`confidence`、`current_phase`、`rationale`、`image_hash`

## 调用示例

```bash
python <RUN_PY> kline-pattern-annotations --date 20260918 --page 1
```
