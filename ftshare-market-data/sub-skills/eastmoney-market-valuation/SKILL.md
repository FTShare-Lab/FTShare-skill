---
name: eastmoney-market-valuation
description: "查询东财市场日估值。当用户需要查询 A 股主要市场指数（上证指数、沪深300、深证成指、创业板指、科创50、北证50）的每日估值数据，包括市盈率、总市值、流通市值、收盘点位等；支持单日、区间查询，或了解东财市场日估值时使用。"
---

# 查询东财市场日估值

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财市场日估值 |
| 外部接口 | `/api/v1/market/data/eastmoney-market-valuation` |
| 请求方式 | GET |
| 适用场景 | 查询 A 股主要市场指数（上证指数、沪深300、深证成指、创业板指、科创50、北证50）的每日估值数据，包括市盈率、总市值、流通市值、收盘点位等；支持单日、区间查询 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| `market_code` | string | 否 | 市场代码 | `000300` | 000001=上证指数, 000300=沪深300, 399001=深证成指, 399006=创业板指, 000688=科创50, 899050=北证50 |
| `trade_date` | string | 否 | 交易日 | `2026-06-08` | 格式 `YYYY-MM-DD`；与 `start_date`/`end_date` 互斥 |
| `start_date` | string | 否 | 区间起始日 | `2026-06-01` | 格式 `YYYY-MM-DD`；与 `end_date` 同时提供 |
| `end_date` | string | 否 | 区间结束日 | `2026-06-09` | 格式 `YYYY-MM-DD`；与 `start_date` 同时提供 |
| `--page` | int | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `--page_size` | int | 否 | 每页条数 | `50` | 默认 50，最大 500 |

### 查询模式

| 模式 | 参数 | 说明 |
|------|------|------|
| 全量查询 | 无 | 返回全部市场全部日期估值 |
| 单市场全部历史 | `--market_code` | 返回指定市场全部历史估值 |
| 单日全市场 | `--trade_date` | 返回指定交易日全部市场估值 |
| 单市场单日 | `--market_code --trade_date` | 返回指定市场指定交易日估值 |
| 单市场区间 | `--market_code --start_date --end_date` | 返回指定市场日期区间估值 |

## 执行方式

通过根目录的 `run.py` 调用：

```bash
python <RUN_PY> eastmoney-market-valuation --market_code 000300 --page 1 --page_size 10
python <RUN_PY> eastmoney-market-valuation --market_code 000001 --start_date 2026-06-01 --end_date 2026-06-09
python <RUN_PY> eastmoney-market-valuation --start_date 2026-06-01 --end_date 2026-06-09 --page 1 --page_size 50
python <RUN_PY> eastmoney-market-valuation --market_code 000300 --trade_date 2026-06-08
python <RUN_PY> eastmoney-market-valuation --start_date 2026-06-01 --end_date 2026-06-09 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

顶层为分页包装对象：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `code` | int | 业务状态码，成功为 `0` |
| `message` | string | 业务消息 |
| `data` | object/null | 分页数据体；无数据时可能为 `null` |
| `data.pageNum` | int | 当前页码 |
| `data.pageSize` | int | 每页条数 |
| `data.total` | int | 总记录数 |
| `data.pages` | int | 总页数 |
| `data.records` | array | 当前页记录列表 |

`data.records` 中每项字段：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `market_code` | string | 市场代码，如 `000001`=上证指数 |
| `market_name` | string | 市场名称，如 `上证指数` |
| `trade_date` | string | 交易日期，格式 `YYYY-MM-DD` |
| `pe_ttm` | string | 市盈率 TTM，无数据时为空 |
| `total_shares` | string | 总股本，无数据时为空 |
| `free_shares` | string | 流通股本，无数据时为空 |
| `trade_market_value` | string | 市场总市值（元），无数据时为空 |
| `free_market_cap` | string | 流通市值（元），无数据时为空 |
| `listing_org_num` | string | 上市公司家数，无数据时为空 |
| `close_price` | string | 收盘点位，无数据时为空 |
| `change_rate` | string | 涨跌幅（%），无数据时为空 |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 3,
    "total": 36,
    "pages": 12,
    "records": [
      {
        "market_code": "000001",
        "market_name": "上证指数",
        "trade_date": "2026-06-08",
        "pe_ttm": "13.95",
        "total_shares": "484989600",
        "free_shares": "462381100",
        "trade_market_value": "5276746800",
        "free_market_cap": "5065018100",
        "listing_org_num": "1708",
        "close_price": "3959.3378",
        "change_rate": "-1.6982"
      }
    ]
  }
}
```

## 注意事项

- 覆盖 6 个 A 股主要市场指数
- 市场代码参考：上证指数(000001)、沪深300(000300)、深证成指(399001)、创业板指(399006)、科创50(000688)、北证50(899050)
- 所有数值字段序列化为字符串，避免 JSON 浮点精度问题
- 无数据的字段输出为空字符串 `""`，而非 `null`
- 推荐使用 `YYYY-MM-DD` 日期格式；`YYYYMMDD` 会返回空列表
- 当前单日查询可能异常，建议优先使用区间查询
