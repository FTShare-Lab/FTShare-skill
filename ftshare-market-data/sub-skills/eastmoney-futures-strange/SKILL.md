---
name: eastmoney-futures-strange
description: 查询东方财富期货龙虎榜面板（成交量/持仓量多空排名等）。用户提到「东财期货龙虎榜」「期货龙虎榜面板」「期货会员排名」「eastmoney futures strange」时使用。按交易所/品种/合约/交易日返回完整面板数组，不分页。
---

# 查询东方财富期货龙虎榜

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询东方财富期货龙虎榜 |
| 外部接口 | GET /api/v1/market/data/eastmoney-futures-strange |
| 请求方式 | GET |
| 适用场景 | 查询指定交易所、品种、合约和交易日的东方财富期货龙虎榜面板，包括占比切片、会员排名和汇总数据 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| exchange | string | 是 | 交易所代码 | `dce` | `shfe`/`dce`/`czce`/`cffex`/`ine`/`gfe` |
| variety | string | 是 | 品种名称 | `多晶硅` | 中文名称，URL 编码后传入 |
| contract | string | 是 | 合约代码 | `ps2609` | 小写合约代码 |
| trade_date | string | 是 | 交易日 | `20260721` | `YYYYMMDD` |

## 执行方式

```bash
python <RUN_PY> eastmoney-futures-strange --exchange dce --variety 多晶硅 --contract ps2609 --trade_date 20260721
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。

## 响应结构

返回统一结构 `code/message/data`，`data` 为面板数组（不分页）。

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "key": "volume_rank",
      "title": "成交量龙虎榜",
      "slices": null,
      "rows": [{"rank": 1, "member_name": "东证期货（代客）", "value": 24952, "change": -4961}],
      "summary": {"today_total": 175902, "previous_total": 218790, "total_change": -42888}
    }
  ]
}
```

### data 元素字段

| 字段 | 类型 | 是否可为空 | 说明 |
|------|------|------------|------|
| key | string | 否 | 面板标识 |
| title | string | 否 | 面板标题 |
| slices | array/null | 是 | 饼图切片；每项含 `name`/`value`/`percent` |
| rows | array/null | 是 | 排名记录；每项含 `rank`/`member_id`/`member_name`/`value`/`change` |
| summary | object/null | 是 | 汇总；含 `today_total`/`previous_total`/`total_change` |

## 注意事项

- 所有参数均为必填，缺一返回 400。
- 单次返回该合约对应的完整面板数组，不分页。
- `variety` 为中文品种名称，调用时通过 URL 编码传入。
- HTTP 恒为 200，业务错误通过 `code`/`message` 携带。
