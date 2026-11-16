---
name: yzxdr-detail
description: "按年份/季度（且可按股票代码过滤）查询一致行动人持股明细，返回每组一致行动人的合计持股比例与股数，以及组内每位股东的排名、持股数与市值、可流通股、增减变化等。用户问一致行动人、共同持股或股东持股集中度时使用。同义：一致行动人明细。"
---

# 一致行动人明细

接口：GET `/api/v1/market/data/yzxdr-detail`。参数和响应以 [《一致行动人明细》](https://market.ft.tech/gateway/doc/pages/zpyi79up.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--year` | 是 | 年份（如 2026） |
| `--quarter` | 是 | 季度，1-4 |
| `--stock_code` | 否 | 股票代码，6 位数字 |
| `--page` | 否 | 页码，默认 1 |
| `--page_size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`id`、`data_date`、`stock_code`、`stock_name`、`group_ratio`、`group_shares`、`row_no`、`holder_name`、`holder_rank`、`hold_shares`、`hold_value`、`tradable_shares`、`hold_ratio`、`shares_change`、`ratio_change`、`holder_type`、`share_type`、`is_controlling` …共 21 个

## 调用示例

```bash
python <RUN_PY> yzxdr-detail --year 2026 --quarter 2 --page 1 --stock_code 000001
```
