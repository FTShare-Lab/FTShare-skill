---
name: futures-dominant-mapping
description: "查询指定生效交易日的期货主力合约映射，返回各交易所各品种的主力合约代码与规则版本。当用户询问期货主力合约、主连对应真实合约、某日主力是哪个合约或主力换月时使用。Use when user asks about 期货主力合约、主力映射、dominant contract."
---

# 期货主力合约映射

接口：`GET /api/v1/market/data/futures/dominant-mapping`。

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 期货主力合约映射 |
| 外部接口 | `/api/v1/market/data/futures/dominant-mapping` |
| 请求方式 | GET |
| 适用场景 | 查询某生效交易日各交易所、各期货品种对应的主力合约代码 |
| 数据范围 | 按交易日查询；`v1`/`v2`/`v3`/`v4` 各交易所起始日不同：DCE `20000508`、SHFE `20020107`、CFFEX `20100416`、CZCE `20150921`、INE `20180326`、GFEX `20221222` |
| 更新频率 | 每晚 18:10 更新 T+1 数据 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|---|---|---|---|---|
| `trade_date` | string | 是 | 主力映射生效交易日，格式 `YYYYMMDD` | `20261123` |
| `rule_version` | string | 否 | 主力规则版本：`v1`、`v2`、`v3`、`v4`，区分大小写；省略或传空值默认 `v1`，传入不支持的版本返回空数组 | `v2` |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 查询某日主力映射（默认 v1 规则）
python <RUN_PY> futures-dominant-mapping --trade-date 20261123

# 指定规则版本
python <RUN_PY> futures-dominant-mapping --trade-date 20261123 --rule-version v4

# 只看某个交易所或品种的组合，可用 jq 过滤
python <RUN_PY> futures-dominant-mapping --trade-date 20261123 | jq '.data[] | select(.exchange == "CFFEX")'
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

`data` 为主力映射数组，不分页；无匹配记录时为空数组：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "trade_date": "20261123",
            "exchange": "CFFEX",
            "variety": "IF",
            "dominant_symbol": "IF2612",
            "rule_version": "v1"
        },
        {
            "trade_date": "20261123",
            "exchange": "CZCE",
            "variety": "AP",
            "dominant_symbol": "AP2701",
            "rule_version": "v1"
        }
    ]
}
```

### data 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `trade_date` | string | 否 | 主力映射生效交易日，`YYYYMMDD` |
| `exchange` | string | 否 | 交易所代码，例如 `CFFEX`、`CZCE`、`SHFE`、`INE`、`GFEX`、`DCE` |
| `variety` | string | 否 | 期货品种代码，例如 `IF`、`CU`、`AP`、`EC` |
| `dominant_symbol` | string | 否 | 当日实际主力合约代码，按交易所官网口径返回：CZCE、CFFEX 大写，SHFE、INE、DCE、GFEX 小写；CZCE 为四位年份格式 |
| `rule_version` | string | 否 | 本条记录采用的主力规则版本 |

## 注意事项

- `trade_date` 必填，且必须是有效日期；接口按生效交易日查询，通常使用 T 日收盘后数据决定 T+1 日生效的主力映射。
- 不同规则版本的换月逻辑不同：`v1` 按前一交易日量仓排名、不限方向换月；`v2` 只向远月换月且要求持仓量超过当前主力 `1.1` 倍；`v3` 只向远月换月但无 `1.1` 倍阈值；`v4` 对 CFFEX 股指期货每月重排、无 `1.1` 倍阈值。
- 查询无匹配记录或传入不支持的 `rule_version` 时仍返回成功响应，`data` 为空数组，不是报错。
- 同一交易日的记录条数随规则版本和可用品种变化，调用方不要按固定条数解析。
- 主力合约是期货代码，可直接传给 `futures-daily-kline`、`futures-kline` 等按 `symbol` 查询的接口。