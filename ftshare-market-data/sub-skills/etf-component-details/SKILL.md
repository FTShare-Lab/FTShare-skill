---
name: etf-component-details
description: 查询 ETF 成分证券明细（etf_component_details）。用户问 ETF 成分股明细、申赎清单成分证券、成分数量、现金替代标志、必须/禁止现金替代、ETF PCF 成分明细时使用。
---

# ETF 成分证券明细

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | ETF 成分证券明细（etf_component_details） |
| 外部接口 | `GET /api/v2/market/data/etf-component-details` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 按 ETF 和交易日返回申赎清单中的全部成分证券及数量、成分类型、现金替代标志与替代金额 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | ETF 代码 | 510300.SH | 也支持 `159915.SZ` |
| trade_date | int | 否 | 交易日 | 20260908 | YYYYMMDD；不传时查询该 ETF 最新可用交易日 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为成分证券明细数组（无分页，一次返回全部）。

数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | ETF 代码 |
| trade_date | int | 实际返回的交易日 YYYYMMDD |
| component_code | string | 成分证券代码，带 `.SH`/`.SZ`/`.BJ`/`.HK` 后缀 |
| component_name | string | 成分证券名称 |
| component_type | string / null | `stock`/`bond`/`commodity`/`cash`；无法识别时为 `null` |
| quantity | int / null | 成分证券数量（股） |
| cash_substitution_flag | int / null | 现金替代原始编码 |
| cash_substitution_type | string / null | `prohibited`/`allowed`/`mandatory`/`refund` |
| creation_substitution_amount | number / null | 申购替代金额 |
| redemption_substitution_amount | number / null | 赎回替代金额 |
| general_substitution_amount | number / null | 通用替代金额 |

现金替代编码：`0`=prohibited（禁止现金替代）、`1`=allowed（允许）、`2/4/6/8`=mandatory（必须）、`3/5/7`=refund（退补）。

## 4. 调用方式

```bash
python <RUN_PY> etf-component-details --symbol 510300.SH
python <RUN_PY> etf-component-details --symbol 510300.SH --trade-date 20260908
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 数据范围 20250501 年至今。
- `trade_date` 为精确查询条件：该日期没有数据时成功返回空数组，不向前回退。
- 现金占位成分会保留，`component_type` 标记为 `cash`。
- 不同交易所的现金替代编码语义可能存在差异；需要精确区分时以 `cash_substitution_flag` 为准。
- 本接口不返回成分权重。
