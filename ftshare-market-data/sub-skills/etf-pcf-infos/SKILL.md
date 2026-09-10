---
name: etf-pcf-infos
description: 查询 ETF 申赎清单（PCF 汇总信息，etf_pcf_infos）。用户问 ETF 申赎清单、PCF 汇总、申购赎回单位、现金替代金额、预估现金差额、成分证券数量、ETF PCF 信息时使用。
---

# ETF 申赎清单（PCF 汇总信息）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | ETF 申赎清单（etf_pcf_infos） |
| 外部接口 | `GET /api/v2/market/data/etf-pcf/etf-pcf-infos` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 查询 ETF 的 PCF（申购赎回清单）汇总信息：申购赎回单位、现金替代金额、预估现金差额、现金替代比例上限、成分证券数量 |

支持三种查询模式：

1. **单标的单日**：同时传 `symbol` + `trade_date`，`data` 直接返回一条 PCF 信息对象。
2. **全市场单日**：只传 `trade_date`，`data` 返回分页对象。
3. **单标的区间**：同时传 `symbol` + `start_date` + `end_date`，`data` 返回分页对象（区间最长 30 个日历日）。

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 视模式 | ETF 代码 | 510300.SH | 支持短/长市场后缀（`510300.XSHG`） |
| trade_date | int | 视模式 | 交易日 | 20260909 | YYYYMMDD；与日期区间参数互斥 |
| start_date | int | 视模式 | 区间开始日期 | 20260901 | 须与 `end_date`、`symbol` 同时提供 |
| end_date | int | 视模式 | 区间结束日期 | 20260909 | 须与 `start_date`、`symbol` 同时提供 |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1；分页查询有效 |
| page_size | int | 否 | 每页条数 | 50 | 默认 50，最大 500；分页查询有效 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 在单标的单日模式下为对象，分页模式下为分页对象（`pageNum`/`pageSize`/`total`/`pages`/`records`）。

PCF 信息字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | ETF 代码（短市场后缀） |
| trade_date | int | 交易日 YYYYMMDD |
| creation_redemption_unit | int / null | 申购赎回单位（份） |
| cash_substitution | string / null | 现金替代金额 |
| estimated_cash | string / null | 预估现金差额 |
| iopv | string / null | 基金份额参考净值；当前为 `null`（保留字段） |
| min_creation_unit | int / null | 最小申购单位（份） |
| max_cash_ratio | string / null | 现金替代比例上限 |
| component_count | int / null | 成分证券数量 |

## 4. 调用方式

```bash
python <RUN_PY> etf-pcf-infos --symbol 510300.SH --trade-date 20260909
python <RUN_PY> etf-pcf-infos --trade-date 20260909 --page 1 --page-size 5
python <RUN_PY> etf-pcf-infos --symbol 510300.SH --start-date 20260901 --end-date 20260909 --page 1 --page-size 5
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `trade_date` 不能与 `start_date`、`end_date` 同时使用（handler 会在本地校验并拒绝）。
- `start_date` 必须早于 `end_date`，区间最长 30 个日历日。
- 单标的单日查询未命中数据时，仍返回对应标的和日期，其余业务字段为 `null`。
- `iopv` 为保留字段，当前返回 `null`。
- 金额和比例字段以字符串形式返回，以保留小数精度。
- 需要指定日期的 PCF 文件清单（XML 文件名）请使用 `etf-pcfs` 子 skill；本接口返回的是汇总指标。
