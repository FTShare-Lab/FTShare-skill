---
name: news-reaction-snapshot
description: 查询指定 A 股的新闻市场反应快照（消息量价共振）。用户询问个股消息面与量价的共振、新闻反应方向或阶段时使用。
---

# 消息量价共振

接口：`GET /api/v3/market/data/news-reaction-snapshot`

参数：`--symbol` 必填（带交易所后缀，如 `600519.SH`，兼容 `.XSHG/.XSHE/.BJSE`、`SH:600000` 等写法，响应统一为六位数字加 `.SH/.SZ/.BJ`）；`--start-date`、`--end-date` 必填（`YYYYMMDD` 或 `YYYY-MM-DD`，与起始日相隔不超过 31 天）；`--lookback-hours` 可选，仅 `24` 或 `48`，不传返回两套窗口；`--page` 默认 1（上限 1000）、`--page-size` 默认 50（上限 200）；支持 `--all` 自动翻页。

```bash
python <RUN_PY> news-reaction-snapshot --symbol 600519.SH --start-date 20260818 --end-date 20260828 --lookback-hours 48 --page 1 --page-size 5
```

返回 `code/message/data` 分页信封，快照位于 `data.records`；每条包含 `trade_date`、`symbol`、`stock_name`、`lookback_hours`、`reaction_direction`、`reaction_stage`、`trend_interaction`、`price_volume_signature`、`relative_performance`、`participation_state`、`event_attention_state`、`observation_sufficiency`、`state_summary`、`confidence`、`data_insufficient`、`signal_ambiguous`。枚举字段保持英文码，中文解释只出现在 `state_summary`；接口只读历史成功快照，不重新调用模型，也不预测收益。
