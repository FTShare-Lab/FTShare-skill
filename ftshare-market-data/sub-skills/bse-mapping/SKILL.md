---
name: bse-mapping
description: 查询北交所代码映射。可选 --o-code。接口：GET /api/v1/market/data/bse-mapping。
---

# 北交所映射

接口：`GET /api/v1/market/data/bse-mapping`。在线文档：[《北交所映射》](https://market.ft.tech/gateway/doc/pages/dk0d6dqi.md)

查询北交所代码映射。可选 --o-code。接口：GET /api/v1/market/data/bse-mapping。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> bse-mapping
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--o-code` | 否 |  |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`stock_name`、`old_code`、`new_code`、`listing_date`
