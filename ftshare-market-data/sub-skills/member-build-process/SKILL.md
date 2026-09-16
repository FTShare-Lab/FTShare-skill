---
name: member-build-process
description: 查询单个期货会员在指定合约/日期区间的持仓变化，并结合合约行情估算每日及累计盈亏。用户提到「会员建仓过程」「期货会员持仓盈亏」「会员净持仓变化」「member build process」时使用。按交易所/会员/合约过滤，可选日期区间和合约乘数，分页返回，page_size 最大 200，支持 --all 翻页。
---

# 查询期货会员建仓过程

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询期货会员建仓过程 |
| 外部接口 | GET /api/v2/market/data/member-build-process |
| 请求方式 | GET |
| 适用场景 | 查询单个期货会员在指定合约和日期区间内的持仓变化，并结合合约行情估算每日及累计盈亏 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| exchange | string | 是 | 交易所代码 | `DCE` | `SHFE`/`DCE`/`CZCE` 等 |
| member_name | string | 是 | 会员名称 | `永安期货` | 中文，URL 编码后传入 |
| instrument_id | string | 是 | 合约代码 | `a2609` | - |
| start_date | string | 否 | 起始日期 | `20260701` | YYYYMMDD 或 YYYY-MM-DD，默认 `20260101` |
| end_date | string | 否 | 结束日期 | `20260721` | YYYYMMDD 或 YYYY-MM-DD，默认当天 |
| contract_multiplier | float | 否 | 合约乘数 | `10` | 不传时按品种默认表推导 |
| page | int | 否 | 页码 | `1` | 默认 1 |
| page_size | int | 否 | 每页条数 | `50` | 默认 50，最大 200 |

## 执行方式

```bash
# 查某会员某合约某区间建仓过程
python <RUN_PY> member-build-process --exchange DCE --member_name 永安期货 --instrument_id a2609 --start_date 20260701 --end_date 20260721
# 指定合约乘数
python <RUN_PY> member-build-process --exchange SHFE --member_name 永安期货 --instrument_id rb2601 --contract_multiplier 10 --all
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

返回 `code/message/data`，记录位于 `data.records`。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pageNum": 1, "pageSize": 50, "total": 15, "pages": 1,
    "records": [
      {
        "trade_date": "2026-07-21", "exchange": "DCE", "instrument_id": "a2609",
        "product_name": "豆一", "member_name": "永安期货",
        "volume_rank": 1, "value": 10000, "change": 100,
        "long_rank": 2, "long_value": 5000, "long_change": 200,
        "short_rank": null, "short_value": null, "short_change": null,
        "net_position": 5000, "observed_side": "long",
        "open_price": "4200", "high_price": "4220", "low_price": "4180", "close_price": "4210",
        "settlement_price": "4205", "pre_settlement_price": "4198",
        "volume": "12345", "open_interest": "45678", "open_interest_change": "-100",
        "contract_multiplier": 10,
        "estimated_net_change": 100,
        "estimated_position_cost": 42000000.0,
        "estimated_daily_pnl": 5000.0, "estimated_daily_pnl_wan": 0.5,
        "estimated_cumulative_pnl": 25000.0, "estimated_cumulative_pnl_wan": 2.5
      }
    ]
  }
}
```

### records 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | string | 交易日 |
| exchange / instrument_id / product_name / member_name | string | 交易所 / 合约代码 / 品种名称 / 会员名称 |
| volume_rank / value / change | int/null | 成交排名 / 成交量 / 变化 |
| long_rank / long_value / long_change | int/null | 多头排名 / 持仓量 / 变化 |
| short_rank / short_value / short_change | int/null | 空头排名 / 持仓量 / 变化 |
| net_position | int/null | 净持仓 |
| observed_side | string | 观察方向 |
| open_price / high_price / low_price / close_price | string/null | 当日开高低收 |
| settlement_price / pre_settlement_price | string/null | 结算价 / 前结算价 |
| volume / open_interest / open_interest_change | string/null | 合约成交量 / 持仓量 / 持仓量变化 |
| contract_multiplier | float/null | 合约乘数 |
| estimated_net_change | int/null | 估算净持仓变化 |
| estimated_position_cost | float/null | 估算持仓成本 |
| estimated_daily_pnl / estimated_daily_pnl_wan | float/null | 估算当日盈亏 / 万元 |
| estimated_cumulative_pnl / estimated_cumulative_pnl_wan | float/null | 估算累计盈亏 / 万元 |

## 注意事项

- `exchange`/`member_name`/`instrument_id` 三者为必填。
- `contract_multiplier` 不传时按品种默认表推导；不同品种乘数不同，影响盈亏估算结果。
- 多数价格/数量字段以字符串返回，估算字段为 float。
- `page_size` 最大 200。
