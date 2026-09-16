---
name: pledge-summary
description: "查询所有期股权质押总揽数据。当用户需要获取 A 股市场所有报告期的股权质押总揽数据，包括质押公司数量、质押笔数、质押总股数、质押总市值、沪深300指数等信息，支持沪深京股票，或了解所有期股权质押总揽数据时使用。"
---

# 查询所有期股权质押总揽数据

## 接口说明

| 项目     | 说明                                                                                                                       |
|----------|----------------------------------------------------------------------------------------------------------------------------|
| 接口名称 | 查询所有期股权质押总揽数据                                                                                                 |
| 外部接口 | `/api/v1/market/data/pledge/pledge-summary`                                                                           |
| 请求方式 | GET                                                                                                                        |
| 适用场景 | 获取 A 股市场所有报告期的股权质押总揽数据，包括质押公司数量、质押笔数、质押总股数、质押总市值、沪深300指数等信息，支持沪深京股票 |

## 请求参数

本接口无需任何请求参数。

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> pledge-summary
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

接口直接返回数组，**不含分页信息**。

```json
[
    {
        "trade_date": "2025-09-30",
        "pledge_total_ratio": 0,
        "pledge_company_count": 1234,
        "pledge_deal_count": 5678,
        "pledge_total_shares": 1234567890000.0,
        "pledge_total_market_value": 98765432100000.0,
        "hs300_index": 3456.78,
        "hs300_week_change_ratio": 2.34
    }
]
```

### PledgeMarketSummary 字段说明

| 字段名                    | 类型   | 是否可为空 | 说明                                      | 单位 |
|---------------------------|--------|------------|-------------------------------------------|------|
| trade_date                | String | 否         | 报告日期，固定格式为 YYYY-MM-DD            | -    |
| pledge_total_ratio        | float  | 否         | A 股质押总比例，当前返回 0                 | %    |
| pledge_company_count      | int    | 否         | 质押公司数量（有质押的上市公司数量）        | 家   |
| pledge_deal_count         | int    | 否         | 质押笔数（所有质押交易的总笔数）            | 笔   |
| pledge_total_shares       | float  | 否         | 质押总股数（所有质押股票的总股数）          | 股   |
| pledge_total_market_value | float  | 否         | 质押总市值（所有质押股票的总市值）          | 元   |
| hs300_index               | float  | 否         | 沪深300指数（报告日期的沪深300指数收盘价）  | -    |
| hs300_week_change_ratio   | float  | 否         | 沪深300周涨跌幅（与一周前对比的涨跌幅）     | %    |

## 注意事项

- 本接口无需任何参数，直接请求即可
- 返回值为**数组**，不含 `items` / `total_pages` / `total_items` 等分页包装
- `pledge_total_ratio` 当前接口固定返回 `0`
- `pledge_total_shares` 和 `pledge_total_market_value` 原始接口以字符串返回，handler 已转为数值输出
