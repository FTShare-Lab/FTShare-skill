---
name: ashare-rating-factor-snapshot
description: 查询指定 A 股的 Top-K 相关公司。用户询问股票相关性、相关公司排名或相关性评分时使用。
---

# A股相关性 Top-K

接口：`GET /api/v3/market/data/ashare-rating-factor-snapshot`。在线文档：[《A股相关性 Top-K》](https://market.ft.tech/gateway/doc/pages/hdns2u7u.md)

外部接口：`GET /api/v3/market/data/ashare-rating-factor-snapshot`

必填：`--trade-code`。可选：`--date`（YYYYMMDD）、`--top-k`（1–500，默认由服务端设为 20）。不分页。

```bash
python <RUN_PY> ashare-rating-factor-snapshot --trade-code 600000.SH --date 20260819 --top-k 10
```

返回 `code`、`message`、`data`，其中 `data.related_securities` 按相关性分数返回相关证券。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-code` | 是 | 目标股票代码，必须包含交易所后缀，格式为 `六位数字.SH` 或 `六位数字.SZ` |
| `--date` | 否 | 快照日期，格式 `YYYYMMDD`，省略时使用最新快照 |
| `--top-k` | 否 | 返回的相关公司数量，默认 20，范围 1–500 |

## 返回

- 记录字段：`trade_code`、`related_securities`、`score`、`rank`、`security_name`、`rating`
