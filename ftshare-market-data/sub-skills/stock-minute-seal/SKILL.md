---
name: stock-minute-seal
description: "查询股票分钟封单金额。接口：GET /api/v2/market/data/stock-minute-seal。用户问个股某日的分钟封单金额、涨停或跌停封单的变化、封单金额时间序列时使用。同义：打板。"
---

# 股票分钟封单金额

接口：GET `/api/v2/market/data/stock-minute-seal`。参数和响应以 [《股票分钟封单金额》](https://market.ft.tech/gateway/doc/pages/flxy83s5.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 请求参数

| 参数 | 是否必填 | 说明 |
|---|---|---|
| `--trade-date` | 是 | 交易日期，八位 `YYYYMMDD`，如 `20260923`；仅支持单日查询，不接受 `YYYY-MM-DD` |
| `--symbol` | 否 | 股票代码，如 `600825.SH`、`000001.SZ`，也支持六位裸代码；不传时返回该日全部有封单记录的股票 |

## 响应说明

返回 `code`/`message`/`data` 信封，非分页（没有 `--all`）。`data` 字段：

| 字段 | 说明 |
|---|---|
| `trade_date` | 本次查询的交易日，格式 `YYYYMMDD` |
| `sampling` | 固定为 `last_accepted_quote_per_minute`，表示每分钟最后一条有效行情 |
| `stocks` | 按股票分组的分钟封单记录；无匹配数据时为空数组 |

`stocks[]`：`symbol`（六位裸代码，保留前导零，不带交易所后缀）、`market_id`（`3553` 沪市 / `3554` 深市）、`minutes`。

`minutes[]`：`minute`（北京时间 `HH:MM`）、`direction`（`up` 涨停封单 / `down` 跌停封单）、`seal_amount_yuan`（该分钟最后一条有效行情的封单金额）。

## 注意事项

- 金额单位为**元**，以十进制字符串返回，小数末尾的零可省略；不要按万元解读，也不要依赖固定小数位数。
- 每分钟取最后一条有效行情；无有效记录的分钟**不补零、不向前填充**，故分钟序列可能有缺口。
- 返回的股票代码始终为六位裸代码（市场由 `market_id` 标识），与传入的 `--symbol` 后缀形式无关。
- 股票按市场 ID、股票代码升序排列，每只股票的分钟记录按时间升序排列。
- 合法查询无匹配数据时返回 HTTP 200 且 `stocks` 为空数组，不以错误响应代替空结果。

## 调用示例

```bash
python <RUN_PY> stock-minute-seal --trade-date 20260923 --symbol 000560.SZ
python <RUN_PY> stock-minute-seal --trade-date 20260923
```
