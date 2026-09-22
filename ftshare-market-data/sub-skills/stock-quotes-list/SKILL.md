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

`board` 字段当前不可用于 `filter`：写成 `board = "..."` 服务端返回 `code=502`「下游服务请求失败」，加引号写成 `"board" = "..."` 则不报错但匹配不到任何记录。`filter` 支持 `ex_id`、`latest` 等字段，`total_items` 在带 `filter` 时不反映筛选后的实际条数（恒为全量），分页以 `items` 实际返回为准。

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-quotes-list --order_by "change_rate desc" --page_no 1 --page_size 30
```

可选参数：`--filter`、`--masks`。示例（仅上交所）：

```bash
python <RUN_PY> stock-quotes-list --order_by "change_rate desc" --page_no 1 --page_size 30 --filter 'ex_id = "XSHG" AND latest != null'
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应说明

返回当前页股票列表及总条数，数据模型如下：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "page": 1,
        "page_size": 3,
        "total_pages": 1966,
        "total_items": 5897,
        "items": [ { "StockInfo" } ]
    }
}
```

### 顶层字段

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| page | int | 否 | 当前页码 |
| page_size | int | 否 | 每页条数 |
| total_pages | int | 否 | 总页数 |
| total_items | int | 否 | 总记录数（带 `filter` 时可能不反映筛选结果，见上） |
| items | array | 否 | 当前页股票列表，元素为 StockInfo |

### StockInfo 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| name | string | 是 | 股票名称 | - |
| symbol | string | 是 | 股票代码，带市场短后缀（如 `600000.SH`、`000001.SZ`、`920680.BJ`） | - |
| symbol_id | string | 是 | 证券代码（不含市场后缀） | - |
| board | string | 是 | 板块标识：`XshgMain`、`XsheMain`、`XshgStar`、`XsheChiNext`、`Bjse` | - |
| latest | number | 是 | 最新价 | 元 |
| open | string | 是 | 今开；非交易时段或未开盘时可能为空 | 元 |
| high | string | 是 | 最高价 | 元 |
| low | string | 是 | 最低价 | 元 |
| prev_close | string | 是 | 前收盘价 | 元 |
| close | string | 是 | 收盘价 | 元 |
| change | string | 是 | 涨跌额 | 元 |
| change_rate | number | 是 | 涨跌幅，小数值（如 0.1175 表示 11.75%） | 小数 |
| avg | number | 是 | 均价 | 元 |
| bid_ask_ratio | number | 是 | 委比 | 小数 |
| turnover | string | 是 | 成交额；非交易时段或停牌可为 0 | 元 |
| volume | integer | 是 | 成交量（股）；前端常除以 100 显示为「手」 | 股 |
| turnover_rate | number | 是 | 换手率，小数值（如 0.05 表示 5%）；非交易时段可为 0 | 小数 |
| amplitude | number | 是 | 振幅，小数值 | 小数 |
| market_cap | string | 是 | 总市值 | 元 |
| tradable_a_market_cap | string | 是 | 流通 A 股市值 | 元 |
| float_a_shares | integer | 是 | 流通 A 股数量 | 股 |
| shares | integer | 是 | 总股本 | 股 |
| pe_ttm | number | 是 | 市盈率（TTM） | 倍 |
| st | boolean | 是 | 是否 ST | - |
| status | string | 是 | 交易状态：`Normal`（正常）、`Delisted`（已退市）等 | - |
| listing_date | string | 是 | 上市日期，`YYYY-MM-DD` | - |
| ts_millis | integer | 是 | 行情时间戳（毫秒，原样返回，未转 ISO 字符串） | 毫秒 |
| change_rate_day5 | number | 是 | 五日涨跌幅，小数值 | 小数 |
| change_rate_day10 | number | 是 | 十日涨跌幅，小数值 | 小数 |
| change_rate_day20 | number | 是 | 二十日涨跌幅，小数值 | 小数 |
| change_rate_day60 | number | 是 | 六十日涨跌幅，小数值 | 小数 |
| change_rate_day120 | number | 是 | 一百二十日涨跌幅，小数值 | 小数 |
| change_rate_ytd | number | 是 | 年初至今涨跌幅，小数值 | 小数 |

## 注意事项

- 涨跌幅、换手率、振幅等比率为小数值，展示时乘以 100 转为百分比
- `filter` 中含空格、引号、括号，通过 run.py 传参时需按 shell 规则正确引号包裹（如单引号包裹整段 filter）
