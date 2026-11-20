---
name: stock-ggmx-buy-ranking
description: 查询董监高增持排行。可选 --time-range（1m/3m/6m/1y/2y）、--page、--page-size。接口：GET /api/v2/market/data/holder/stock-ggmx-buy-ranking。
---

# 董监高增持排名

接口：`GET /api/v2/market/data/holder/stock-ggmx-buy-ranking`。在线文档：[《董监高增持排名》](https://market.ft.tech/gateway/doc/pages/zbq8gkmi.md)

查询董监高增持排行。可选 --time-range（1m/3m/6m/1y/2y）、--page、--page-size。接口：GET /api/v2/market/data/holder/stock-ggmx-buy-ranking。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-ggmx-buy-ranking
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--time-range` | 否 | 时间范围：1m / 3m / 6m / 1y / 2y，默认 1m，别名 timeRange |
| `--page` | 否 | 页码 |
| `--page-size` | 否 | 每页条数，别名 pageSize |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`stockCode`、`stockName`、`totalShares`、`totalAmountWan`、`latestPrice`、`priceChangeRate`、`timeRange`、`startDate`、`latestChangeDate`
