---
name: index-description-all
description: 查询全部指数基础信息（market.ft.tech）。用户问全部指数列表、指数简称全称、指数 PB/PE TTM、支持的指数清单、有哪些指数时使用。
---

# 指数 - 查询全部指数基础信息

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询全部指数基础信息 |
| 外部接口 | `GET /api/v1/market/data/index-description-all` |
| 请求方式 | GET |
| 适用场景 | 获取当前服务支持的 A 股相关指数列表及简称、全称、市净率、市盈率（TTM）等基础信息 |

## 2. 请求参数

说明：该接口无需请求参数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| - | - | - | 无需参数 | - | - |

## 3. 响应说明

返回值为指数基础信息数组。

```json
[
  {
    "symbol": "000001.XSHG",
    "full_name": "上证综合指数",
    "name": "上证指数",
    "pb": 1.5234,
    "pe_ttm": 16.5903
  }
]
```

### IndexDescriptionItem 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| symbol | string | 否 | 指数代码，一般为六位代码加交易所后缀（如 `000001.XSHG`、`399001.XSHE`、`899050.BJSE`） | - |
| full_name | string | 否 | 指数全称 | - |
| name | string | 否 | 指数简称 | - |
| pb | float | 是 | 市净率（LF），无数据时为 null | - |
| pe_ttm | float | 是 | 市盈率（TTM），无数据时为 null | - |

## 4. 用法

通过主目录 `run.py` 调用（无参数）：

```bash
python <RUN_PY> index-description-all
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON；请求头已内置 `X-Client-Name: ft-claw`。

## 5. 请求示例

```
GET /api/v1/market/data/index-description-all
```

## 6. 注意事项

- 响应为数组；字段 `pb`、`pe_ttm` 可能为 `null`。
- 数据更新时间以服务端为准。
