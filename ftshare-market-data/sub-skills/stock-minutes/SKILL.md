---
name: stock-minutes
description: 股票历史分钟行情。必填 --symbol；可选日期和分页参数。 用户询问股票历史分钟行情时使用。
---

# 股票历史分钟行情

接口：`GET /api/v2/market/data/stock_minutes`。在线文档：[《股票历史分钟行情》](https://market.ft.tech/gateway/doc/pages/z9lsvrvu.md)

外部接口：`GET /api/v2/market/data/stock_minutes`。

必填 --symbol；可选日期和分页参数。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-minutes --symbol 000001.SZ --since-ts-millis 1787189400000 --until-ts-millis 1787191200000 --limit 5
```

接口返回 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

响应为数组结构（非分页），每根 K 线字段：open / high / low / close / ts_millis / ts_millis_open / turnover / volume / turnover_rate（换手率）。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 是 | 股票代码（带交易所后缀，如 `600519.SH`、`000001.SZ`、`920258.BJ`） |
| `--interval-value` | 否 | 分钟周期数值，仅支持 `1`、`5`、`15`、`30`、`60`；缺省为 `1`（1 分钟 K 线） |
| `--adjust-kind` | 否 | 复权类型，仅支持小写：`none`（默认，不复权）/ `forward`（前复权）/ `backward`（后复权） |
| `--since-ts-millis` | 是 | 开始时间戳（毫秒）；不得晚于 `until_ts_millis`，且与 `until_ts_millis` 跨度不超过 30 个北京时间自然日（包含起止日期） |
| `--until-ts-millis` | 是 | 结束时间戳（毫秒） |
| `--limit` | 否 | 返回条数上限（1~1000），截取区间内最新的 N 根；缺省返回区间内全部 |

## 返回

- 记录字段：`open`、`high`、`low`、`close`、`ts_millis`、`ts_millis_open`、`turnover`、`volume`、`turnover_rate`
