---
name: pledge-detail
description: "查询单票股权质押个股详细信息。当用户需要获取 A 股上市公司单只股票所有报告期的股权质押详细信息，支持沪深京股票，支持分页查询，或了解单票股权质押个股详细信息时使用。"
---

# 查询单票股权质押个股详细信息

## 接口说明

| 项目     | 说明                                                                              |
|----------|-----------------------------------------------------------------------------------|
| 接口名称 | 查询单票股权质押个股详细信息                                                      |
| 外部接口 | `/api/v1/market/data/pledge/pledge-detail`                                   |
| 请求方式 | GET                                                                               |
| 适用场景 | 获取 A 股上市公司单只股票所有报告期的股权质押详细信息，支持沪深京股票，支持分页查询 |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述            | 取值示例  | 备注                                                                                     |
|------------|--------|----------|-----------------|-----------|------------------------------------------------------------------------------------------|
| stock_code | string | 是       | 单个股票代码    | 603323.SH | 支持沪深京股票，A股需为6位数字+后缀（SH=上交所，SZ=深交所，BJ=北交所），单次仅支持一个代码 |
| page       | int    | 否       | 页码，从 1 开始 | 1         | 默认值为 1，必须大于等于 1                                                               |
| page_size  | int    | 否       | 每页记录数      | 50        | 默认值为 50，必须大于等于 1                                                              |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> pledge-detail --stock_code 603323.SH
python <RUN_PY> pledge-detail --stock_code 603323.SH --page 2 --page_size 20
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

接口返回带分页信息的对象：

```json
{
    "items": [
        {
            "trade_code": "603323.SH",
            "stock_name": "苏农银行",
            "report_date": "2025-09-30",
            "pledge_ratio": 12.34,
            "pledge_n": 5,
            "pledge_market_value": 98765432.0,
            "pledge_unlimitn": 1234.56,
            "pledge_limitn": 0.0,
            "last_year_fluctuation": -5.67
        }
    ],
    "total_pages": 1,
    "total_items": 21
}
```

### PledgeStockHolder 字段说明

| 字段名                | 类型   | 是否可为空 | 说明                                                                   | 单位 |
|-----------------------|--------|------------|------------------------------------------------------------------------|------|
| trade_code            | String | 否         | 股票交易代码，固定携带 .SZ/.SH/.BJ 市场后缀                             | -    |
| stock_name            | String | 否         | 上市公司对应股票名称                                                   | -    |
| report_date           | String | 否         | 报告日期，固定格式为 YYYY-MM-DD                                         | -    |
| pledge_ratio          | float  | 否         | 质押比例                                                               | %    |
| pledge_n              | int    | 否         | 质押笔数                                                               | 笔   |
| pledge_market_value   | float  | 否         | 质押市值（质押股数 × 报告日期收盘价）                                    | 元   |
| pledge_unlimitn       | float  | 否         | 质押无限售股数                                                         | 万股 |
| pledge_limitn         | float  | 否         | 质押限售股数                                                           | 万股 |
| last_year_fluctuation | float  | 是         | 较上年变动（报告日期收盘价与一年前收盘价的涨跌幅），无上年数据时返回 null | %    |

## 注意事项

- `stock_code` 为必填参数，单次请求只支持一个股票代码
- 分页参数 `page` 和 `page_size` 均为可选，默认 `page=1`、`page_size=50`
- 返回值包含 `items`、`total_pages`、`total_items` 分页包装
- `last_year_fluctuation` 可为 null（无上年数据时）
