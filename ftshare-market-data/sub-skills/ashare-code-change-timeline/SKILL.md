---
name: ashare-code-change-timeline
description: 查询 A 股代码变更时间线（全量）。Use when user asks about A 股代码变更时间线、换码事件全量列表、代码迁移对照表、新旧代码启用区间、全市场换码记录。
---

# A 股代码变更时间线

接口：`GET /api/v1/market/data/stk_code_change_timeline`。无入参，全量返回全部代码变更事件，不分页。

```bash
python <RUN_PY> ashare-code-change-timeline
```

成功响应为 `code/message/data`，`data` 为记录数组，每条记录描述一次换码事件：

| 字段 | 类型 | 说明 |
|------|------|------|
| stock_name | string | 证券名称 |
| new_code | string | 换码后的新代码 |
| new_code_start | string | 新代码启用起始日期 `YYYYMMDD` |
| old_code | string | 换码前的旧代码 |
| old_code_start | string | 旧代码启用起始日期 `YYYYMMDD` |
| old_code_end | string | 旧代码停用日期 `YYYYMMDD` |
| old_last_trade_dt | string | 旧代码最后交易日 `YYYYMMDD` |
| new_first_trade_dt | string | 新代码首个交易日 `YYYYMMDD` |
| market | string | 所属市场，取值 `SH` / `SZ` / `BJ` |

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "stock_name": "上海医药",
            "new_code": "601607",
            "new_code_start": "20100305",
            "old_code": "600849",
            "old_code_start": "19940324",
            "old_code_end": "20100304",
            "old_last_trade_dt": "20100225",
            "new_first_trade_dt": "20100309",
            "market": "SH"
        }
    ]
}
```

## 注意事项

- 无入参，一次性返回全部记录（覆盖 1993 年以来的 A 股代码变更）。
- 日期字段均为 `YYYYMMDD` 字符串（如 `20181226`），非时间戳；代码为六位纯数字，不带交易所后缀。
- `market` 取值 `SH`（上交所）/ `SZ`（深交所）/ `BJ`（北交所）。
- 若需要按单只股票查询其代码变更历史，请使用 `ashare-code-change` 子 skill。
