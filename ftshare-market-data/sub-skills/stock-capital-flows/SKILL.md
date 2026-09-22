---
name: stock-capital-flows
description: 查询 A 股股票资金流向（主力净流入）。支持当前实时快照，或指定日期的 15 分钟切片快照（默认日终 time=1530）。Use when user asks about 资金流向, 主力净流入, 超大单/大单/中单/小单净流入, 15分钟资金流, 个股资金流排名, capital flow, money flow, stock capital flows.
---

# 查询 A 股股票资金流向（实时快照 / 15 分钟切片）

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询股票资金流向 |
| 外部接口 | GET /api/v1/market/data/stock-capital-flows |
| 请求方式 | GET |
| 适用场景 | 分页查询 A 股股票资金流向；不传 `date` 返回当前实时快照，传入 `date` 可指定 15 分钟切片（默认 `time=1530` 日终）。仅返回 A 股（不含 ETF/指数），按主力净流入降序排列。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| date | string | 否 | 查询日期 | 20260616 | 格式 YYYYMMDD；不传=实时快照 |
| time | string | 否 | 15 分钟切片时刻 | 1530 | 格式 HHMM，分钟须为 00/15/30/45；仅与 `date` 同时有效，默认 1530（日终） |
| symbol | string | 否 | 只查指定标的 | 601138.SH | 外部格式（如 `601138.SH`）；逐页扫描定位，找到即停，返回其全市场排名与单条记录。不传则按分页/全量返回 |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 50 | 默认 50 |

## 执行方式

```bash
# 当前实时快照（分页）
python scripts/handler.py --page 1 --page-size 50
# 历史 15 分钟切片（默认 time=1530 日终）
python scripts/handler.py --date 20260616 --page 1 --page-size 50
# 指定切片时刻（如 10:15）
python scripts/handler.py --date 20260616 --time 1015 --page 1 --page-size 50
# 全量自动翻页拉取某日日终资金流
python scripts/handler.py --date 20260616 --all
# 只查某只票某切片（逐页定位，返回排名+记录）
python scripts/handler.py --date 20260616 --symbol 601138.SH
# 只查某只票当前实时快照
python scripts/handler.py --symbol 601138.SH
```

## 响应结构

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 50,
    "total": 5209,
    "pages": 105,
    "records": [
      {
        "net_inflow_extra_large": "123456789.0000",
        "net_inflow_large": "98765432.1000",
        "net_inflow_main": "222222221.1000",
        "net_inflow_medium": "-50000000.0000",
        "net_inflow_small": "-172222221.1000",
        "symbol": "600000.SH",
        "symbol_name": "浦发银行",
        "ts_nanos": 1747037400000000000
      }
    ]
  }
}
```

`--symbol` 模式输出为定位结果：`{"found": bool, "symbol": str, "rank": int|null, "total_items": int, "record": {...}}`。

### 字段说明（CapitalFlowResponse）

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| net_inflow_extra_large | string | 否 | 超大单净流入，单位元 |
| net_inflow_large | string | 否 | 大单净流入，单位元 |
| net_inflow_main | string | 否 | 主力净流入，单位元；公式 = 超大单净流入 + 大单净流入 |
| net_inflow_medium | string | 否 | 中单净流入，单位元 |
| net_inflow_small | string | 否 | 小单净流入，单位元 |
| symbol | string | 否 | 标的代码，外部格式如 `600000.SH`、`000001.SZ` |
| symbol_name | string | 是 | 标的名称 |
| ts_nanos | int | 否 | 快照时间戳（纳秒） |

## 注意事项

- 不传 `date`：返回当前实时资金流向快照。
- 传入 `date`：返回该日指定 15 分钟切片快照，默认 `time=1530`（日终）；`time` 分钟须为 00/15/30/45。
- 金额字段在 JSON 中以字符串形式返回（Decimal 序列化），单位元。
- `symbol` 为外部代码格式（如 `600000.SH`）。
- 仅返回 A 股股票（不含 ETF、指数等）；列表按 `net_inflow_main` 降序排列。
- 本接口响应带短期缓存（失败重试策略约 5 秒），相同 query 在缓存有效期内可能返回相同结果。
- `--all` 自动翻页拉取全量；全市场约 5000+ 条，按需使用以免响应过大。

## 调用示例

```bash
python <RUN_PY> stock-capital-flows --symbol 600519.SH
```
