---
name: sector-knowledge-insights
description: "检索板块洞察。当用户想了解某个板块的景气研判、政策影响、资金轮动、产业链传导、风险预警等分析结论，或按置信度、影响力筛选板块洞察时使用。Use when user asks about 板块洞察、板块研判、板块观点、sector insights."
---

# 板块洞察检索

接口：`GET /api/v3/market/data/sector-knowledge/insights`。

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 板块洞察检索 |
| 外部接口 | `/api/v3/market/data/sector-knowledge/insights` |
| 请求方式 | GET |
| 适用场景 | 按板块、分类、生成时间、影响力、置信度等条件检索板块洞察，分页返回 |
| 数据范围 | 已发布的板块洞察，生成时间 20260806 起 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|---|---|---|---|---|
| `sector_name` | string | 否 | 板块标准名称，精确匹配 | `A股半导体` |
| `sector_type` | string | 否 | 板块类型：`industry`、`concept`、`region`、`index_style`、`macro_asset` | `industry` |
| `market` | string | 否 | 市场：`CN`、`US`、`HK`、`KR`、`JP`、`global` | `CN` |
| `keyword` | string | 否 | 关键词子串匹配 `title`、`summary`，最长 200 字符；与 `keyword_expression` 互斥 | `产能` |
| `keyword_expression` | string | 否 | 布尔表达式，支持 `AND`、`OR`、括号；与 `keyword` 互斥 | `2026 AND (产能 OR 库存)` |
| `insight_category` | string | 否 | 板块洞察分类，可重复传入；同维度多值为 OR | `产业景气研判` |
| `start_date` | string | 否 | 板块洞察生成日期下界，`YYYYMMDD` | `20260101` |
| `end_date` | string | 否 | 板块洞察生成日期上界，`YYYYMMDD` | `20261123` |
| `min_influence_score` | integer | 否 | 最低影响力，0–100 | `60` |
| `min_confidence` | number | 否 | 最低置信度，0–1 | `0.8` |
| `sort` | string | 否 | `relevance`、`latest`、`influence`、`confidence`；默认 `relevance` | `confidence` |
| `page` | integer | 否 | 页码，默认 1，最大 1000 | `1` |
| `page_size` | integer | 否 | 每页条数，默认 50，最大 200 | `50` |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 按板块 + 分类 + 置信度检索
python <RUN_PY> sector-knowledge-insights --sector-name A股半导体 --insight-category 产业景气研判 --min-confidence 0.8 --sort confidence

# 关键词检索（必须同时提供 --sector-name）
python <RUN_PY> sector-knowledge-insights --sector-name A股半导体 --keyword 产能

# 布尔表达式检索
python <RUN_PY> sector-knowledge-insights --sector-name A股半导体 --keyword-expression "2026 AND (产能 OR 库存)"

# 日期范围 + 影响力
python <RUN_PY> sector-knowledge-insights --sector-name A股半导体 --start-date 20260101 --end-date 20261123 --min-influence-score 60

# 自动翻页获取全量数据
python <RUN_PY> sector-knowledge-insights --sector-name A股半导体 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

`data` 为分页对象，`records` 为当前页板块洞察列表：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "pageNum": 1,
        "pageSize": 50,
        "total": 40,
        "pages": 1,
        "records": [
            {
                "sector_name": "A股半导体",
                "sector_type": "industry",
                "market": "CN",
                "title": "半导体设备端利润弹性远超营收",
                "summary": "……",
                "insight_category": "产业景气研判",
                "insight_tags": [],
                "confidence": 0.95,
                "influence_score": 75,
                "entity": [
                    {"name": "半导体设备", "role": "受益环节", "entity_type": "sector"}
                ],
                "created_date": "20260824",
                "updated_date": null
            }
        ]
    }
}
```

### records 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `sector_name` | string | 否 | 板块标准名称 |
| `sector_type` | string | 否 | 板块类型 |
| `market` | string | 否 | 市场 |
| `title` | string | 否 | 板块洞察标题 |
| `summary` | string | 否 | 板块洞察摘要 |
| `insight_category` | string | 是 | 板块洞察分类 |
| `insight_tags` | array | 否 | 板块洞察标签；无标签时为 `[]` |
| `confidence` | number | 否 | 置信度，0–1 |
| `influence_score` | integer | 是 | 影响力，0–100 |
| `entity` | array | 否 | 关联实体列表；无实体时为 `[]` |
| `created_date` | string | 否 | 板块洞察生成日期，`YYYYMMDD` |
| `updated_date` | string | 是 | 最后更新日期，`YYYYMMDD` |

### entity 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `name` | string | 否 | 实体名称 |
| `role` | string | 是 | 实体在本条板块洞察中的角色 |
| `entity_type` | string | 是 | 实体类型，如 `sector`、`company`、`product` |

## 注意事项

- 首次检索前先调用 `sector-knowledge-search-options` 获取 `insight_category`、`sort` 的合法取值。
- 板块名用 `sector-knowledge-sectors` 获取，`sector_name` 为精确匹配。
- 关键词只匹配 `title` 和 `summary`，为子串匹配；`keyword` 与 `keyword_expression` 不能同时传。
- 使用 `keyword` 或 `keyword_expression` 时必须提供 `sector_name`。
- 使用 `min_confidence` 时必须提供 `sector_name`；仅给类型、市场、日期或分类不满足。
- `sort=relevance` 时标题命中词项的结果优先，其次按影响力排序；未传关键词时等同于 `influence`。
- `start_date` / `end_date` 按自然日闭区间过滤板块洞察生成日期。
- 至少提供一个检索条件。