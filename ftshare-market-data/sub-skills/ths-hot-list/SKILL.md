---
name: ths-hot-list
description: 查询同花顺热榜。接口：GET /api/v1/market/data/ths-hot-list。所有请求必须设置 FTSHARE_API_KEY。
---

# 同花顺热榜

接口：GET `/api/v1/market/data/ths-hot-list`。参数和响应以 `ftshare-doc/api-doc/股票数据/特色数据/同花顺热榜.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> ths-hot-list --list_type stock_day --page 1
```
