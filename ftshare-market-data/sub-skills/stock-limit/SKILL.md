---
name: stock-limit
description: 查询涨跌停价。接口：GET /api/v1/market/data/stk-limit。所有请求必须设置 FTSHARE_API_KEY。
---

# 涨跌停价

接口：GET `/api/v1/market/data/stk-limit`。参数和响应以 `ftshare-doc/api-doc/股票数据/行情数据/涨跌停价.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-limit --symbol 600519.SH --page 1
python <RUN_PY> stock-limit --trade_date 20260911 --page 1 --page_size 100
```

`--symbol` 可选：不传标的参数时按 `--trade_date` 返回全市场当日涨跌停截面（配合分页）；传入 `--symbol` 时查单标的单日或历史区间。
