---
name: convertible-bond-realtime-minute-kline
description: 查询单只或批量可转债当前交易日实时 1 分钟 K 线（GET /api/v4/market/data/convertible-bond-realtime-minute-kline）。用户问可转债实时分钟行情、当下转债分钟走势、多只可转债盘中分钟 K 线时使用。必填 --symbols，按空格分隔，1～20 只。
---

# 可转债实时分钟K线

查询单只或批量可转债当前交易日实时 1 分钟 K 线。必填 `--symbols`，按空格分隔，1～20 只。

外部接口：`GET /api/v4/market/data/convertible-bond-realtime-minute-kline`。

| 项目 | 说明 |
|------|------|
| 输入参数 | `symbols`（必填）：JSON 字符串数组，例如 `["113042.SH","123107.SZ"]`；单只也必须是单元素数组 |
| 响应结构 | `code` / `message` / `data`；`data` 为分组数组，每项含 `symbol`、`items`、`total` |
| 每根 K 线字段 | open / high / low / close / ts_millis / ts_millis_open / turnover / volume |
| 单次限量 | 无分页；1～20 个标的 |

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> convertible-bond-realtime-minute-kline --symbols 113042.SH 123107.SZ
```

## 注意事项

- 仅接受可转债标的，支持 `.SH` / `.XSHG`、`.SZ` / `.XSHE` 后缀；代码可被解析不代表属于接口支持的证券类别。
- 自动选择交易日：北京时间交易日 09:00 起选择当日，09:00 前及非交易日选择上一交易日，实际返回以行情可用性为准。
- 不提供 `symbol`、日期范围、`interval_unit`、`interval_value`、`adjust_kind`、`limit` 或分页参数；不能通过本接口指定历史日期。
- 固定 1 分钟周期；结果按时间升序返回，可包含 09:30 记录，不应硬编码每日必须为 240 条。
- 无可用行情时仍返回对应标的分组，`items` 为 `[]`、`total` 为 0；停牌可能导致不返回 K 线。
- 时间戳单位为毫秒；价格与成交额在 JSON 中为字符串，不是 number。响应中的 symbol 使用 `.SH`/`.SZ` 短后缀。
- `total` 是 `items` 条数，不是分页总量。本接口不提供历史翻页，历史区间请使用 `convertible-bond-minutes`。