---
name: index-fut-depth
description: 查询股指期货合约深度快照、对应指数价格与仪器映射（index_fut_depth，GET /api/v1/market/data/index-fut/depth）。用户问股指期货行情、IF/IC/IM/IH 合约快照、期货基差/年化基差/分红调整基差、对应指数点位、期货与指数映射时使用。支持 --trade-date 单日、--start-date/--end-date 区间与 --code-prefix 品种筛选。
---

# 股指期货与指数深度行情

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 股指期货与指数深度行情（index_fut_depth） |
| 外部接口 | `GET /api/v1/market/data/index-fut/depth` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 查询 IF / IC / IM / IH 股指期货深度快照、对应指数价格和仪器映射 |
| 数据范围 | 按交易日查询；历史数据自 20261030 起 |

不传日期参数时默认查询最新交易日。历史区间内 `futures` 与 `index` 按闭区间返回每个交易日；`instrument_map` 只返回一份。

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_date | string | 否 | 单日查询日期 | 20261030 | 格式 `YYYYMMDD`；与 `start_date`、`end_date` 互斥；不传日期参数时查询最新交易日 |
| start_date | string | 否 | 区间起始交易日 | 20261030 | 格式 `YYYYMMDD`；必须与 `end_date` 同时传入 |
| end_date | string | 否 | 区间结束交易日 | 20261103 | 格式 `YYYYMMDD`；必须与 `start_date` 同时传入，不得早于起始日，区间最长 3 年 |
| code_prefix | string | 否 | 品种筛选 | IF | 仅 `IF` / `IC` / `IM` / `IH`，不区分大小写；不传返回全部品种 |

接口全量返回、无分页；历史区间内每日数据按闭区间返回，`instrument_map` 只返回一份。

## 3. 响应说明

外层固定为 `code` / `message` / `data`；成功时 `code=200`、`message=success`。

`data` 对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| count | integer | `futures` 数组中的期货合约记录数 |
| futures | array | 期货合约深度快照列表；每条记录带 `trade_date` |
| index | array | 指数价格快照列表；同一标的的完整价格与快速价格合并在同一条记录中 |
| instrument_map | object | 仪器映射信息，按 `fut_info` / `index_info` 分组 |

`futures` 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| trade_date | string | 交易日 `YYYYMMDD` |
| code_prefix | string | 品种代码 IF / IC / IM / IH |
| delivery_code | integer | 交割合约代码 |
| expire_date | string | 合约到期日 `YYYYMMDD` |
| days_left | integer | 剩余交易日数 |
| price | number | 期货价格 |
| volume | number | 成交量 |
| open_interest | number | 持仓量 |
| dividend_config | number | 分红配置值 |
| index_price | number | 对应指数的 `full` 口径价格，用于基差计算 |
| basis | number | 基差 |
| div_basis | number | 分红调整后的基差 |
| div_basis_ratio_pct | number | 分红调整后基差比例（百分比数值） |
| basis_daily_pct | number/null | 基差日度百分比；无数据为 `null` |
| basis_ann_pct | number/null | 基差年化百分比；无数据为 `null` |
| basis_ann_nodiv_pct | number/null | 不考虑分红的基差年化百分比；无数据为 `null` |
| timestamp | string | 期货深度快照时间 `YYYY-MM-DD HH:MM:SS.fff`，无时区偏移 |

`index` 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| trade_date | string | 交易日 `YYYYMMDD` |
| symbol_id | integer | 指数标识 |
| name | string | 指数名称 |
| price_full | number/null | 深度快照确认的正式点位，用于基差计算；无数据为 `null` |
| price_quick | number/null | 逐 tick 快速点位，仅辅助观察，不参与基差计算；无数据为 `null` |

`instrument_map` 对象包含 `fut_info` / `index_info` 两个数组，元素字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code_prefix | string/null | 品种代码；指数映射没有对应品种时为 `null` |
| ex_id | integer | 交易所标识 |
| symbol_id | integer | 仪器标识 |
| index_symbol_id | integer/null | 关联指数标识；无关联为 `null` |
| fut_symbol_id | integer/null | 关联期货标识；无关联为 `null` |
| multiplier | number/null | 合约乘数；无数据为 `null` |
| symbol_name | string/null | 仪器名称；无数据为 `null` |

## 4. 调用方式

```bash
# 最新交易日、全部品种
python <RUN_PY> index-fut-depth

# 指定交易日 + 品种
python <RUN_PY> index-fut-depth --trade-date 20261030 --code-prefix IF

# 历史区间（闭区间，需成对传入）
python <RUN_PY> index-fut-depth --start-date 20261030 --end-date 20261103 --code-prefix IC
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。脚本输出格式化 JSON；HTTP / 网络错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `trade_date` 与 `start_date` / `end_date` 互斥；`start_date` 与 `end_date` 必须成对传入。本子 skill 会在本地校验并拒绝冲突参数。
- 日期格式仅支持 `YYYYMMDD`；传 `YYYY-MM-DD` 返回 HTTP 400，本地也会直接拒绝。
- `code_prefix` 只筛选 `futures` 与 `instrument_map.fut_info`；`index` 与 `instrument_map.index_info` 不按品种过滤。
- 历史数据自 `20261030` 起；早于该日的交易日没有记录，区间查询只返回该日起已有的交易日。
- `price_full` 是深度快照确认的正式点位，用于 `futures.index_price` 与基差计算；`price_quick` 不能替代 `price_full`。
- 历史区间查询时，`instrument_map` 只对应当次 `futures` 的最大 `trade_date`；`futures` 为空时对应 `index` 的最大 `trade_date`。
