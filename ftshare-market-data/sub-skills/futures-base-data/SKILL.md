---
name: futures-base-data
description: "查询指定交易日的期货合约要素，包括交易单位、最小变动价位、保证金、合约乘数、上市日、最后交易日和交割信息。可用参数：--trade-date、--symbol。接口：GET /api/v1/market/data/futures/futures-base-data。"
---

# 中国期货基础数据

接口：`GET /api/v1/market/data/futures/futures-base-data`。在线文档：[《中国期货基础数据》](https://market.ft.tech/gateway/doc/pages/qd32szq6.md)

外部接口：`GET /api/v1/market/data/futures/futures-base-data`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-date` | 否 | 交易日，格式 YYYYMMDD；不传则使用按 CST 计算的前一交易日 |
| `--symbol` | 否 | 不带交易所后缀的合约代码，例如 `CU2609`；请求不区分大小写，CZCE 真实合约必须使用四位年份代码（如 `AP2612`，三位代码返回参数错误）；不传或为空表示该日全部 |

## 返回

- 记录容器：`data.items`；合法格式但该交易日无对应数据时返回 HTTP 200 的空结果（`data` 可能为 `null`），非法代码返回 HTTP 400
- 记录字段：`trade_date`、`exchange`、`symbol`、`product`、`symbol_cn_name`、`trade_unit`、`price_unit`、`put_price`、`min_put_price_info`、`margin_info`、`trade_months_info`、`trade_hours_info`、`last_trade_date`、`last_trade_date_hour`、`delivery_date`、`multiplier`、`list_date`、`de_list_tdate` …共 28 个

## 调用示例

```bash
python <RUN_PY> futures-base-data --trade-date 20260918
```
