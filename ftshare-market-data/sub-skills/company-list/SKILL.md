---
name: company-list
description: 查询公司列表。可选 --page、--page-size。接口：GET /api/v1/market/data/company-list。
---

# 公司列表

接口：`GET /api/v1/market/data/company-list`。在线文档：[《公司列表》](https://market.ft.tech/gateway/doc/pages/92awt2dx.md)

查询公司列表。可选 --page、--page-size。接口：GET /api/v1/market/data/company-list。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> company-list
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--page` | 否 | 页码，默认 1 |
| `--page-size` | 否 | 每页条数，默认 50，最大 200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`id`、`company_code`、`stock_code`、`stock_name`、`change_percent`、`close`、`pe`、`pb`、`total_market_value`、`circulation_value`、`circulation_capital`、`total_capital`、`listing_date`、`listing_type`、`bk`、`main_business`、`business_products`、`business_scope` …共 23 个
