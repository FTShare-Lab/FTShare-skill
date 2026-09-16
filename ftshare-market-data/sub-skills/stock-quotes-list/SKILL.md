---
name: stock-quotes-list
description: "查询 A 股行情列表（分页）。当用户需要获取 A 股（沪深京）股票行情列表，支持按板块筛选、多字段排序与分页，用于行情中心「个股行情」等列表展示，或了解A 股行情列表（分页）时使用。"
---

# 查询 A 股行情列表（分页）

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询 A 股行情列表（分页） |
| 外部接口 | `/api/v1/market/data/daec/stocks` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股（沪深京）股票行情列表，支持按板块筛选、多字段排序与分页，用于行情中心「个股行情」等列表展示 |

请求头要求：必须携带 `X-Client-Name: ft-claw`，否则返回参数错误。

## 请求参数

说明：`order_by`、`page_no`、`page_size` 为必填项；`filter`、`masks` 为可选项，用于筛选与字段控制。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| order_by | string | 是 | 排序规则，格式为「字段 排序方向」 | change_rate desc | 常用：change_rate desc、change desc、latest desc、turnover desc、volume desc、market_cap_total desc、turnover_rate desc、change_rate_5d desc、amplitude desc；方向为 asc/desc |
| page_no | int | 是 | 页码，从 1 开始 | 1 | 必须大于等于 1 |
| page_size | int | 是 | 每页记录数 | 30 | 必须大于等于 1，建议不超过 100 |
| filter | string | 否 | 筛选条件表达式 | (ex_id = "XSHE" OR ex_id = "XSHG" OR ex_id = "BJSE") AND (latest != null) | 见下方「filter 常用取值」 |
| masks | string | 否 | 返回字段掩码/控制 | - | 不传则返回默认字段集 |

### filter 常用取值（按板块）

| 板块 | filter 取值 |
|---|---|
| 全部股票 | (ex_id = "XSHE" OR ex_id = "XSHG" OR ex_id = "BJSE") AND (latest != null) |
| 上交主板 | ex_id = "XSHG" AND latest != null |
| 深交主板 | ex_id = "XSHE" AND latest != null |
| 北交主板 | ex_id = "BJSE" AND latest != null |
| 科创板 | board = "XSHG_STAR" AND latest != null |
| 创业板 | board = "XSHE_CHI_NEXT" AND latest != null |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-quotes-list --order_by "change_rate desc" --page_no 1 --page_size 30
```

可选参数：`--filter`、`--masks`。示例（仅科创板）：

```bash
python <RUN_PY> stock-quotes-list --order_by "change_rate desc" --page_no 1 --page_size 30 --filter 'board = "XSHG_STAR" AND latest != null'
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应说明

返回当前页股票列表及总条数，数据模型如下：

```json
{
    "total_size": 5000,
    "stocks": [ { "StockInfo" } ]
}
```

### 顶层字段

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| total_size | int | 否 | 符合筛选条件的总记录数，用于分页计算 |
| stocks | array | 否 | 当前页股票列表，元素为 StockInfo |

### StockInfo 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| name | string | 是 | 股票名称 | - |
| symkey | string | 是 | 股票唯一标识，带市场后缀（如 920036.BJ、002445.SZ） | - |
| symbol_id | string | 是 | 证券代码（不含市场后缀） | - |
| ex_id | string | 是 | 交易所标识：XSHG（上交所）、XSHE（深交所）、BJSE（北交所） | - |
| board | string | 是 | 板块标识，如 XSHG_STAR（科创板）、XSHE_CHI_NEXT（创业板） | - |
| latest | number | 是 | 最新价 | 元 |
| open | number | 是 | 今开；非交易时段或未开盘时可能为空 | 元 |
| high | number | 是 | 最高价 | 元 |
| low | number | 是 | 最低价 | 元 |
| prev_close | number | 是 | 前收盘价 | 元 |
| close | number | 是 | 收盘价 | 元 |
| change | number | 是 | 涨跌额 | 元 |
| change_rate | number | 是 | 涨跌幅，小数值（如 0.1175 表示 11.75%） | 小数 |
| turnover | number | 是 | 成交额；非交易时段或停牌可为 0 | 元 |
| volume | number | 是 | 成交量（股）；前端常除以 100 显示为「手」 | 股 |
| market_cap_total | number | 是 | 总市值 | 元 |
| turnover_rate | number | 是 | 换手率，小数值（如 0.05 表示 5%）；非交易时段可为 0 | 小数 |
| change_rate_5d | number | 是 | 五日涨跌幅，小数值 | 小数 |
| amplitude | number | 是 | 振幅，小数值 | 小数 |
| limit_up | number | 是 | 涨停价 | 元 |
| limit_down | number | 是 | 跌停价 | 元 |
| is_in_default_choice_group | boolean | 是 | 是否在用户默认自选列表中；未登录时为 null | - |
| trading_status | string | 是 | 交易状态：LIMIT_UP（涨停）、LIMIT_DOWN（跌停）、NORMAL（正常） | - |
| symbol_status | object | 是 | 标的状态，含 base、extra 等 | - |
| margin_status | string | 是 | 融资融券状态：BOTH、NONE 等 | - |
| industry_sector | object | 是 | 行业板块，含 code、name | - |

## 注意事项

- 涨跌幅、换手率、振幅等比率为小数值，展示时乘以 100 转为百分比
- `filter` 中含空格、引号、括号，通过 run.py 传参时需按 shell 规则正确引号包裹（如单引号包裹整段 filter）
