---
name: ashare-interactions
description: "按提问日期范围查询 A 股上市公司互动问答，返回公司、行业、问题、答复及其时间等业务信息。接口：GET /api/v2/market/data/ashare-interactions。"
---

# e互动

接口：GET `/api/v2/market/data/ashare-interactions`。参数和响应以 [《e互动》](https://market.ft.tech/gateway/doc/pages/wzxfo6gw.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--start_date` | 是 | 开始日期，格式 `YYYYMMDD` |
| `--end_date` | 是 | 结束日期，格式 `YYYYMMDD`，不能早于 `start_date` |
| `--trade_code` | 否 | 股票代码，精确匹配，例如 `000001.SZ` |
| `--company_name` | 否 | 公司名称，精确匹配 |
| `--industry_code` | 否 | 行业代码，精确匹配 |
| `--industry_name` | 否 | 行业名称，精确匹配 |
| `--data_source` | 否 | 数据来源，精确匹配 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page_size` | 否 | 每页数量，默认 100，范围 1–1000 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`trade_code`、`company_name`、`industry_name`、`industry_code`、`id`、`time_q`、`question`、`answer`、`time_a`、`data_source`

## 调用示例

```bash
python <RUN_PY> ashare-interactions --start_date 20260828 --end_date 20260828 --page 1 --page_size 5
```
