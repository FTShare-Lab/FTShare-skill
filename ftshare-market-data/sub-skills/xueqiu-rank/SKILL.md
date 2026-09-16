---
name: xueqiu-rank
description: 查询雪球股票排名。接口：GET /api/v1/market/data/xueqiu-rank。所有请求必须设置 FTSHARE_API_KEY。
---

# 雪球股票排名

接口：GET `/api/v1/market/data/xueqiu-rank`。参数和响应以 `ftshare-doc/api-doc/股票数据/特色数据/雪球股票排名.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> xueqiu-rank --page 1 --display_name 1 --metric_name 1 --rank_no 1 --stock_name 1 --metric_value 1
```
