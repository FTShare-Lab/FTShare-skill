---
name: index-weight-summary
description: 分页查询指数权重汇总（market.ft.tech）。可按 index_code 查询指定指数各期权重的 date 与 url_hash。用户问指数权重汇总、成分股权重期数、权重文件 url_hash、沪深300 权重日期、有哪些指数权重数据时使用。下游：取到 url_hash 后可调 index-weight-download 下载 xlsx；取到 index_code/date 后可调 index-weight-list 查成份明细。
---

# 分页查询指数权重汇总（index-weight-summary）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 分页查询指数权重汇总 |
| 外部接口 | `/api/v1/market/data/index/index_weight_summary` |
| 请求方式 | GET |
| 适用场景 | 按指数汇总各期权重数据的 `date` 与 `url_hash`；可用 `index_code` 定位单个指数，便于再调用「下载指数权重文件」获取具体权重表 |

## 2. 请求参数

说明：使用查询参数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| index_code | string | 否 | 指数代码 | 000300 | 不传则分页返回全部指数 |
| page | int | 否 | 页码 | 1 | 默认 1 |
| page_size | int | 否 | 每页条数 | 20 | 默认 20，最大 100 |

## 3. 响应说明

返回值为分页列表对象 **`IndexWeightSummaryListResponse`**。

### IndexWeightSummaryListResponse 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| total | int | 否 | 总条数（按指数汇总的记录数） | - |
| page | int | 否 | 当前页码 | - |
| page_size | int | 否 | 每页条数 | - |
| index_weights | array | 否 | 单只指数的期数汇总列表 | - |

### IndexWeightSummary 结构（index_weights 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| index_code | String | 否 | 指数代码 | - |
| periods | array | 否 | 该指数各期的日期与下载用 url_hash | - |

### IndexWeightPeriod 结构（periods 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| date | String | 否 | 权重日期；文档示例为 `YYYYMMDD`，线上也可能为 `YYYY-MM-DD`，以实际返回为准 | - |
| url_hash | String | 否 | 该期权重文件的哈希 | - |

## 4. 调用方式

本 handler 与上级 `FTShare-index-data/run.py` 配合使用：

```bash
python <RUN_PY> index-weight-summary --index-code 000300 --page 1 --page-size 20
python <RUN_PY> index-weight-summary --page 1 --page-size 20
```

其中 `<RUN_PY>` 为 `FTShare-index-data/run.py` 的绝对路径。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --page 1 --page-size 20
python scripts/handler.py --index-code 000300 --page 1 --page-size 20
```

（需在 `sub-skills/index-weight-summary` 目录下执行，或传入脚本完整路径。）

## 5. 链路说明

本接口为**权重链第 1 步**。  
- 取到 `index_code` + `date` → 可调 `index-weight-list --index_code <code> --date <date>` 查成份明细。  
- 取到 `url_hash` → 可调 `index-weight-download --url-hash <url_hash>` 直接下载整期 xlsx。

## 6. 请求示例

```
GET /api/v1/market/data/index/index_weight_summary?index_code=000300&page=1&page_size=20
```
