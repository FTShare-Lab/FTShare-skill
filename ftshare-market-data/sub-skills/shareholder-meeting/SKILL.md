---
name: shareholder-meeting
description: 查询A股上市公司股东大会信息（market.ft.tech）。用户问股东大会、股东会议、股权登记日、投票日期、会议提案时使用。
---

# 股东大会 - 查询股东大会信息

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询股东大会 |
| 外部接口 | `GET /api/v1/market/data/corporate/meeting` |
| 请求方式 | GET |
| 适用场景 | 查询 A 股上市公司股东大会召开信息，包括会议日期、股权登记日、提案等，支持分页 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| page | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| page_size | int | 否 | 每页数量 | `50` | 默认 50，最大 200 |

## 3. 响应说明

返回 `PaginatedApiResponse` 包装的 JSON 对象。

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 50,
    "total": 189,
    "pages": 4,
    "records": [
      {
        "security_code": "920011",
        "security_name_abbr": "晨光电机",
        "meeting_title": "2026年第4次临时股东大会",
        "start_adjust_date": "2026-06-17",
        "equity_record_date": "2026-06-12",
        "onsite_record_date": null,
        "web_start_date": "2026-06-16",
        "web_end_date": "2026-06-17",
        "decision_notice_date": null,
        "notice_date": "2026-06-01",
        "serial_num": "238348",
        "proposal": "1、《关于公司董事2026年度薪酬方案的议案》"
      }
    ]
  }
}
```

### data.records 元素结构

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| security_code | string | 是 | 股票代码 |
| security_name_abbr | string | 是 | 股票简称 |
| meeting_title | string | 是 | 会议标题 |
| start_adjust_date | string | 是 | 开始调整日期（会议召开日期） |
| equity_record_date | string | 是 | 股权登记日 |
| onsite_record_date | string | 是 | 现场登记日 |
| web_start_date | string | 是 | 网络投票开始日期 |
| web_end_date | string | 是 | 网络投票结束日期 |
| decision_notice_date | string | 是 | 决议公告日期 |
| notice_date | string | 是 | 公告日期 |
| serial_num | string | 是 | 序号 |
| proposal | string | 是 | 提案内容 |

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> shareholder-meeting
python <RUN_PY> shareholder-meeting --page 1 --page_size 50
```

## 5. 请求示例

```
GET /api/v1/market/data/corporate/meeting?page=1&page_size=50
```

## 6. 注意事项

- 数据按 `notice_date` 降序排列。
- 日期字段以 YYYY-MM-DD 格式返回，无数据时为 null。
