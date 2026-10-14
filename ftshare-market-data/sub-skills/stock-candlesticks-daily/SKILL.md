---
name: stock-candlesticks-daily
description: "查询股票日K快照。当用户需要某个交易日全部普通 A 股的日 K（开高低收、成交量额、换手率），或要对某日全市场做横截面分析时使用。"
---

# 查询股票日K快照

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 股票日K快照 |
| 外部接口 | `/api/v1/market/data/stock-candlesticks-daily` |
| 请求方式 | GET |
| 适用场景 | 查询指定交易日全部普通 A 股的日 K 快照，用于全市场横截面分析 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `trade_date` | string | 是 | 交易日 | `20261008` | 格式 `YYYYMMDD`，必须是交易日 |
| `page` | integer | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `page_size` | integer | 否 | 每页数量 | `200` | 默认 200，最大 500 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 取当日日 K 快照第一页
python <RUN_PY> stock-candlesticks-daily --trade_date 20261008

# 指定分页
python <RUN_PY> stock-candlesticks-daily --trade_date 20261008 --page 1 --page_size 500

# 自动翻页取全市场当日日 K
python <RUN_PY> stock-candlesticks-daily --trade_date 20261008 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "pageNum": 1,
        "pageSize": 200,
        "total": 5400,
        "pages": 27,
        "records": [
            {
                "trade_code": "000001.SZ",
                "open": "11.5700",
                "high": "11.8700",
                "low": "11.5400",
                "close": "11.7800",
                "ts_millis": 1791442800000,
                "ts_millis_open": 1791423000000,
                "turnover": "1743402510.4000",
                "volume": 148168594,
                "turnover_rate": 0.00763531893198915
            }
        ]
    }
}
```

### 字段说明

`data` 为分页对象，含 `pageNum`、`pageSize`、`total`、`pages` 与 `records`。

### records 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `trade_code` | String | 否 | 标的代码，带标准市场后缀，如 `600519.SH`、`000001.SZ`、`920001.BJ` |
| `open` | String | 否 | 开盘价（元） |
| `high` | String | 否 | 最高价（元） |
| `low` | String | 否 | 最低价（元） |
| `close` | String | 否 | 收盘价（元） |
| `ts_millis` | Integer | 否 | 收盘时间戳（毫秒） |
| `ts_millis_open` | Integer | 否 | 开盘时间戳（毫秒） |
| `turnover` | String | 否 | 成交额（元） |
| `volume` | Integer | 否 | 成交量（股） |
| `turnover_rate` | Number | 否 | 换手率比例值；如 `0.0076353189` 表示约 0.7635% |

## 注意事项

- 仅覆盖普通 A 股日 K，不含 ETF、可转债、指数等其他标的类型。
- 分页返回，默认 `page=1`、`page_size=200`，`page_size` 最大 500；`page` 传 0 或负数会返回参数错误。
- `turnover_rate` 是比例值而非百分数，展示时需乘以 100。
