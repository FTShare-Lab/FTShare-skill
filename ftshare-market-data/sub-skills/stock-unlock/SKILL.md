---
name: stock-unlock
description: 查询限售解禁。接口：GET /api/v1/market/data/unlock/stock_unlock。所有请求必须设置 FTSHARE_API_KEY。
---

# 限售解禁

接口：GET `/api/v1/market/data/unlock/stock_unlock`。参数和响应以 `ftshare-doc/api-doc/股票数据/参考数据/限售解禁.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

查询条件二选一：传 `--stock-code`，或同时传 `--start-date` 与 `--end-date`；两种模式不能混用。

按证券代码查询单票解禁批次：

```bash
python <RUN_PY> stock-unlock --stock-code 000001 --page 1 --page_size 10
```

按解禁日期区间查询全市场解禁日历：

```bash
python <RUN_PY> stock-unlock --start-date 20260901 --end-date 20260930 --page 1 --page_size 100
```
