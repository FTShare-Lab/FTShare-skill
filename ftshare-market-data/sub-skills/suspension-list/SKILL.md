---
name: suspension-list
description: 查询停牌股票列表。可选 --trade-date。接口：GET /api/v1/market/data/suspension-list。
---

# 停牌列表

接口：`GET /api/v1/market/data/suspension-list`。在线文档：[《停牌列表》](https://market.ft.tech/gateway/doc/pages/e42u4fqk.md)

查询停牌股票列表。可选 --trade-date。接口：GET /api/v1/market/data/suspension-list。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> suspension-list
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-date` | 否 | 交易日，格式 YYYYMMDD，默认当天 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`symbol`、`suspension_type`、`suspend_time`、`resume_time`、`reason`
