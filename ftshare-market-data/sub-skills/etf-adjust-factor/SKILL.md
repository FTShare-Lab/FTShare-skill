---
name: etf-adjust-factor
description: 查询 ETF 复权因子。支持 --symbol、--trade-date 或带 symbol 的 --start-date/--end-date 区间查询，以及 --page/--page-size。接口：GET /api/v1/market/data/etf-adjust-factor。
---

# ETF复权因子

接口：`GET /api/v1/market/data/etf-adjust-factor`。在线文档：[《ETF复权因子》](https://market.ft.tech/gateway/doc/pages/wj8y3my9.md)

查询 ETF 复权因子。支持 --symbol、--trade-date 或带 symbol 的 --start-date/--end-date 区间查询，以及 --page/--page-size。接口：GET /api/v1/market/data/etf-adjust-factor。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> etf-adjust-factor
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 否 | ETF 代码，支持纯数字或带后缀格式；区间扫描必填 |
| `--trade-date` | 否 | 交易日期 YYYYMMDD；空则默认当天，非交易日回退前一交易日 |
| `--start-date` | 否 | 区间起始日期 YYYYMMDD；区间扫描必填且需配 symbol |
| `--end-date` | 否 | 区间结束日期 YYYYMMDD；区间扫描必填且需配 symbol |
| `--page` | 否 | 页码，从 1 开始；默认 1 |
| `--page-size` | 否 | 每页条数，默认 50，最大 2000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`symbol`、`trade_date`、`adj_factor`、`ex_adj_factor`
