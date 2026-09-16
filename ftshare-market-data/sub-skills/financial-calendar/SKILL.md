---
name: financial-calendar
description: 按日期范围查询财经日历（market.ft.tech），含华尔街见闻与百度财经日历数据（宏观数据、IPO、财报时间、交易提醒等）。用户问财经日历、经济事件、IPO 日程、财报时间、交易提醒时使用。
---

# 查询财经日历

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询财经日历 |
| 外部接口 | `GET /api/v1/market/data/finance/financial-calendar` |
| 请求方式 | GET |
| 适用场景 | 按日期范围查询华尔街见闻与百度财经日历数据（宏观数据、IPO、财报时间、交易提醒等） |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| start_date | string | 是 | 开始日期 | 2026-05-01 | 格式 `YYYY-MM-DD` |
| end_date | string | 是 | 结束日期 | 2026-05-07 | 格式 `YYYY-MM-DD` |

## 3. 响应说明

响应为信封结构 `code` / `message` / `data`，`data` 包含两大来源：

### 3.1 华尔街见闻（wallstreetcn）

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| stat_date | string | 否 | 统计日期 |
| tab_type | string | 否 | 标签类型 |
| event_time | string | 否 | 事件时间 |
| region | string | 否 | 地区 |
| event | string | 否 | 事件名称 |
| importance | string | 否 | 重要程度 |
| actual_value | string | 是 | 公布值 |
| forecast_value | string | 是 | 预测值 |
| previous_value | string | 是 | 前值 |

### 3.2 百度财经日历（baidu）

包含四类数据：

- **economic**（经济数据）：region、time、title、former_val、market_value、pub_val、indicate_val、star、negative、positive
- **ipo**（IPO 数据）：code、name、exchange、market、price、volume、amount、pe_ratio 等
- **report_time**（财报时间）：code、name、exchange、market、report_type、market_time 等
- **trade_reminder**（交易提醒）：code、name、exchange、market、meeting_type、reason、divi_cash、divi_date 等

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "wallstreetcn": { "items": [] },
    "baidu": {
      "economic": { "items": [] },
      "ipo": { "items": [] },
      "report_time": { "items": [] },
      "trade_reminder": { "items": [] }
    }
  }
}
```

## 4. 用法

通过主目录 `run.py` 调用（必填 `--start-date`、`--end-date`）：

```bash
python <RUN_PY> financial-calendar --start-date 2026-05-01 --end-date 2026-05-03
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 5. 注意事项

- 日期格式为 `YYYY-MM-DD`。
- 各 `items` 列表可能为空数组，表示该日期范围内无对应事件。
- 百度侧 IPO、财报时间、交易提醒等条目中，类型字段 JSON 名为 `type`。
- **多日范围查询可能因响应过大导致服务端截断**（服务端 HTTP/2 限制）。建议每次仅查询单日（`start_date` 与 `end_date` 相同），如需多日数据请逐日调用后合并。
