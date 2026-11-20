---
name: ashare-news-sentiment-factors
description: 查询指定 A 股的新闻情绪因子。必填 --trade-code 与 --start-date；区间跨度不得超过 31 天。接口：GET /api/v3/market/data/ashare-news-sentiment-factors。
---

# A股新闻情绪因子

接口：`GET /api/v3/market/data/ashare-news-sentiment-factors`。在线文档：[《A股新闻情绪因子》](https://market.ft.tech/gateway/doc/pages/zdxwn9lx.md)

查询指定 A 股的新闻情绪因子。必填 --trade-code 与 --start-date；区间跨度不得超过 31 天。接口：GET /api/v3/market/data/ashare-news-sentiment-factors。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> ashare-news-sentiment-factors --trade-code 600519.SH --start-date 20261101 --page-size 20
python <RUN_PY> ashare-news-sentiment-factors --trade-code 600519.SH --start-date 20261020 --end-date 20261113
```

> 重要：`--start-date` 实际必填 —— 不传（或只传 `--end-date`）时服务端返回 **503 服务暂不可用**，不是标准 400。
> `--start-date` 与 `--end-date` 间隔超过 31 天会返回 400「start_date 与 end_date 间隔不能超过 31 天」。
> 数据保留窗口有限（实测 2026-11 时可查的最早起始日约为 2026-08-01，更早返回 503）。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-code` | 是 | 股票代码，标准格式为 `六位数字.SH/SZ/BJ`，必须包含交易所后缀 |
| `--start-date` | 是 | 起始预测日，格式 `YYYYMMDD`，包含该日；建议提供以限制查询范围 |
| `--end-date` | 否 | 截止预测日，格式 `YYYYMMDD`，包含该日；建议与 `start_date` 一起传入 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页返回的预测因子行数，默认 50，范围 1–200 |

## 返回

- 记录容器：`data.records`
- 分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：`prediction_date`、`trade_code`、`company_name`、`sentiment_index`、`confidence`、`news_count_t2`、`news_count_t1`、`reasoning`、`predicted_at`
