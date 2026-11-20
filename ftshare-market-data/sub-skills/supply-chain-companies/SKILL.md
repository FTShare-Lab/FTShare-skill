---
name: supply-chain-companies
description: "查询指定 A 股公司的上游或下游行业及其公司候选，并按相邻行业记录分页返回。可用参数：--trade_code、--direction、--page、--page_size。接口：GET /api/v3/market/data/supply-chain/company-supply-chain-companies。"
---

# 供应链公司候选

接口：GET `/api/v3/market/data/supply-chain/company-supply-chain-companies`。参数和响应以 [《供应链公司候选》](https://market.ft.tech/gateway/doc/pages/jhcd4x3y.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade_code` | 是 | A 股交易代码，必须包含交易所后缀；支持 SH、SZ、BJ。 |
| `--direction` | 是 | 查询方向；`upstream` 表示上游，`downstream` 表示下游，不区分大小写。 |
| `--page` | 否 | 页码，从 `1` 开始，默认 `1`。 |
| `--page_size` | 否 | 每页相邻行业记录数，范围 `1` 至 `20`，默认 `20`。 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`industry_name`、`subindustry_names`、`companies`、`company_name`、`trade_code`、`index_memberships`

## 调用示例

```bash
python <RUN_PY> supply-chain-companies --trade_code 600519.SH --direction downstream --page 1
```
