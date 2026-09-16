---
name: kline-pattern-annotations
description: 查询K线形态标注。接口：GET /api/v3/market/data/kline-pattern-annotations。所有请求必须设置 FTSHARE_API_KEY。
---

# K线形态标注

接口：GET `/api/v3/market/data/kline-pattern-annotations`。参数和响应以 `ftshare-doc/api-doc/股票数据/特色数据/K线形态标注.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> kline-pattern-annotations --symbol 000002 --page 1
```
