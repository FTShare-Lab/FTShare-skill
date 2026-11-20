---
name: bullion-price
description: "查询指定标的的贵金属行情（日期 + 值），按 `start_date`/`end_date` 区间分页返回。接口：GET /api/v1/market/data/bullion/price。"
---

# 贵金属价格

接口：GET `/api/v1/market/data/bullion/price`。参数和响应以 [《贵金属价格》](https://market.ft.tech/gateway/doc/pages/sl79u72x.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 是 | 标的代码，如 XAUUSD、AU9999 |
| `--start_date` | 是 | 查询起始日期 YYYYMMDD |
| `--end_date` | 是 | 查询结束日期 YYYYMMDD，不得早于 start_date |
| `--page` | 是 | 当前页，从 1 开始；小于 1 时按 1 处理 |
| `--page_size` | 是 | 每页条数，范围 1～1000；超出范围时自动截断 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`date`、`value`

## 调用示例

```bash
python <RUN_PY> bullion-price --symbol XAUUSD --start_date 20260615 --end_date 20260617 --page 1 --page_size 10
```
