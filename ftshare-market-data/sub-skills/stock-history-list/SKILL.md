---
name: stock-history-list
description: 按交易日查询股票历史行情截面列表。必填 --trade-date，可选 --code、--page、--page-size。接口：GET /api/v1/market/data/stock-history-list。
---

# 股票历史列表

按交易日查询 A 股主板股票历史行情截面。接口：GET `/api/v1/market/data/stock-history-list`。

注意：`region_sector`、`cum_adjust_factor` 不可用；`pe_ttm`、`concept_sectors` 仅 2026 年起有数据。

## 参数

- `--trade-date`：必填，交易日，格式 `YYYYMMDD`。
- `--code`：可选，股票代码，支持 `600000.SH`、`600000.XSHG` 或纯六位数字。
- `--page`：可选，页码，默认 1。
- `--page-size`：可选，每页条数，默认 50，最大 200。

响应为统一 `code/message/data` JSON，分页记录位于 `data.records`。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送，并设置 `Content-Type: application/json`。缺失凭据时不会发起请求。

```bash
python <RUN_PY> stock-history-list --trade-date 20260909 --page 1 --page-size 5
python <RUN_PY> stock-history-list --trade-date 20260909 --code 600000.SH --page 1 --page-size 5
```
