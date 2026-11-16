---
name: futures-lists
description: "查询指定交易日的期货合约列表，包括合约代码、交易所、品种、中文名称和合约类型。可用参数：--trade-date。接口：GET /api/v1/market/data/futures/futures-lists。"
---

# 中国期货列表

接口：`GET /api/v1/market/data/futures/futures-lists`。在线文档：[《中国期货列表》](https://market.ft.tech/gateway/doc/pages/rffbd7ih.md)

外部接口：`GET /api/v1/market/data/futures/futures-lists`。

支持源接口文档列出的查询参数，handler 将参数作为 query 发送，并以 JSON 输出响应。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-date` | 否 | 交易日，格式 YYYYMMDD；不传则使用按 CST 计算的前一交易日 |

## 返回

- 记录容器：`data.items`
- 记录字段：`trade_date`、`symbol`、`exchange`、`product`、`symbol_cn_name`、`future_type`

## 调用示例

```bash
python <RUN_PY> futures-lists
```
