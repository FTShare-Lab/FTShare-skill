---
name: cashflow-stock-code
description: 查询现金流支持股票代码。接口：GET /api/v2/market/data/finance/cashflow-stock-code。所有请求必须设置 FTSHARE_API_KEY。
---

# 现金流支持股票代码

接口：GET `/api/v2/market/data/finance/cashflow-stock-code`。参数和响应以 `ftshare-doc/api-doc/股票数据/财务数据/现金流支持股票代码.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> cashflow-stock-code --stock_code 600519 --stock_name 1
```
