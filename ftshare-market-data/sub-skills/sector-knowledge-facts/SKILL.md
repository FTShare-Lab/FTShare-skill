---
name: sector-knowledge-facts
description: "检索板块事实。当用户想了解某个板块的行业供需、公司事件、产业政策等事实性信息，或按关键词、分类、发布日期、影响力筛选板块事实时使用。Use when user asks about 板块事实、板块消息面、板块舆情、sector facts."
---

# 板块事实检索

接口：`GET /api/v3/market/data/sector-knowledge/facts`。

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 板块事实检索 |
| 外部接口 | `/api/v3/market/data/sector-knowledge/facts` |
| 请求方式 | GET |
| 适用场景 | 按板块、分类、发布时间、影响力、可靠性等条件检索板块事实，分页返回 |
| 数据范围 | 已发布的板块事实，原始发布时间 20150401 起 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|---|---|---|---|---|
| `sector_name` | string | 否 | 板块标准名称，精确匹配 | `A股半导体` |
| `sector_type` | string | 否 | 板块类型：`industry`、`concept`、`region`、`index_style`、`macro_asset` | `industry` |
| `market` | string | 否 | 市场：`CN`、`US`、`HK`、`KR`、`JP`、`global` | `CN` |
| `keyword` | string | 否 | 关键词子串匹配 `title`、`content`，最长 200 字符；与 `keyword_expression` 互斥 | `存储` |
| `keyword_expression` | string | 否 | 布尔表达式，支持 `AND`、`OR`、括号；与 `keyword` 互斥 | `2026 AND (营收 OR 产能)` |
| `fact_category` | string | 否 | 板块事实分类，可重复传入；同维度多值为 OR | `行业供需` |
| `start_date` | string | 否 | 原始发布日期下界，`YYYYMMDD` | `20260101` |
| `end_date` | string | 否 | 原始发布日期上界，`YYYYMMDD` | `20261123` |
| `min_influence_score` | integer | 否 | 最低影响力，0–100 | `60` |
| `min_reliability_score` | integer | 否 | 最低可靠性，0–100 | `60` |
| `sort` | string | 否 | `relevance`、`latest`、`influence`；默认 `relevance` | `latest` |
| `page` | integer | 否 | 页码，默认 1，最大 1000 | `1` |
| `page_size` | integer | 否 | 每页条数，默认 50，最大 200 | `50` |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 按板块 + 分类 + 日期范围检索
python <RUN_PY> sector-knowledge-facts --sector-name A股半导体 --fact-category 行业供需 --start-date 20260101 --end-date 20261123 --sort latest

# 关键词检索（必须同时提供 --sector-name）
python <RUN_PY> sector-knowledge-facts --sector-name A股半导体 --keyword 存储 --page 1 --page-size 50

# 布尔表达式检索
python <RUN_PY> sector-knowledge-facts --sector-name A股半导体 --keyword-expression "2026 AND (营收 OR 产能)"

# 多分类（同维度 OR）并限制影响力
python <RUN_PY> sector-knowledge-facts --sector-name A股半导体 --fact-category 行业供需 --fact-category 公司事件 --min-influence-score 60

# 自动翻页获取全量数据
python <RUN_PY> sector-knowledge-facts --sector-name A股半导体 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

`data` 为分页对象，`records` 为当前页板块事实列表：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "pageNum": 1,
        "pageSize": 50,
        "total": 120,
        "pages": 3,
        "records": [
            {
                "sector_name": "A股半导体",
                "sector_type": "industry",
                "market": "CN",
                "title": "AI服务器与HBM挤占存储及成熟制程产能",
                "content": "……",
                "url": null,
                "published_date": "20261118",
                "fact_category": "行业供需",
                "fact_tags": [],
                "reliability_score": 100,
                "influence_score": 90
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
| `title` | string | 否 | 板块事实标题 |
| `content` | string | 是 | 板块事实摘要 |
| `url` | string | 是 | 原始来源链接；非 `http(s)://` 形态时为 `null` |
| `published_date` | string | 是 | 原始发布日期，`YYYYMMDD` |
| `fact_category` | string | 是 | 板块事实分类 |
| `fact_tags` | array | 否 | 板块事实标签；无标签时为 `[]` |
| `reliability_score` | integer | 是 | 可靠性，0–100 |
| `influence_score` | integer | 是 | 影响力，0–100 |

## 注意事项

- 首次检索前先调用 `sector-knowledge-search-options` 获取 `fact_category`、`sort` 的合法取值。
- 板块名用 `sector-knowledge-sectors` 获取，`sector_name` 为精确匹配。
- 关键词只匹配 `title` 和 `content`，为子串匹配；`keyword` 与 `keyword_expression` 不能同时传。
- 使用 `keyword` 或 `keyword_expression` 时必须提供 `sector_name`，仅给类型、市场、日期或评分不满足。
- 含空格或括号的表达式需做 URL 编码（handler 已自动处理）。
- `sort=relevance` 时标题命中词项的结果优先，其次按影响力排序；未传关键词时等同于 `influence`。
- `start_date` / `end_date` 按自然日闭区间过滤；`published_date` 可能为空，按日期过滤时不包含空值。
- 至少提供一个检索条件。