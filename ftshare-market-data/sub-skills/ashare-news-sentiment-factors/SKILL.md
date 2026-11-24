---
name: ashare-news-sentiment-factors
description: 查询指定 A 股的新闻情绪因子。用户询问个股新闻情绪、利好利空判断、情绪分数或预测日因子时使用。支持单日 --date、--start-date/--end-date 区间（跨度不超过 31 天）或都不传查当天。接口：GET /api/v3/market/data/ashare-news-sentiment-factors。
---

# A股新闻情绪因子

接口：`GET /api/v3/market/data/ashare-news-sentiment-factors`。在线文档：[《A股新闻情绪因子》](https://market.ft.tech/gateway/doc/pages/zdxwn9lx.md)

查询指定 A 股的新闻情绪因子，结果按预测日升序排列。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-code` | 是 | 股票代码，标准格式 `六位数字.SH/SZ/BJ`；也接受 `SH:600000`、`600000.XSHG` 和不带后缀的 `600000` |
| `--date` | 否 | 单日预测日，格式 `YYYYMMDD`；与 `--start-date`、`--end-date` 互斥 |
| `--start-date` | 否 | 起始预测日，格式 `YYYYMMDD`，包含该日；必须与 `--end-date` 同时传入，含首尾跨度不超过 31 天 |
| `--end-date` | 否 | 截止预测日，格式 `YYYYMMDD`，包含该日；必须与 `--start-date` 同时传入，含首尾跨度不超过 31 天 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页返回的预测因子行数，默认 50，范围 1–200 |

`--date` 与 `--start-date`、`--end-date` 不能同时传入；日期区间三选一或都不传。都不传时查询当天的预测日。

## 命令

```bash
python <RUN_PY> ashare-news-sentiment-factors --trade-code 600000.SH --date 20261117
python <RUN_PY> ashare-news-sentiment-factors --trade-code 600000.SH --start-date 20261112 --end-date 20261113 --page-size 20
python <RUN_PY> ashare-news-sentiment-factors --trade-code 600000.SH
```

## 返回

- 记录容器：`data.records`；分页字段：`pageNum`、`pageSize`、`total`、`pages`
- 记录字段：
  - `prediction_date`：预测日，`YYYYMMDD`，均为交易日
  - `trade_code`：统一为 `六位数字.SH/SZ/BJ`
  - `company_name`：公司名称
  - `sentiment_index`：情绪分数，整数 **-2 ~ 2**，正为利好、负为利空、0 为无关或中性
  - `confidence`：置信度，整数 **0 ~ 2**，越大越有把握
  - `reasoning`：情绪判断依据，6 ~ 500 字；方向被调整时末尾带说明
  - `price_context`：预测日前的价格位置说明，含近期涨跌幅与价格在区间中的位置

## 注意

- 当前数据自 `20260417` 起，当日数据在凌晨 4 点前更新完成。
- 只有当日有新闻覆盖的股票才会生成记录；无新闻时返回空记录，`total` 为 0。
- 非交易日不产生数据，查询非交易日返回空 `records`。
- `start_date` 与 `end_date` 含首尾跨度超过 31 天（即 `end_date - start_date` 超过 30 天）、只传其中一个、或与 `date` 同时传入，均返回 400。