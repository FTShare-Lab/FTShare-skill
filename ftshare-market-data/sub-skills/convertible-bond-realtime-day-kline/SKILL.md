---
name: convertible-bond-realtime-day-kline
description: 查询单只或批量可转债当前交易日实时日 K 线（GET /api/v4/market/data/convertible-bond-realtime-day-kline）。用户问可转债实时日 K、当下转债开高低收、多只可转债今日行情时使用。必填 --symbols，按空格分隔，1～20 只。
---

# 可转债实时日K线

查询单只或批量可转债当前交易日实时日 K 线。必填 `--symbols`，按空格分隔，1～20 只。

外部接口：`GET /api/v4/market/data/convertible-bond-realtime-day-kline`。

| 项目 | 说明 |
|------|------|
| 输入参数 | `symbols`（必填）：JSON 字符串数组，例如 `["113042.SH","123107.SZ"]`；单只也必须是单元素数组 |
| 响应结构 | `code` / `message` / `data`；`data` 为分组数组，每项含 `symbol`、`items`、`total` |
| 每根 K 线字段 | open / high / low / close / ts_millis / ts_millis_open / turnover / volume |
| 单次限量 | 无分页；1～20 个标的 |

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> convertible-bond-realtime-day-kline --symbols 113042.SH 123107.SZ
```

## 注意事项

- 仅接受可转债标的，支持 `.SH` / `.XSHG`、`.SZ` / `.XSHE` 后缀；代码可被解析不代表属于接口支持的证券类别。
- 自动选择交易日：北京时间交易日 09:00 起选择当日，09:00 前及非交易日选择上一交易日，实际返回以行情可用性为准。
- 不提供 `symbol`、日期范围、`interval_unit`、`interval_value`、`adjust_kind`、`limit` 或分页参数；不能通过本接口指定历史日期。
- 每个有数据的标的返回 1 条实时日 K；盘中 OHLC、成交量和成交额会继续变化，不应当作盘中已确定的最终收盘数据。
- 无可用行情时仍返回对应标的分组，`items` 为 `[]`、`total` 为 0；停牌可能导致不返回 K 线。
- 时间戳单位为毫秒；价格与成交额在 JSON 中为字符串，不是 number。响应中的 symbol 使用 `.SH`/`.SZ` 短后缀。
- 历史日 K 请使用 `convertible-bond-candlesticks`，历史分钟 K 请使用 `convertible-bond-minutes`。