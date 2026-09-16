---
name: stock-reports
description: 查询 A 股研报列表。按 stock-code 查询个股历史，或按 type 与日期范围查询；page 和 page-size 必填。
---

# 研报列表

外部接口：`GET /api/v2/market/data/report/stock-reports`。

支持两种模式：

- 按个股查询：`--stock-code`，`--type` 可省略，传入时必须为 `StockReport`。
- 按类型和日期查询：不传 `--stock-code` 时，必须提供 `--type` 与 `--start-date`；`--end-date` 可省略，日期范围最多 3 天。

`--page` 与 `--page-size` 必填。返回 `code`、`message` 和分页 `data`，记录含研报评级、研究机构、研究员及用于下载正文的 `url_hash`。所有请求必须设置 `FTSHARE_API_KEY`，缺失凭据时不会发起请求。

```bash
python <RUN_PY> stock-reports --stock-code 600036.SH --page 1 --page-size 20
python <RUN_PY> stock-reports --type MacroReport --start-date 20260821 --page 1 --page-size 20
```
