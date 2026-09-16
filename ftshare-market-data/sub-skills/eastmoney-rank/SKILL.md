---
name: eastmoney-rank
description: 查询东方财富股票排名。接口：GET /api/v1/market/data/eastmoney-rank。所有请求必须设置 FTSHARE_API_KEY。
---

# 东方财富股票排名

接口：GET `/api/v1/market/data/eastmoney-rank`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/东方财富股票排名.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> eastmoney-rank --display_name 1 --metric_name 1 --rank_no 1 --stock_name 1
```
