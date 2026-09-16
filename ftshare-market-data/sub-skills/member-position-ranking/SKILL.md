---
name: member-position-ranking
description: 查询指定交易日/交易所/合约/方向的期货会员持仓排名（品种/合约/方向/会员/持仓量/持仓量变化/净持仓）。用户提到「会员持仓排名」「期货会员持仓」「多头排名」「空头排名」「member position ranking」时使用。按交易所/合约/交易日/方向过滤，分页返回，page_size 最大 200，支持 --all 翻页。
---

# 查询期货会员持仓排名

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询期货会员持仓排名 |
| 外部接口 | GET /api/v2/market/data/member-position-ranking |
| 请求方式 | GET |
| 适用场景 | 查询指定交易日、交易所、合约及方向的期货会员持仓排名 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| exchange | string | 是 | 交易所代码 | `DCE` | `SHFE`/`DCE`/`CZCE` 等 |
| instrument_id | string | 是 | 合约代码 | `a2605` | - |
| trade_date | string | 是 | 交易日 | `20260721` | YYYYMMDD 或 YYYY-MM-DD |
| direction | string | 是 | 查询方向 | `long` | `long` 或 `short`，也接受常见中文和缩写别名 |
| page | int | 否 | 页码 | `1` | 默认 1 |
| page_size | int | 否 | 每页条数 | `50` | 默认 50，最大 200 |

## 执行方式

```bash
# 查某合约某日多头会员排名
python <RUN_PY> member-position-ranking --exchange DCE --instrument_id a2605 --trade_date 20260721 --direction long
# 查空头排名并翻全量
python <RUN_PY> member-position-ranking --exchange SHFE --instrument_id rb2610 --trade_date 20260721 --direction short --all
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

返回 `code/message/data`，记录位于 `data.records`。

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pageNum": 1, "pageSize": 50, "total": 100, "pages": 2,
    "records": [
      {
        "variety": "a", "code": "a2605", "date": "2026-07-21",
        "direction": "long", "broker": "永安期货",
        "oi": 10000, "oi_chg": 200, "net_position": 5000
      }
    ]
  }
}
```

### records 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| variety | string | 品种名称或代码 |
| code | string | 合约代码 |
| date | string | 交易日 |
| direction | string | 持仓方向 |
| broker | string | 期货会员名称 |
| oi | int64/null | 持仓量 |
| oi_chg | int64/null | 持仓量变化 |
| net_position | int64/null | 净持仓 |

## 注意事项

- `exchange`/`instrument_id`/`trade_date`/`direction` 四者均为必填。
- `direction` 接受 `long`/`short` 及常见中文和缩写别名。
- `page_size` 最大 200。
