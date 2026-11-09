---
name: sge-spot-description-all
description: 查询上海黄金交易所（SGE）现货/延期品种主档全量列表（sge_spot_description_all，GET /api/v1/market/data/sge-spot-description-all）。用户问上金所现货品种、黄金/白银品种代码、品种分类、合约乘数、保证金率、涨跌停板、最小变动价位、报价单位、交收规则或官网交易时间时使用。支持 --category 与 --active-only 过滤，不传参数返回全部 19 只品种。
---

# 上金所现货品种

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 上金所现货品种（sge_spot_description_all） |
| 外部接口 | `GET /api/v1/market/data/sge-spot-description-all` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 查询 SGE 现货实盘 / 现货即期 / 现货延期交收品种的主档快照 |
| 数据范围 | 品种主档快照，随官网更新，每天 17:30 更新；共 19 只（活跃 17 + 已下架 2） |

不传参数返回全部 19 只品种（含已下架）。`category` 与 `active_only` 可自由组合，返回结果按 `symbol` 升序。

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| category | string | 否 | 品种分类 | spot_deferred | 仅 `spot_full`（现货实盘）/ `spot_forward`（现货即期）/ `spot_deferred`（现货延期交收）；其他取值返回 400，空串视同未传 |
| active_only | boolean | 否 | 仅返回活跃品种 | true | `true` 返回 17 只活跃品种；`false` 或缺省返回全部；空串视同未传；其他非布尔值返回 400 |

该接口无分页，一次返回满足过滤条件的全部品种（最多 19 只）。

## 3. 响应说明

外层固定为 `code` / `message` / `data`；成功时 `code=200`、`message=success`，`data` 为品种数组。

`data` 元素：

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| symbol | string | 否 | 品种代码，含交易所后缀，如 `AG9999.SGEX` |
| exchange | string | 否 | 交易所代码，如 `SGEX` |
| type | string | 否 | 品种类型，如 `Spot` |
| symbol_cn_name | string | 否 | 中文简称，如 白银9999 |
| listed_date | string | 否 | 上市日期，`YYYY-MM-DD` |
| de_listed_date | string | 是 | 下架日期，`YYYY-MM-DD`；活跃品种为 `null` |
| market_tplus | integer | 否 | T+N 交易日限制 |
| trading_hours | string | 是 | 官网交易时间原文（含集合竞价段）；下架品种为 `null` |
| contract_multiplier | number | 否 | 合约乘数，统一按克（白银官网按千克，已折算为克） |
| margin_rate | number | 否 | 保证金率，小数；现货实盘类全额交易为 1.0 |
| round_lot | integer | 否 | 每手最小交易单位 |
| category | string | 否 | 品种分类：spot_full / spot_forward / spot_deferred |
| official_code | string | 否 | 官网代码（slug），如 `Au(T+D)`、`Ag9999` |
| limit_pct | number | 是 | 涨跌停板百分比，如 30.0；下架品种为 `null` |
| min_move | number | 是 | 最小变动价位；下架品种为 `null` |
| quote_unit | string | 是 | 报价单位，如 `元（人民币）/克`；下架品种为 `null` |
| settle_rule | string | 是 | 官网交收规则原文，如 `T+0`；下架品种为 `null` |

## 4. 调用方式

```bash
# 全部 19 只品种
python <RUN_PY> sge-spot-description-all

# 仅活跃的现货延期交收品种
python <RUN_PY> sge-spot-description-all --category spot_deferred --active-only

# 仅现货实盘
python <RUN_PY> sge-spot-description-all --category spot_full
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。脚本输出格式化 JSON；HTTP / 网络错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `symbol` 含交易所后缀（如 `AG9999.SGEX`），`official_code` 是官网代码（如 `Ag9999`），两者格式不同。
- 交易所会在节假日前后动态调整保证金率与涨跌停板，返回值为最近一次更新的口径。
- `contract_multiplier` 统一按克计；`limit_pct`、`min_move`、`quote_unit`、`settle_rule` 为官网独有字段，缺失（尤其下架品种）时返回 `null`。
- 不传 `active_only` 与传 `false` 等价；本子 skill 仅在需要活跃品种时传该参数。
