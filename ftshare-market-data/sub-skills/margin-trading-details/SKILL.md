---
name: margin-trading-details
description: "获取融资融券明细。当用户需要获取 A 股融资融券明细列表（按交易日快照），支持单日、区间或标的过滤查询，或了解融资融券明细时使用。"
---

# 获取融资融券明细

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 获取融资融券明细（margin_trading_details） |
| 外部接口 | `/api/v1/market/data/margin-trading-details` |
| 请求方式 | GET |
| 适用场景 | 按交易日查询 A 股两融快照（每标的一行）：单日查询、指定标的的交易日区间查询、默认前一交易日快照 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `--date` | str | 否 | 单日查询日期 | `20260623` | 格式 `YYYYMMDD`，必须为交易日；不传返回前一交易日快照 |
| `--start-date` | str | 否 | 区间查询开始日期 | `20260601` | 须与 `--end-date`、`--stock` **同时提供**；跨度不超过 3 年 |
| `--end-date` | str | 否 | 区间查询结束日期 | `20260623` | 须与 `--start-date`、`--stock` 同时提供；开始须早于结束 |
| `--stock` | str | 否 | 标的代码过滤 | `600000.SH` | 单日/默认查询时可选；区间查询时必填 |
| `--page` | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| `--page_size` | int | 否 | 每页记录数 | `20` | 默认 20，最大 1000 |
| `--all` | - | 否 | 自动翻页获取全量数据 | - | 合并 `data.records` 输出 |

## 执行方式

```bash
# 默认：前一交易日快照
python <RUN_PY> margin-trading-details --page 1 --page_size 20

# 指定交易日
python <RUN_PY> margin-trading-details --date 20260623 --page 1 --page_size 20

# 单日 + 标的过滤
python <RUN_PY> margin-trading-details --date 20260623 --stock 600000.SH

# 区间查询：start_date、end_date、stock 必须同时提供
python <RUN_PY> margin-trading-details --start-date 20260601 --end-date 20260623 --stock 600000.SH

# 自动翻页获取全量数据
python <RUN_PY> margin-trading-details --date 20260623 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

外层为 `code`（成功 200）/ `message` / `data`；分页信息与记录位于 `data`：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "pageNum": 1,
        "pageSize": 20,
        "total": 4443,
        "pages": 223,
        "records": [
            {
                "date": "2026-06-16",
                "margin_trading_balance": 13197538116,
                "margin_trading_buying_amount": 3827217410,
                "margin_trading_repayment_amount": 874371294,
                "securities_lending_balance_volume": 143377,
                "securities_lending_repayment_volume": 25800,
                "securities_lending_selling_volume": 34500,
                "total_balance": 13233247592,
                "symbol": "002384.SZ",
                "symbol_name": "合力泰"
            }
        ]
    }
}
```

### records 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `date` | String | 否 | 交易日期，格式 `YYYY-MM-DD` | - |
| `symbol` | String | 否 | 标的代码，短市场后缀（`600000.SH`、`000001.SZ`、`920178.BJ`） | - |
| `symbol_name` | String | 是 | 标的名称 | - |
| `margin_trading_balance` | int | 是 | 融资余额 | 元 |
| `margin_trading_buying_amount` | int | 是 | 融资买入额 | 元 |
| `margin_trading_repayment_amount` | int | 是 | 融资偿还额 | 元 |
| `securities_lending_balance_volume` | int | 是 | 融券余量 | 股 |
| `securities_lending_repayment_volume` | number | 是 | 融券偿还量 | 股 |
| `securities_lending_selling_volume` | int | 是 | 融券卖出量 | 股 |
| `total_balance` | int | 是 | 融资融券余额 | 元 |

## 注意事项

- `--date` 不能与 `--start-date`/`--end-date` 同时使用；区间查询必须三参数（含 `--stock`）齐全，否则本地校验直接退出。
- 区间包含首尾交易日，自动忽略非交易日；跨度不能超过 3 年。
- `--stock` 支持与响应代码等价的格式（`600000.SH`、`600000.XSHG`、`600000`）；响应 `symbol` 统一为短市场后缀。
- 金额字段单位为**元**，量字段单位为**股**，无值时为 `null`。
- 如需全量数据，使用 `--all` 自动翻页合并，或按 `--page` 递增循环至 `data.pages`。
