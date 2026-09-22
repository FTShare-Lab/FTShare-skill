---
name: hk-candlesticks
description: 按港股代码查询日/月/季/年 K 线。用户问港股 K 线、日 K / 月 K / 季 K / 年 K、00700 历史行情、港股开高低收、OHLC、成交量成交额、前复权不复权港股时使用。必填 trade_code、interval_unit、until_date；可选 since_date、adjust_kind、limit。
---

# 查询港股 K 线（hk-candlesticks）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询港股 K 线 |
| 外部接口 | `/api/v2/market/data/hk/hk-candlesticks` |
| 请求方式 | GET |
| 适用场景 | 按港股代码查询日/月/季/年 K 线；请求与响应中的代码均为 **5 位数字 + `.HK`** |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_code | string | 是 | 港股代码 | 00700.HK | 支持 `700` 或 `00700.HK`，响应中统一为 5 位 + `.HK` |
| interval_unit | string | 是 | K 线间隔单位 | day | `day`/`month`/`quarter`/`year`（大小写不敏感）；**不支持 `week`** |
| until_date | string | 是 | 结束日期 | 2026-03-24 | 格式 `YYYY-MM-DD` |
| since_date | string | 否 | 开始日期 | 2026-01-01 | 不传则从库中最早数据起至 `until_date` |
| adjust_kind | string | 否 | 复权类型 | forward | 默认 `forward`（前复权）；`none` 为不复权；取值大小写不敏感 |
| interval_value | int | 否 | 间隔数值 | 1 | 当前仅支持 `1`，其它值会报错 |
| limit | int | 否 | 返回条数上限 | 100 | 日 K 在 SQL 层下推；月/季/年在聚合后截取最近 N 根 |

## 3. 响应说明

返回值为 **`HkCandlesticksResponse`**：`trade_code` + K 线数组 `items`。

### HkCandlesticksResponse 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| trade_code | String | 否 | 规范化后的港股代码（5 位 + `.HK`） | - |
| items | Array | 否 | K 线列表，按日期升序 | - |

### HkCandlestick 结构（items 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| open | String | 否 | 开盘价 | 元 |
| high | String | 否 | 最高价 | 元 |
| low | String | 否 | 最低价 | 元 |
| close | String | 否 | 收盘价 | 元 |
| date | String | 否 | 交易日 | `YYYY-MM-DD` |
| turnover | String | 否 | 成交额 | 元 |
| volume | int64 | 否 | 成交量 | 股 |

### 时区说明

`since_date` / `until_date` 及响应中的 `date` 均为 **港交所交易日历（UTC+8 / 东八区）** 日期。若 Agent 所在系统时区非东八区，计算「今天」等相对日期时应先转为东八区再传参。Handler 内置了东八区容错：若传入 ISO 8601 含时区的字符串，会自动转为东八区后截取日期部分。

## 4. 调用方式

本 handler 与上级 `FTShare-hk-data/run.py` 配合使用：

```bash
python <RUN_PY> hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24 --since-date 2026-03-01 --limit 20
python <RUN_PY> hk-candlesticks --trade-code 00700.HK --interval-unit month --until-date 2026-03-24 --limit 12
```

其中 `<RUN_PY>` 为 `FTShare-hk-data/run.py` 的绝对路径。

CLI 统一使用 **kebab-case** 长选项名：`--trade-code`、`--interval-unit`、`--until-date`、`--since-date`、`--adjust-kind`、`--interval-value`；查询串参数名仍为接口文档中的 snake_case。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --trade-code 00700.HK --interval-unit day --until-date 2026-03-24
```

（需在 `sub-skills/hk-candlesticks` 目录下执行，或传入脚本完整路径。）

## 5. 请求示例

```
GET /api/v2/market/data/hk/hk-candlesticks?trade_code=00700.HK&interval_unit=day&since_date=2026-03-01&until_date=2026-03-24&limit=20
```
