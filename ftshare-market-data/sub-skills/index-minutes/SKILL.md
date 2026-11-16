---
name: index-minutes
description: 指数历史分钟行情。必填 --symbol；可选日期和分页参数。 用户询问指数历史分钟行情时使用。
---

# 指数历史分钟行情

接口：`GET /api/v2/market/data/index_minutes`。在线文档：[《指数历史分钟行情》](https://market.ft.tech/gateway/doc/pages/ls85mq5n.md)

外部接口：`GET /api/v2/market/data/index_minutes`。

必填 --symbol；可选日期和分页参数。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> index-minutes --symbol 000300.SH --since-ts-millis 1787189400000 --until-ts-millis 1787191200000 --limit 5
```

接口返回 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--symbol` | 是 | 指数标的代码（带市场后缀，如 `000300.SH`、`399001.SZ`、`000300.CSI`） |
| `--interval-value` | 否 | 分钟周期数值，必须大于 0 的整数；缺省为 `1`（1 分钟 K 线） |
| `--since-ts-millis` | 是 | 开始时间戳（毫秒）；与 until 跨度不超过 30 个北京时间自然日（包含起止日期） |
| `--until-ts-millis` | 是 | 结束时间戳（毫秒） |
| `--limit` | 否 | 返回条数上限（1~1000）；不传时返回查询范围内全部记录 |
| `--adjust-kind` | 否 | 复权：none（默认，不复权）/forward（前复权）/backward（后复权） |

## 返回

- 记录字段：`open`、`high`、`low`、`close`、`ts_millis`、`ts_millis_open`、`turnover`、`volume`
