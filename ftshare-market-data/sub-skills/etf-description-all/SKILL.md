---
name: etf-description-all
description: 查询全部 ETF 基础信息（market.ft.tech）。用户问 ETF 列表、全部 ETF、ETF 代码与名称映射、按名称找 ETF 代码时使用。
---

# ETF-查询全部ETF基础信息

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询全部ETF基础信息 |
| 外部接口 | `/api/v2/market/data/etf-description-all` |
| 请求方式 | GET |
| 适用场景 | 获取 ETF 列表（代码与名称）及部分基础属性信息，用于列表展示、筛选与检索 |

## 2. 请求参数

说明：该接口无需请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| - | - | - | 无需参数 | - | - |

## 3. 响应说明

返回值为 ETF 基础信息数组，数据模型如下：

```json
[
  EtfDescriptionItem
]
```

### EtfDescriptionItem 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| asset_class | String | 否 | 基金类型，当前外部返回小写字符串（如 `stock`、`bond`、`commodity`、`currency`） | - |
| custodian | String | 否 | 基金托管人（通常为托管银行） | - |
| float_shares | int | 是 | 流通份额，无数据时为 null | 份 |
| inception_date | String | 否 | 成立日期，格式 `YYYY-MM-DD` | - |
| management_company | String | 否 | 基金管理人 | - |
| name | String | 否 | ETF 名称 | - |
| symbol | String | 否 | ETF 标的代码，带交易所后缀 | - |

## 4. 用法

通过主目录 `run.py` 调用（无需参数）：

```bash
python <RUN_PY> etf-description-all
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON 数组，可直接用于“名称 -> symbol”映射。

## 5. 请求示例

```
GET /api/v1/market/data/etf-description-all
```

## 6. 响应示例

```json
[
  {
    "asset_class": "currency",
    "custodian": "交通银行",
    "float_shares": 3955933,
    "inception_date": "2013-03-29",
    "management_company": "易方达基金",
    "name": "货币ETF易方达",
    "symbol": "159001.XSHE"
  }
]
```

## 7. 数据更新时间与注意事项

- 数据更新时间以接口/数据源为准。
- 当用户只给 ETF 名称或简称时，建议先调用本接口做名称匹配，拿到唯一 `symbol` 后再调用 `etf-detail`、`etf-ohlcs`、`etf-prices`、`etf-components-all`、`etf-pre-single`。
- 若名称匹配到多个 `symbol`，先让用户确认目标标的，再继续查询指标。
