---
name: major-contract-by-symbol
description: 按股票代码查询重大合同历史（market.ft.tech）。用户问某股票的重大合同、某公司签了哪些大单、合同金额时使用。
---

# 重大合同 - 按股票代码查询

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 按股票代码查询重大合同 |
| 外部接口 | `GET /api/v1/market/data/corporate/contract/by-symbol` |
| 请求方式 | GET |
| 适用场景 | 查询指定股票的所有重大合同信息，按公告日期降序排列，支持分页 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 股票代码 | `300500` | 6 位代码 |
| page | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| page_size | int | 否 | 每页数量 | `50` | 默认 50，最大 200 |

## 3. 响应说明

返回 `PaginatedApiResponse` 包装的 JSON 对象。`data.records` 元素结构与 [major-contract-by-date](major-contract-by-date) 的 `items` 一致。

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> major-contract-by-symbol --symbol 300500
python <RUN_PY> major-contract-by-symbol --symbol 601668 --page 1 --page_size 50
```

## 5. 请求示例

```
GET /api/v1/market/data/corporate/contract/by-symbol?symbol=300500&page=1&page_size=50
```
