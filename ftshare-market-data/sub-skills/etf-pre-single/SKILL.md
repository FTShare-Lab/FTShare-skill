---
name: etf-pre-single
description: 查询单只 ETF 盘前数据。用户问某只 ETF 盘前、申购赎回单位、净值、现金差额、IOPV、510300 盘前时使用。
---

# 查询单只 ETF 盘前数据

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询单只 ETF 盘前数据 |
| 外部接口 | `GET /api/v1/market/data/etf-pre-single` |
| 请求方式 | GET |
| 适用场景 | 根据标的代码查询单只 ETF 的盘前信息（申购赎回单位、净值、现金差额等）；不传 date 时使用当日（CST）；未找到或报错时接口返回相应错误信息 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | ETF 标的代码，带交易所后缀 | 510300.XSHG、159915.XSHE | - |
| date | int | 否 | 交易日 | 20260316 | YYYYMMDD；不传则使用当日（CST） |

## 3. 响应说明

返回单条 ETF 盘前信息，结构与全量接口 `etf-pre-data` 的 `items` 中单条一致。

### EtfPreItem 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| etf_symbol_id | int | 否 | ETF 代码 | - |
| etf_market_id | int | 否 | ETF 交易所编号 | - |
| creation_redemption_unit | long | 是 | 最小申购、赎回单位 | 份 |
| max_cash_ratio | float | 是 | 现金替代比例上限 | - |
| publish_ipov | int | 否 | 是否需要公布 IOPV：1=需要公布 | - |
| creation_redemption_flag | int | 否 | 申购赎回允许情况：1=允许申购 2=允许赎回，通过 & 判断 | - |
| record_num | int | 是 | 成分股数量 | - |
| estimate_cash_component | float | 是 | 最小申购、赎回单位的预估现金部分 | 元 |
| trade_date | int | 是 | 交易日 | YYYYMMDD |
| cash_component | float | 是 | 现金差额 | 元 |
| nav_per_cu | float | 是 | 最小申购、赎回单位净值 | 元 |
| nav | float | 是 | 基金份额净值 | 元 |
| member_market_type | int | 否 | 成分股类型位掩码：1=上交所 2=深交所 4=港交所 8=北交所 16=外汇 32=其他 | - |

### 响应示例

```json
{
  "etf_symbol_id": 510300,
  "etf_market_id": 1,
  "creation_redemption_unit": 1000000,
  "max_cash_ratio": 0.15,
  "publish_ipov": 1,
  "creation_redemption_flag": 3,
  "record_num": 301,
  "estimate_cash_component": 12345.67,
  "trade_date": 20260316,
  "cash_component": 0.0,
  "nav_per_cu": 3.8921,
  "nav": 3.8921,
  "member_market_type": 1
}
```

## 4. 用法

通过主目录 `run.py` 调用（必填 `--symbol`，可选 `--date`）：

```bash
# 当日盘前（CST）
python <RUN_PY> etf-pre-single --symbol 510300.XSHG

# 指定交易日
python <RUN_PY> etf-pre-single --symbol 510300.XSHG --date 20260316
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON；接口报错或未找到时，将接口返回的错误信息原样输出到 stderr 并退出码 1。

## 5. 请求示例

当日：

```
GET /api/v1/market/data/etf-pre-single?symbol=510300.XSHG
```

指定日期：

```
GET /api/v1/market/data/etf-pre-single?symbol=510300.XSHG&date=20260316
```

## 6. 数据更新时间与注意事项

- 数据更新时间以接口/数据源为准；不传 `date` 时使用当日（CST）交易日。
- 净值、现金差额等金额类字段以接口返回为准；展示时注意单位（元、份）。
- `creation_redemption_flag` 为位掩码：1=允许申购，2=允许赎回，3 表示申购与赎回均允许。
- **时段**：盘前数据在**交易日盘前时段**更易返回成功；非盘前、周末、节假日或当日数据尚未就绪时，接口可能返回系统错误或空数据，**属服务端行为而非脚本故障**。
