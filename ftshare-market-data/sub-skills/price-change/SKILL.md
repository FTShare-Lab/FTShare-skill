---
name: price-change
description: "单票 N 日涨跌幅接口。可用参数：--stock_code、--base_date、--n、--direction。接口：GET /api/v2/market/data/price/get-price-change。"
---

# 价格变动

接口：GET `/api/v2/market/data/price/get-price-change`。参数和响应以 [《价格变动》](https://market.ft.tech/gateway/doc/pages/d953tpbb.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--stock_code` | 是 | 目标股票 6 位纯数字代码，兼容沪市/深市/创业板/科创板 |
| `--base_date` | 是 | 涨跌幅计算基准日，格式 YYYYMMDD |
| `--n` | 是 | 需计算的有效交易日数量，建议不超过 365 |
| `--direction` | 是 | 计算方向：forward（基准日为结束日）/ backward（基准日为开始日） |

## 返回

- 记录字段：`stock_code`、`stock_name`、`base_date`、`n`、`direction`、`start_date`、`end_date`、`actual_trading_days`、`start_price`、`end_price`、`price_change`、`change_pct`

## 调用示例

```bash
python <RUN_PY> price-change --stock_code 600519 --base_date 20260828 --n 5 --direction forward
```
