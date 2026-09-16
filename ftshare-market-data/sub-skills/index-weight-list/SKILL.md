---
name: index-weight-list
description: 分页查询指数成份权重明细（market.ft.tech）。必填 index_code；可选 date、分页。每条含成份代码、名称、权重及该期 url_hash。用户问指数成份权重、沪深300 权重列表、某期指数权重明细、指数成份股占比时使用。前置：可先用 index-weight-summary 确认有哪些期数/日期。下游：取到 url_hash 后可调 index-weight-download 下载 xlsx。
---

# 分页查询指数权重列表（index-weight-list）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 分页查询指数权重列表 |
| 外部接口 | `/api/v1/market/data/index/index_weight` |
| 请求方式 | GET |
| 适用场景 | 按指数代码（及可选日期）分页查询成份权重明细；每条记录含成份代码、名称、权重比例及该期文件 `url_hash` |

## 2. 请求参数

说明：使用查询参数。服务端校验 `index_code` 非空，否则返回错误。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| index_code | string | 是 | 指数代码 | 000300 | 不能为空或仅空白 |
| date | string | 否 | 查询日期，格式 `YYYYMMDD` | 20250320 | 不传则由上游默认行为决定 |
| page | int | 否 | 页码 | 1 | 默认 1 |
| page_size | int | 否 | 每页条数 | 20 | 默认 20，最大 100 |

## 3. 响应说明

返回值为分页列表对象 **`IndexWeightListResponse`**。

### IndexWeightListResponse 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| total | int | 否 | 总条数 | - |
| page | int | 否 | 当前页码 | - |
| page_size | int | 否 | 每页条数 | - |
| index_weights | array | 否 | 权重明细列表 | - |

### IndexWeightInfo 结构（index_weights 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| date | String | 否 | 权重日期，`YYYYMMDD`（线上也可能为其他日期字符串格式，以实际为准） | - |
| index_code | String | 否 | 指数代码 | - |
| component_code | String | 否 | 成份证券代码 | - |
| component_name | String | 否 | 成份证券名称 | - |
| weight | String | 否 | 权重（字符串形式，与上游一致） | - |
| url_hash | String | 否 | 该期完整权重表文件的哈希，可用于下载 xlsx | - |

## 4. 调用方式

本 handler 与上级 `FTShare-index-data/run.py` 配合使用：

```bash
python <RUN_PY> index-weight-list --index-code 000300 --date 20250320 --page 1 --page-size 20
python <RUN_PY> index-weight-list --index-code 000300 --page 1 --page-size 20
```

其中 `<RUN_PY>` 为 `FTShare-index-data/run.py` 的绝对路径。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --index-code 000300 --date 20250320 --page 1 --page-size 20
```

（需在 `sub-skills/index-weight-list` 目录下执行，或传入脚本完整路径。）

## 5. 链路说明

本接口为**权重链第 2 步**。  
- **前置**：`index-weight-summary` → 取得 `index_code` 与可用 `date`。  
- **下游**：返回的 `url_hash` → `index-weight-download --url-hash <url_hash>` 下载整期 xlsx。

### 名称→代码映射

`--index-code` 只接受**纯 6 位指数代码**（如 `000300`），不接受中文名称。  
若用户给出中文名称（如"沪深300"），须先映射：

1. 调用 `index-description-paginated --page 1 --page-size 100` → 在 `index_descriptions` 中按 `index_name` 模糊匹配 → 取得 `index_code`。  
2. 或调用 `index-description-all` → 从 `symbol`（如 `000300.XSHG`）截取前 6 位。

## 6. 请求示例

```
GET /api/v1/market/data/index/index_weight?index_code=000300&date=20250320&page=1&page_size=20
```
