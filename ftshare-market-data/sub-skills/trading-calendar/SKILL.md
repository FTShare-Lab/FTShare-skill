---
name: trading-calendar
description: 查询中国内地（cn）或香港（hk）市场在指定闭区间内的交易日列表。用户提到「交易日历」「A 股交易日」「港股交易日」「某区间内的交易日」「trading calendar」时使用。返回裸 JSON 对象（market/start_date/end_date/trade_dates），不使用通用 code/message/data 信封。
---

# 查询交易日历

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询交易日历 |
| 外部接口 | GET /api/v1/market/data/time/trading-calendar |
| 请求方式 | GET |
| 适用场景 | 查询中国内地或香港市场在指定闭区间内的交易日列表 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| market | string | 是 | 市场 | `cn` | 仅支持 `cn`（中国内地）/ `hk`（香港） |
| start_date | int | 是 | 起始日期（含） | `20251001` | YYYYMMDD |
| end_date | int | 是 | 截止日期（含） | `20251003` | YYYYMMDD；须 `>= start_date` |

> 请求区间的起止日期必须全部位于所选市场的日历覆盖范围内：
> - `cn`：2000-01-04 至 2026-12-31
> - `hk`：2010-01-04 至 2026-12-31

## 执行方式

```bash
# 查港股某区间交易日
python <RUN_PY> trading-calendar --market hk --start_date 20251001 --end_date 20251003
# 查 A 股某区间交易日
python <RUN_PY> trading-calendar --market cn --start_date 20260101 --end_date 20260131
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

返回值为**裸 JSON 对象**，不使用通用的 `code/message/data` 响应信封。

```json
{
  "market": "hk",
  "start_date": 20251001,
  "end_date": 20251003,
  "trade_dates": [20251002, 20251003]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| market | string | 请求的市场，`cn` 或 `hk` |
| start_date | int | 请求的起始日期，YYYYMMDD |
| end_date | int | 请求的截止日期，YYYYMMDD |
| trade_dates | array&lt;int&gt; | 日期闭区间内按升序排列的交易日 |

## 注意事项

- `market` 仅支持 `cn` 和 `hk`，其他值返回 400。
- `start_date` 不得晚于 `end_date`；区间须全部落在所选市场的日历覆盖范围内。
- 响应直接是裸 JSON 对象，无 `code`/`message` 信封。
