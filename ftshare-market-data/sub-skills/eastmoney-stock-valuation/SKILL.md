---
name: eastmoney-stock-valuation
description: "查询东财个股日估值。当用户需要查询全部 A 股个股的每日估值数据，包括市盈率（TTM/LYR）、市净率、市现率、市销率、PEG、总市值、流通市值、收盘价等；支持单票单日、单票历史区间及全市场查询，或了解东财个股日估值时使用。"
---

# 查询东财个股日估值

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财个股日估值 |
| 外部接口 | `/api/v1/market/data/eastmoney-stock-valuation` |
| 请求方式 | GET |
| 适用场景 | 查询全部 A 股个股的每日估值数据，包括市盈率（TTM/LYR）、市净率、市现率、市销率、PEG、总市值、流通市值、收盘价等；支持单票单日、单票历史区间及全市场查询 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| `symbol` | string | 否 | 股票代码 | `000001` | 6位数字代码，不传返回全部股票 |
| `trade_date` | string | 否 | 交易日 | `2026-06-08` | 格式 `YYYY-MM-DD`；与 `start_date`/`end_date` 互斥 |
| `start_date` | string | 否 | 区间起始日 | `2026-06-01` | 格式 `YYYY-MM-DD`；与 `end_date` 同时提供 |
| `end_date` | string | 否 | 区间结束日 | `2026-06-09` | 格式 `YYYY-MM-DD`；与 `start_date` 同时提供 |
| `--page` | int | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `--page_size` | int | 否 | 每页条数 | `50` | 默认 50，最大 500 |

### 查询模式

| 模式 | 参数 | 说明 |
|------|------|------|
| 全量查询 | 无 | 返回全部股票全部日期（⚠️ 数据量极大，建议配合分页） |
| 单票全部历史 | `--symbol` | 返回指定股票全部历史估值 |
| 单日全市场 | `--trade_date` | 返回指定交易日全部股票估值 |
| 单票单日 | `--symbol --trade_date` | 返回指定股票指定交易日估值 |
| 单票历史区间 | `--symbol --start_date --end_date` | 返回指定股票日期区间估值走势 |

## 执行方式

通过根目录的 `run.py` 调用：

```bash
python <RUN_PY> eastmoney-stock-valuation --symbol 000001 --page 1 --page_size 10
python <RUN_PY> eastmoney-stock-valuation --symbol 000001 --start_date 2026-06-01 --end_date 2026-06-09
python <RUN_PY> eastmoney-stock-valuation --start_date 2026-06-01 --end_date 2026-06-09 --page 1 --page_size 50
python <RUN_PY> eastmoney-stock-valuation --symbol 000001 --trade_date 2026-06-08
python <RUN_PY> eastmoney-stock-valuation --start_date 2026-06-01 --end_date 2026-06-09 --all
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
| `stock_code` | string | 股票代码，如 `000001` |
| `stock_name` | string | 股票简称，如 `平安银行` |
| `trade_date` | string | 交易日期，格式 `YYYY-MM-DD` |
| `pe_ttm` | string | 市盈率 TTM，无数据时为空 |
| `pe_lar` | string | 市盈率 LYR（静态），无数据时为空 |
| `pb_mrq` | string | 市净率 MRQ，无数据时为空 |
| `pcf_ocf_ttm` | string | 市现率 TTM，无数据时为空 |
| `pcf_ocf_lar` | string | 市现率 LYR，无数据时为空 |
| `ps_ttm` | string | 市销率 TTM，无数据时为空 |
| `peg_car` | string | PEG 指标，无数据时为空 |
| `total_market_cap` | string | 总市值（元），无数据时为空 |
| `notlimited_marketcap_a` | string | 流通市值（元），无数据时为空 |
| `close_price` | string | 收盘价（元/股），无数据时为空 |
| `change_rate` | string | 涨跌幅（%），无数据时为空 |
| `total_shares` | string | 总股本，无数据时为空 |
| `free_shares_a` | string | 流通股本，无数据时为空 |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 3,
    "total": 33142,
    "pages": 11048,
    "records": [
      {
        "stock_code": "000001",
        "stock_name": "平安银行",
        "trade_date": "2026-06-08",
        "pe_ttm": "4.9709",
        "pe_lar": "5.0207",
        "pb_mrq": "0.4612",
        "pcf_ocf_ttm": "1.1223",
        "pcf_ocf_lar": "0.6777",
        "ps_ttm": "1.6093",
        "peg_car": "-1.1934",
        "total_market_cap": "214047277723.94",
        "notlimited_marketcap_a": "214043775202.59",
        "close_price": "11.03",
        "change_rate": "0.4554",
        "total_shares": "19405918198",
        "free_shares_a": "19405600653"
      }
    ]
  }
}
```

## 注意事项

- 所有数值字段序列化为字符串，避免 JSON 浮点精度问题
- 无数据的字段输出为空字符串 `""`，而非 `null`
- 部分估值指标（如 PEG、市现率 LYR）可能因财务数据缺失而为空
- 负值指标（如负市盈率）会正常返回负数字符串
- 推荐使用 `YYYY-MM-DD` 日期格式；`YYYYMMDD` 会返回空列表
- 当前单日查询可能异常，建议优先使用区间查询
