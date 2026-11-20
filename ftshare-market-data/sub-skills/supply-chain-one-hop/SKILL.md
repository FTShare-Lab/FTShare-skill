---
name: supply-chain-one-hop
description: "查询指定行业的上游或下游相邻行业名称。可用参数：--industry_name、--direction。接口：GET /api/v3/market/data/supply-chain/subindustry-supply-chain。"
---

# 供应链一跳关系

接口：GET `/api/v3/market/data/supply-chain/subindustry-supply-chain`。参数和响应以 [《供应链一跳关系》](https://market.ft.tech/gateway/doc/pages/6q0txaos.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--industry_name` | 是 | 行业名称，去除首尾空白后长度须为 1 至 256 个字符。 |
| `--direction` | 是 | 查询方向；`upstream` 表示上游，`downstream` 表示下游，不区分大小写。 |

## 返回

- 记录字段：`industry_name`、`direction`、`neighbor_industries`

## 调用示例

```bash
python <RUN_PY> supply-chain-one-hop --industry_name 银行 --direction downstream
```
