---
name: exchange-margin-summaries
description: 查询交易所融资融券汇总日度数据。用户询问沪深北交易所融资融券余额、买入额、偿还额或融券数据时使用。
---

# 交易所融资融券汇总日度

外部接口：`GET /api/v1/market/data/exchange-margin-summaries`

必填：`--start-date`、`--end-date`（YYYYMMDD）。可选：`--exchange`、`--page`、`--page-size`、`--all`。

```bash
python <RUN_PY> exchange-margin-summaries --start-date 20260701 --end-date 20260731 --page 1 --page-size 100
```

返回分页 JSON，记录位于 `records`，包含 `exchange`、`trade_date`、`rzye`、`rzmre`、`rzche`、`rqyl`、`rqylje`、`rqmcl`、`rzrqjyzl`。
