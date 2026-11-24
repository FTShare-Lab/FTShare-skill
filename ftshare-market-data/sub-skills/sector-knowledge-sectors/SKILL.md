---
name: sector-knowledge-sectors
description: "查询板块描述列表。当用户需要确认板块标准名称、板块类型、所属市场，或按名称关键词查找板块时使用。Use when user asks about 板块列表、板块标准名、板块描述、sector list."
---

# 板块描述列表

接口：`GET /api/v3/market/data/sector-knowledge/sectors`。

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 板块描述列表 |
| 外部接口 | `/api/v3/market/data/sector-knowledge/sectors` |
| 请求方式 | GET |
| 适用场景 | 返回板块标准名称、类型、市场与描述，支持按市场、板块类型和名称关键词筛选 |
| 数据范围 | 板块列表快照，无时间维度 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|---|---|---|---|---|
| `market` | string | 否 | 市场过滤：`CN`、`US`、`HK`、`KR`、`JP`、`global` | `CN` |
| `sector_type` | string | 否 | 板块类型过滤：`industry`、`concept`、`region`、`index_style`、`macro_asset` | `industry` |
| `name_keyword` | string | 否 | 板块标准名或别名关键词，最多返回 10 个候选，最长 100 字符 | `半导体` |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 按市场 + 名称关键词查找板块
python <RUN_PY> sector-knowledge-sectors --market CN --name-keyword 半导体

# 按板块类型筛选
python <RUN_PY> sector-knowledge-sectors --sector-type industry --market CN

# 全部板块（无过滤）
python <RUN_PY> sector-knowledge-sectors
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

`data` 为板块数组，不分页：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "sector_name": "A股半导体",
            "sector_type": "industry",
            "market": "CN",
            "description": "A股半导体行业板块，涵盖芯片设计、制造、封测、设备、材料等全产业链上市公司。"
        }
    ]
}
```

### data 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `sector_name` | string | 否 | 板块标准名称，全局唯一 |
| `sector_type` | string | 否 | 板块类型：`industry`、`concept`、`region`、`index_style`、`macro_asset` |
| `market` | string | 否 | 市场：`CN`、`US`、`HK`、`KR`、`JP`、`global` |
| `description` | string | 是 | 板块描述；无描述时为 `null` |

## 注意事项

- 先调用 `sector-knowledge-search-options` 获取板块类型与市场的合法取值。
- 本接口返回的 `sector_name` 可直接作为 `sector-knowledge-facts`、`sector-knowledge-insights` 的 `sector_name`，为精确匹配。
- `name_keyword` 按标准名或别名查找候选，最多返回 10 个；不分页，返回当前查询匹配的完整板块列表。