---
name: stock-announcements
description: 查询 A 股公告列表。按 stock-code 或日期范围查询，page 和 page-size 必填。
---

# 公告列表

外部接口：`GET /api/v2/market/data/announcements/stock-announcements`。

必须提供 `--stock-code` 或 `--start-date`，`--type` 当前固定为 `stock`，`--page` 与 `--page-size` 必填。按日期范围查询时日期跨度最多 3 天。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-announcements --start-date 20260908 --page 1 --page-size 5
```
