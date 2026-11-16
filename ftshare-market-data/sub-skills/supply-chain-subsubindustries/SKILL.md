---
name: supply-chain-subsubindustries
description: "查询指定行业直接对应的子子行业名称列表。可用参数：--industry_name。接口：GET /api/v3/market/data/supply-chain/subindustry-subsubindustries。"
---

# 供应链子行业层级展开

接口：GET `/api/v3/market/data/supply-chain/subindustry-subsubindustries`。参数和响应以 [《供应链子行业层级展开》](https://market.ft.tech/gateway/doc/pages/j7xpe5zx.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--industry_name` | 是 | 行业名称，去除首尾空白后长度须为 1 至 256 个字符。 |

## 返回

- 记录字段：`industry_name`、`subindustry_names`

## 调用示例

```bash
python <RUN_PY> supply-chain-subsubindustries --industry_name 银行
```
