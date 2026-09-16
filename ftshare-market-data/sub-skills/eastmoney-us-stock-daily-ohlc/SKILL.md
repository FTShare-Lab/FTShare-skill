---
name: eastmoney-us-stock-daily-ohlc
description: "查询东财美股历史日 K 线。当用户需要查询东财美股历史日 K 线；有日期范围时按 3 天窗口分批请求，无日期范围时全量拉取，或了解东财美股历史 OHLC、东财美股历史日 K 线时使用。"
---

# 查询东财美股历史 OHLC

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财美股历史日 K 线 |
| 外部接口 | `/api/v1/market/data/eastmoney-us-stock-daily-ohlc` |
| 请求方式 | GET |
| 适用场景 | 查询东财美股历史日 K 线；有日期范围时按 3 天窗口分批请求，无日期范围时全量拉取 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| `--stock_code` | string | 是 | 股票代码 | `AAL` | 东财美股代码 |
| `--start_date` | string | 否 | 起始日期（含） | `2026-06-01` | 格式 `YYYY-MM-DD` 或 `YYYYMMDD` |
| `--end_date` | string | 否 | 截止日期（含） | `2026-06-10` | 格式 `YYYY-MM-DD` 或 `YYYYMMDD` |
| `--page` | int | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `--page_size` | int | 否 | 每页条数 | `50` | 默认 50 |
| `--all` | flag | 否 | 全量返回 | — | 返回全量数据（不分页） |

> **执行策略**：有日期范围时，将区间拆分为最多 3 天的窗口分批请求，合并去重排序；无日期范围时全量拉取（不传日期参数）。

### 查询模式

| 模式 | 参数 | 说明 |
|------|------|------|
| 全部历史 | `--stock_code` | 全量拉取全部历史 K 线（分页） |
| 日期区间 | `--stock_code --start_date --end_date` | 按 3 天窗口分批请求，合并后分页 |
| 日期区间全量 | `--stock_code --start_date --end_date --all` | 按 3 天窗口分批请求，合并后返回全量（不分页） |

## 执行方式

通过根目录的 `run.py` 调用：

```bash
python <RUN_PY> eastmoney-us-stock-daily-ohlc --stock_code AAL --page 1 --page_size 10
python <RUN_PY> eastmoney-us-stock-daily-ohlc --stock_code AAL --start_date 2026-05-01 --end_date 2026-06-10 --page 1 --page_size 50
python <RUN_PY> eastmoney-us-stock-daily-ohlc --stock_code AAL --start_date 2026-05-01 --end_date 2026-06-10 --all
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
| `data.records` | array | 当前页 K 线列表 |

`data.records[]` 单条记录字段（**全部字段按字符串返回**）：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `secid` | string | 证券 ID，格式 `{market}.{code}`，如 `105.ADV` |
| `code` | string | 股票代码 |
| `name` | string | 股票名称 |
| `market` | string | 市场编号 |
| `date` | string | 日期，格式 `YYYY-MM-DD` |
| `open` | string | 开盘价 |
| `close` | string | 收盘价 |
| `high` | string | 最高价 |
| `low` | string | 最低价 |
| `volume` | string | 成交量 |
| `amount` | string | 成交额 |
| `amplitude` | string | 振幅 |
| `klt` | string | K 线类型 |
| `fqt` | string | 复权类型 |

### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 50,
    "total": 503,
    "pages": 11,
    "records": [
      {
        "secid": "105.ADV",
        "code": "ADV",
        "name": "Advantage Solutions Inc",
        "market": "105",
        "date": "2021-01-05",
        "open": "12.34",
        "close": "12.56",
        "high": "12.78",
        "low": "12.10",
        "volume": "1234567",
        "amount": "9876543.21",
        "amplitude": "5.5",
        "klt": "101",
        "fqt": "1"
      }
    ]
  }
}
```

## 注意事项

- 有日期范围时，区间拆分为最多 3 天的窗口分别请求，避免服务端大范围 500 错误
- 无日期范围时，全量拉取全部历史 K 线（单只股票数据量较小，如 AAL ~1365 条）
- `start_date` / `end_date` 支持 `YYYY-MM-DD` 与 `YYYYMMDD` 两种格式
- 记录字段为 snake_case，所有数值字段均为字符串
- `data` 在错误或无数据时可能为 `null`
- `stock_code` 为东财美股代码（如 `AAL`）
- 可先通过 `eastmoney-us-stock-list` 获取有效的美股代码列表
