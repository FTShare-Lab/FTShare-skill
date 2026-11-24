---
name: sector-knowledge-search-options
description: "查询板块知识检索选项。当用户准备检索板块事实或板块洞察，需要先确认分类、板块类型、市场与排序的合法取值时使用。Use when user asks about 板块知识分类取值、板块检索枚举、sector knowledge options."
---

# 板块知识检索选项

接口：`GET /api/v3/market/data/sector-knowledge/search-options`。

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 板块知识检索选项 |
| 外部接口 | `/api/v3/market/data/sector-knowledge/search-options` |
| 请求方式 | GET |
| 适用场景 | 返回板块事实与板块洞察的受控分类、关键词匹配方式，以及板块类型、市场与排序方式 |
| 数据范围 | 静态枚举，无时间维度 |

## 请求参数

无。

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> sector-knowledge-search-options
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

`data` 为检索选项对象：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "fact": {
            "category_list": [
                {"value": "行业供需", "label": "行业供需"}
            ],
            "searchable_field_list": ["title", "content"],
            "keyword_match": "substring"
        },
        "insight": {
            "category_list": [
                {"value": "产业景气研判", "label": "产业景气研判"}
            ],
            "searchable_field_list": ["title", "summary"],
            "keyword_match": "substring"
        },
        "sector_type_list": ["industry", "concept", "region", "index_style", "macro_asset"],
        "market_list": ["CN", "US", "HK", "KR", "JP", "global"],
        "sort": {
            "fact": ["relevance", "latest", "influence"],
            "insight": ["relevance", "latest", "influence", "confidence"]
        }
    }
}
```

### data 字段说明

| 字段名 | 类型 | 说明 |
|---|---|---|
| `fact` | object | 板块事实检索选项 |
| `insight` | object | 板块洞察检索选项 |
| `sector_type_list` | array | 板块类型允许值 |
| `market_list` | array | 市场允许值 |
| `sort` | object | 排序允许值，按资源分组 |

### fact / insight 字段说明

| 字段名 | 类型 | 说明 |
|---|---|---|
| `category_list` | array | 分类列表，元素为 `{value, label}` |
| `searchable_field_list` | array | 关键词匹配字段；`fact` 固定为 `title`、`content`，`insight` 固定为 `title`、`summary` |
| `keyword_match` | string | 关键词匹配方式，固定为 `substring` |

### sort 字段说明

| 字段名 | 类型 | 说明 |
|---|---|---|
| `fact` | array | 板块事实排序允许值：`relevance`、`latest`、`influence` |
| `insight` | array | 板块洞察排序允许值：`relevance`、`latest`、`influence`、`confidence` |

## 注意事项

- 首次检索前先调用本接口，获取分类、板块类型、市场与排序的合法取值。
- 再调用 `sector-knowledge-sectors` 获取板块标准名称。
- 最后调用 `sector-knowledge-facts` 或 `sector-knowledge-insights`，检索时使用本接口返回的取值。
- 关键词匹配方式为子串匹配，不提供全文检索模式。