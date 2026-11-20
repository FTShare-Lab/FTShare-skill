---
name: supply-chain-subsubindustry-companies
description: "查询指定子子行业对应的父行业、指数成分公司及公司明细。可用参数：--subindustry_name。接口：GET /api/v3/market/data/supply-chain/subsubindustry-companies。"
---

# 供应链子子行业公司映射

接口：GET `/api/v3/market/data/supply-chain/subsubindustry-companies`。参数和响应以 [《供应链子子行业公司映射》](https://market.ft.tech/gateway/doc/pages/64iwxu5j.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--subindustry_name` | 是 | 子子行业名称，去除首尾空白后长度须为 1 至 256 个字符。 |

## 返回

- 记录字段：`subindustry_name`、`parent_industries`、`hs300_companies`、`csi1000_companies`、`hs300_count`、`csi1000_count`、`companies`、`company_count`、`company_name`、`trade_code`、`index_memberships`、`company_aliases`、`source_subindustry_names`、`source_origins`

## 调用示例

```bash
python <RUN_PY> supply-chain-subsubindustry-companies --subindustry_name 银行
```
