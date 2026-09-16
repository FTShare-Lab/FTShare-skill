---
name: risk-warning-stocks
description: 按交易日查询风险警示股票列表。必填 --date，可选 --page、--page-size。接口：GET /api/v1/market/data/risk-warning-stocks。
---

# 风险警示股

按指定交易日查询风险警示股票列表。接口：GET `/api/v1/market/data/risk-warning-stocks`。

## 参数

- `--date`：必填，交易日，格式 `YYYYMMDD`。
- `--page`：可选，页码，默认 1。
- `--page-size`：可选，每页条数，默认 50，最大 200。

响应为统一 `code/message/data` JSON，分页记录位于 `data.records`。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送，并设置 `Content-Type: application/json`。缺失凭据时不会发起请求。

```bash
python <RUN_PY> risk-warning-stocks --date 20260829 --page 1 --page-size 5
```
