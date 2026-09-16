---
name: supply-chain-subsubindustry-companies
description: 查询供应链子子行业公司映射。接口：GET /api/v3/market/data/supply-chain/subsubindustry-companies。所有请求必须设置 FTSHARE_API_KEY。
---

# 供应链子子行业公司映射

接口：GET `/api/v3/market/data/supply-chain/subsubindustry-companies`。参数和响应以 `ftshare-doc/api-doc/股票数据/特色数据/供应链子子行业公司映射.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> supply-chain-subsubindustry-companies --subindustry_name 银行
```
