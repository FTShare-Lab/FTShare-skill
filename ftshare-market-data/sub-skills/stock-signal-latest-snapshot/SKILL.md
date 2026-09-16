---
name: stock-signal-latest-snapshot
description: 查询股票最新计算信号快照。用户询问创新高/新低、连续上涨下跌、均线突破或量价信号时使用。
---

# 信号最新快照

接口：`GET /api/v3/market/data/stock-signal-latest-snapshot`

参数：`--signal-type` 可选，支持 `new_high_month`、`new_high_60d`、`new_high_120d`、`new_high_250d`、`new_low_month`、`new_low_60d`、`new_low_120d`、`new_low_250d`、`consecutive_up`、`consecutive_down`、`consecutive_vol_up`、`consecutive_vol_down`、`break_up_ma5`、`break_up_ma10`、`break_up_ma20`、`break_down_ma5`、`break_down_ma10`、`break_down_ma20`、`vol_price_rise`、`vol_price_fall`；`--page` 默认 1，`--page-size` 默认 50，范围 1~200；支持 `--all` 自动翻页。

```bash
python <RUN_PY> stock-signal-latest-snapshot --signal-type new_high_60d --page 1 --page-size 20
```

返回统一 `code/message/data` 分页信封，记录位于 `data.records`，包含 `symbol`、`code`、`latest_trade_date`、`signal_type`、`signal_name`、`signal_detail`、`close_price` 和 `volume`。
