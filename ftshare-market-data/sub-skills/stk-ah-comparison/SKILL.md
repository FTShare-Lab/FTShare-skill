---
name: stk-ah-comparison
description: 查询 A/H 股比价、涨跌幅和溢价率。用户询问港股与对应 A 股估值比较时使用。
---

# AH 股对比

接口：`GET /api/v1/market/data/hk/stk-ah-comparison`。可按 `--hk-code`、`--ts-code`、`--trade-date` 或日期区间 `--start-date`/`--end-date` 过滤；日期区间最多 30 个自然日。分页参数为 `--page`（默认 1）和 `--page-size`（默认 50，最大 1000），支持 `--all` 自动翻页。在线文档：[《AH股对比》](https://market.ft.tech/gateway/doc/pages/8fr77co1.md)

```bash
python <RUN_PY> stk-ah-comparison --hk-code 00038.HK --trade-date 20260918 --page 1 --page-size 20
```

响应为 `code/message/data` 分页信封，记录位于 `data.records`，包含双方代码、名称、收盘价、涨跌幅、A/H 比价和溢价率。

仅返回同时有 A 股和 H 股标的的公司；无 A 股对应的港股（如 `00700.HK` 腾讯控股）查不到记录。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--hk-code` | 否 | 港股股票代码，支持 `168` 或 `00168.HK` |
| `--ts-code` | 否 | A 股股票代码，格式 `xxxxxx.SH/SZ/BJ` |
| `--trade-date` | 否 | 交易日期 YYYYMMDD；传入时优先于日期区间 |
| `--start-date` | 否 | 起始日期 YYYYMMDD；未传 `trade_date` 时需与 `end_date` 同时传入，与结束日间隔不超过 30 个自然日 |
| `--end-date` | 否 | 结束日期 YYYYMMDD；未传 `trade_date` 时需与 `start_date` 同时传入，与起始日间隔不超过 30 个自然日 |
| `--page` | 否 | 页码，默认 1 |
| `--page-size` | 否 | 每页条数，默认 50，上限 1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`hk_code`、`ts_code`、`trade_date`、`hk_name`、`hk_close`、`hk_pct_chg`、`name`、`close`、`pct_chg`、`ah_comparison`、`ah_premium`
