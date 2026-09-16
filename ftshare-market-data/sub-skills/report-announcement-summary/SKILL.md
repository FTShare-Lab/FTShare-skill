---
name: report-announcement-summary
description: 根据公告 ID 查询单条报告公告的摘要、标题、证券信息和处理状态。用户提到「报告公告摘要」「公告摘要」「单条公告详情」「report announcement summary」时使用。未找到公告时 data 为 null、code 为 404。
---

# 查询报告公告摘要

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询报告公告摘要 |
| 外部接口 | GET /api/v2/market/data/report-announcements/summary |
| 请求方式 | GET |
| 适用场景 | 根据公告 ID 查询单条报告公告的摘要、标题、证券信息和处理状态 |

> 同一处理逻辑的兼容入口还包括 `/api/v1/market/data/report-announcement/summary`。

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| announcement_id | string | 是 | 公告 ID | `AN202607140001` | 由「报告公告列表」接口返回 |

## 执行方式

```bash
python <RUN_PY> report-announcement-summary --announcement_id AN202607140001
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

返回 `code/message/data`，未找到公告时 `code` 为 404、`data` 为 `null`。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "announcement_id": "AN202607140001",
    "sec_code": "600000",
    "sec_name": "浦发银行",
    "announcement_title": "公告标题",
    "summary": "公告摘要",
    "status": "summarized",
    "announcement_time": "2026-07-14 09:30:00"
  }
}
```

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| announcement_id | string/null | 公告 ID |
| sec_code / sec_name | string/null | 证券代码 / 证券名称 |
| announcement_title | string/null | 公告标题 |
| summary | string/null | 公告摘要 |
| status | string/null | 摘要处理状态 |
| announcement_time | string/null | 公告时间 |

## 注意事项

- `announcement_id` 为必填，由「报告公告列表」接口返回。
- 未找到公告时 `code` 为 404、`data` 为 `null`。
- 两个路径（`/report-announcements/summary` 与 `/report-announcement/summary`）是同一处理逻辑的兼容入口。
