---
name: index-description-paginated
description: 含指数代码（纯 6 位 `index_code`）、名称、简介及其他描述字段。用户问指数描述分页、指数简介列表、某只指数简介、有哪些指数描述时使用。也可作为名称→代码映射源：用户给出中文指数名称时，先调本接口按 `index_name` 匹配，取 `index_code` 供 `index-weight-list` 等接口使用。
---

# 分页查询指数描述列表（index-description-paginated）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 分页查询指数描述列表 |
| 外部接口 | `/api/v1/market/data/index/index_description` |
| 请求方式 | GET |
| 适用场景 | 分页获取 A 股相关指数描述信息，含指数代码、名称、简介及用于下载文件的 `url_hash` |

## 2. 请求参数

说明：使用查询参数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| page | int | 否 | 页码 | 1 | 默认 1 |
| page_size | int | 否 | 每页条数 | 20 | 默认 20，最大 100 |

## 3. 响应说明

返回值为分页列表对象 **`IndexDescriptionListResponse`**。

### IndexDescriptionListResponse 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| total | int | 否 | 总条数 | - |
| page | int | 否 | 当前页码 | - |
| page_size | int | 否 | 每页条数 | - |
| index_descriptions | array | 否 | 指数描述条目列表 | - |

### IndexDescriptionInfo 结构（index_descriptions 元素）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| index_code | String | 否 | 指数代码 | - |
| index_orig | String | 否 | 指数原始名称/简称类字段（与上游一致） | - |
| index_name | String | 否 | 指数名称 | - |
| index_intro | String | 否 | 指数简介 | - |
| url_hash | String | 否 | 对应描述文件的哈希，用于「下载指数描述文件」接口 | - |

## 4. 调用方式

本 handler 与上级 `FTShare-index-data/run.py` 配合使用：

```bash
python <RUN_PY> index-description-paginated --page 1 --page-size 20
```

其中 `<RUN_PY>` 为 `FTShare-index-data/run.py` 的绝对路径。

### 直接执行 handler（调试）

```bash
python scripts/handler.py --page 1 --page-size 20
```

（需在 `sub-skills/index-description-paginated` 目录下执行，或传入脚本完整路径。）

## 5. 链路说明

本接口返回的 `index_code`（纯 6 位，如 `000300`）与 `index_name` 可用于名称到代码映射。当其他接口（如 `index-weight-list`）需要 `index_code` 但用户只给了中文名称时：

1. 调用本接口 `--page 1 --page-size 100`
2. 在 `index_descriptions` 中按 `index_name` 模糊搜索用户给出的名称
3. 取匹配项的 `index_code` 传给目标接口

## 6. 请求示例

```
GET /api/v1/market/data/index/index_description?page=1&page_size=20
```
