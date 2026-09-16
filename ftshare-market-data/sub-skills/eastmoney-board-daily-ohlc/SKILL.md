---
name: eastmoney-board-daily-ohlc
description: "查询东财单板块历史 OHLC。当用户需要查询指定东财板块历史 OHLC 数据，支持日期范围过滤与分页，或了解东财单板块历史 OHLC时使用。"
---

# 查询东财单板块历史 OHLC

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财单板块历史 OHLC |
| 外部接口 | `/api/v1/market/data/eastmoney-board-daily-ohlc` |
| 请求方式 | GET |
| 适用场景 | 查询指定东财板块历史 OHLC 数据，支持日期范围过滤与分页 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `board_code` | string | 是 | 板块代码 | `BK1024` | BK 前缀 |
| `start_date` | string | 否 | 起始日期（含） | `2021-01-01` | 格式 `YYYY-MM-DD` 或 `YYYYMMDD`；不传则从最早开始 |
| `end_date` | string | 否 | 截止日期（含） | `2021-12-31` | 格式 `YYYY-MM-DD` 或 `YYYYMMDD`；不传则到最晚为止 |
| `page` | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| `page_size` | int | 否 | 每页记录数 | `20` | 默认 50 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 查询板块全部历史 OHLC
python <RUN_PY> eastmoney-board-daily-ohlc --board_code BK1024 --page 1 --page_size 20

# 指定日期范围
python <RUN_PY> eastmoney-board-daily-ohlc --board_code BK1024 --start_date 2021-01-01 --end_date 2021-12-31 --page 1 --page_size 20

# 自动翻页获取全量数据
python <RUN_PY> eastmoney-board-daily-ohlc --board_code BK1024 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "items": [
        {
            "board_code": "BK1024",
            "board_name": "绿色电力",
            "market": "90",
            "date": "2021-10-18",
            "open": "1001.53",
            "close": "1037.67",
            "high": "1041.82",
            "low": "1001.53",
            "volume": "52669555",
            "turnover": "43012845568",
            "amplitude": "4.03",
            "change_rate": "3.77",
            "change": "37.67",
            "turnover_rate": "1.03"
        }
    ],
    "total_pages": 1,
    "total_items": 1
}
```

### 顶层字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `items` | Array | 否 | 当前页 OHLC 数据列表 |
| `total_pages` | int | 否 | 总页数 |
| `total_items` | int | 否 | 总记录数 |

### items 元素字段说明（BoardDailyOhlc）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `board_code` | String | 否 | 板块代码 | - |
| `board_name` | String | 否 | 板块名称 | - |
| `market` | String | 否 | 市场编码 | - |
| `date` | String | 否 | 交易日期，格式 `YYYY-MM-DD` | - |
| `open` | String | 否 | 开盘价 | - |
| `close` | String | 否 | 收盘价 | - |
| `high` | String | 否 | 最高价 | - |
| `low` | String | 否 | 最低价 | - |
| `volume` | String | 否 | 成交量 | 股 |
| `turnover` | String | 否 | 成交额 | 元 |
| `amplitude` | String | 否 | 振幅 | % |
| `change_rate` | String | 否 | 涨跌幅 | % |
| `change` | String | 否 | 涨跌额 | - |
| `turnover_rate` | String | 否 | 换手率 | % |

## 注意事项

- `board_code` 为必填参数，可通过 `eastmoney-concept-boards` 获取板块代码
- 历史 OHLC 中多数数值字段以字符串返回
- 板块代码对行业板块和概念板块通用
