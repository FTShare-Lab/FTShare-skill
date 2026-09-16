---
name: ths-board-kline
description: 查询同花顺板块K线。接口：GET /api/v1/market/data/ths-board-kline。所有请求必须设置 FTSHARE_API_KEY。
---

# 同花顺板块K线

接口：GET `/api/v1/market/data/ths-board-kline`。参数和响应以 `ftshare-doc/api-doc/股票数据/打板专题数据/同花顺板块K线.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> ths-board-kline --board_code 886056 --page 1
```
