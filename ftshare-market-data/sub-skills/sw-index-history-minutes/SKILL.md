---
name: sw-index-history-minutes
description: 查询申万指数历史一分钟 K 线。用户询问申万行业指数分钟行情时使用。
---

# 申万指数历史分钟 K 线

接口：`GET /api/v1/market/data/sw-index/history-minutes`。必填 `--index-code`、`--start-date`、`--end-date`；可选 `--page` 和 `--page-size`（最大 200），支持 `--all` 自动翻页。

```bash
python <RUN_PY> sw-index-history-minutes --index-code 801001 --start-date 20260811 --end-date 20260811 --page 1 --page-size 50
```

返回 `code/message/data` 分页信封，分钟记录位于 `data.records`。
