---
name: index-minutes-batch
description: 批量查询 指数历史分钟 K 线。用户询问多只指数的分钟行情时使用。
---

# 批量指数历史分钟行情

接口：`GET /api/v2/market/data/index_minutes/batch`。必填 `--symbols`、`--since-ts-millis`、`--until-ts-millis`；`--symbols` 使用逗号分隔，最多 20 只；可选 `--interval-value`、`--limit`，时间跨度不超过 3 天，`limit` 范围 1~1000。

```bash
python <RUN_PY> index-minutes-batch --symbols 000300.SH,399001.SZ --since-ts-millis 1787189400000 --until-ts-millis 1787191200000 --limit 5
```

返回 `code/message/data`，`data` 为每只标的的 `symbol`、`total` 和 `items` 列表；不是分页接口。
