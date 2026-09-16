---
name: stock-dividends-effective
description: 查询 A 股已实施（有效）分红记录（stock_dividends_effective）。用户问已实施分红、每股派息、送股、转增、除权除息日、股权登记日、现金到账日、分红公告链接时使用。
---

# 股票有效分红记录

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 股票有效分红记录（stock_dividends_effective） |
| 外部接口 | `GET /api/v2/market/data/stock-dividends-effective` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 查询 A 股已实施分红记录（派息、送股、转增）分页视图，可按标的和公告日期范围筛选 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 否 | 标的代码 | 600519.XSHG | 支持带交易所后缀；不传返回全市场 |
| since_date | string | 成对 | 开始公告日期 | 2026-05-26 | 格式 `YYYY-MM-DD`，按 `ann_date` 筛选 |
| until_date | string | 成对 | 结束公告日期 | 2026-05-26 | 与 `since_date` 成对且不早于开始日期 |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 50 | 默认 50，最大 200 |
| --all | - | 否 | 自动翻页拉全量 | - | 仅本子 skill 扩展参数 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为分页对象：`pageNum` / `pageSize` / `total` / `pages` / `records`。

records 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 标的代码（规范化为短后缀，如 `600519.SH`） |
| ann_date | string | 公告日期 |
| reporting_period | string | 分红所属报告期 |
| cash_dividend_ratio | string | 每股税前现金分红 |
| bonus_issue_ratio | string | 每股送股比例 |
| bonus_issue_from_capital_reserves_ratio | string | 每股转增比例 |
| ex_dividend_date | string / null | 除权除息日 |
| record_date | string / null | 股权登记日 |
| payout_date | string / null | 现金到账日 |
| share_listing_date | string / null | 送转股上市流通日 |
| ann_url | string / null | 公告链接 |
| total_cash_dividend_ratio | string / null | 同一股票同一除权日综合每股税前现金分红 |
| total_bonus_issue_ratio | string / null | 同一股票同一除权日综合每股送股比例 |
| total_bonus_issue_from_capital_reserves_ratio | string / null | 同一股票同一除权日综合每股转增比例 |

## 4. 调用方式

```bash
python <RUN_PY> stock-dividends-effective --symbol 600519.XSHG --page 1 --page-size 1
python <RUN_PY> stock-dividends-effective --symbol 002043.SZ --since-date 2026-05-26 --until-date 2026-05-26
python <RUN_PY> stock-dividends-effective --all
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 只返回已实施的分红记录；未实施或已取消的不返回。
- 同一股票同一除权日可能返回多条记录；三个 `total_*` 字段为该组合计，组内各条记录取值相同。
- 输入代码会规范化为带交易所后缀的 `symbol`，例如输入 `600519.XSHG` 返回 `600519.SH`。
- 日期按公告日期 `ann_date` 筛选，不限制日期跨度；`since_date` / `until_date` 必须成对传入（handler 会本地校验并拒绝）。
- `--all` 会按 `pages` 自动翻页，把所有 `records` 合并为一个数组返回。
