---
name: etf-minutes-batch
description: 批量查询 ETF 历史分钟 K 线。用户询问多只 ETF 的分钟行情时使用。
---

# 批量 ETF 历史分钟行情

接口：`GET /api/v2/market/data/etf_minutes/batch`。必填 `--symbols`、`--since-ts-millis`、`--until-ts-millis`；`--symbols` 使用逗号分隔，最多 20 只；可选 `--interval-value`、`--adjust-kind`、`--limit`。时间跨度不超过 3 天，`limit` 范围 1~1000。

```bash
python <RUN_PY> etf-minutes-batch --symbols 510300.SH,159915.SZ --since-ts-millis 1787189400000 --until-ts-millis 1787191200000 --limit 5
```

返回 `code/message/data`，`data` 为每只标的的 `symbol`、`total` 和 `items` 列表；不是分页接口。
