---
name: report-announcement-list
description: 按公告日期分页查询报告公告列表，可选按证券代码过滤。用户提到「报告公告列表」「公告列表」「某日公告」「report announcement list」时使用。返回公告标题/附件信息/处理状态和公告 ID；公告 ID 可用于查询公告摘要。分页返回，page_size 最大 200，支持 --all 翻页。
---

# 查询报告公告列表

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询报告公告列表 |
| 外部接口 | GET /api/v1/market/data/report-announcements/list |
| 请求方式 | GET |
| 适用场景 | 按公告日期分页查询报告公告，可选按证券代码过滤；公告 ID 可用于查询公告摘要 |

> 同一处理逻辑的兼容入口还包括 `/api/v1/market/data/report-announcement/list`。

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| date | string | 是 | 公告日期 | `20260714` | YYYYMMDD 或 YYYY-MM-DD |
| sec_code | string | 否 | 证券代码 | `600000` | 不传返回当天全部证券公告 |
| page | int | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页数量 | `50` | 默认 50，最大 200 |

## 执行方式

```bash
# 某日某证券公告
python <RUN_PY> report-announcement-list --date 20260714 --sec_code 600000 --page 1 --page_size 20
# 某日全部公告并翻全量
python <RUN_PY> report-announcement-list --date 20260714 --all
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

返回 `code/message/data`，分页数据位于 `data.records`。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pageNum": 1, "pageSize": 20, "total": 50, "pages": 3,
    "records": [
      {
        "id": 12345,
        "announcement_id": "AN202607140001",
        "url_hash": "...",
        "sec_code": "600000",
        "sec_name": "浦发银行",
        "announcement_title": "...",
        "announcement_time": "2026-07-14 09:30:00",
        "adjunct_type": "PDF", "adjunct_size": 102400,
        "column_type": "monthly", "plate": "sh",
        "status": "summarized", "retry_count": 0,
        "created_at": "2026-07-14 09:30:00",
        "updated_at": "2026-07-14 10:00:00",
        "processed_at": "2026-07-14 10:01:00"
      }
    ]
  }
}
```

### data 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| pageNum | int | 当前页码 |
| pageSize | int | 当前每页条数 |
| total | int | 满足条件的总记录数 |
| pages | int | 总页数；无记录时为 0 |
| records | array | 当前页公告记录 |

### records 元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int64/null | 数据库记录 ID |
| announcement_id | string/null | 公告 ID |
| url_hash | string/null | 公告附件哈希 |
| sec_code / sec_name | string/null | 证券代码 / 证券名称 |
| announcement_title | string/null | 公告标题 |
| announcement_time | string/null | 公告时间 |
| adjunct_type | string/null | 附件类型 |
| adjunct_size | int64/null | 附件大小 |
| column_type | string/null | 公告栏目类型 |
| plate | string/null | 所属板块 |
| status | string/null | 处理状态 |
| retry_count | int64/null | 重试次数 |
| created_at / updated_at / processed_at | string/null | 创建 / 更新 / 处理时间 |

## 注意事项

- `date` 为必填，支持 YYYYMMDD 或 YYYY-MM-DD。
- `page_size` 最大 200。
- 取得 `announcement_id` 后可调用 `report-announcement-summary` 查询公告摘要。
- 两个路径（`/report-announcements/list` 与 `/report-announcement/list`）均为 v1 兼容入口。
