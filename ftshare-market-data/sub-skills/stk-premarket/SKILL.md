---
name: stk-premarket
description: "查询盘前数据（每日股本、昨收、涨跌停价、价格与总市值 / 流通市值）。适用于\"某只股票某天的总股本 / 流通股本\"\"历史股本是多少\"\"某日全市场盘前快照\"\"涨跌停价和总市值\"这类问题；接口 GET /api/v2/market/data/stk-premarket。"
---

# 盘前数据

接口：`GET /api/v2/market/data/stk-premarket`
在线文档：<https://market.ft.tech/gateway/doc/pages/q1zs7bsw.md>

返回每个标的每个交易日的总股本、A 股流通股本、昨收、涨跌停价、价格（当日为预测开盘价、历史为收盘价）及据此计算的总市值与流通市值。

## 查询模式

1. **单日全市场**：`--trade-date 20261113`（约 5500+ 只，需翻页）
2. **单票历史区间**：`--ts-code 600036.SH --start-date 20250101 --end-date 20261116`
3. **单票最新一天**：只传 `--ts-code`（等价于该标的最新交易日 1 条）

`--trade-date` 与 `--start-date/--end-date` **互斥**；`--start-date/--end-date` 必须**成对**且配合 `--ts-code`。

## 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `--ts-code` | string | N | 标的代码，如 `000001.SZ` / `600519.SH`。只传本参数时仅返回最新交易日 1 条 |
| `--trade-date` | int | N | 交易日 `YYYYMMDD`，查该日全市场；非交易日返回空数组 |
| `--start-date` | int | N | 区间起始日 `YYYYMMDD`，须与 `--end-date` 成对、并配合 `--ts-code` |
| `--end-date` | int | N | 区间结束日 `YYYYMMDD` |
| `--page` | int | N | 页码，默认 1 |
| `--page-size` | int | N | 每页条数，默认 50、最大 500；配合 `--all` 时默认 500 |
| `--all` | flag | N | 按 `total_pages` 自动翻页并合并 `items`（单票全历史推荐） |

## 分页（关键）

- 响应信封：`{"code":200,"message":"success","data":{"items":[...],"total_items":N,"total_pages":P}}`。
- `total_pages = ceil(total_items / page_size)`，**依赖 page_size**：同一区间 `page_size=50` 与 `500` 的页数不同。
- 默认只返回第 1 页（50 条），按 `trade_date` 升序 —— 单次请求看到的是**最早** 50 个交易日，最容易被误判成"历史只到某月"。
- 取全量：加 `--all`，或自行循环 `--page` 到 `total_pages`。

## 已知边界（实测）

| 场景 | 行为 |
|---|---|
| 只传 `--ts-code` | 最新交易日 1 条；代码无效/无数据返回空数组（如旧北交所 `830799.BJ`） |
| 历史起点 | `2022-01-04`；`2022` 以前无数据，跨起点区间**静默截断**（`2021-12-01~2022-06-30` 返回 117 条，从 `20220104` 起，不报错） |
| 非交易日 `--trade-date` | `200` + `items: []`、`total_items: 0` |
| `--start-date` 或 `--end-date` 单独给 | 本地拦截；服务端 400 `start_date and end_date must be provided together` |
| `--trade-date` 与区间同给 | 本地拦截；服务端 400 `trade_date cannot be used with start_date/end_date` |
| 区间不配 `--ts-code` | 本地拦截；服务端 400 `start_date/end_date must be used with ts_code` |
| `page_size` 越界（0 / 501 / 1000） | 400 `page_size must be between 1 and 500` |
| `page=0` | 400 `page must be greater than 0` |
| 页码超出末页 | `200` + `items: []`，总数照常返回 |
| 日期格式 | 必须 `YYYYMMDD`，`YYYY-MM-DD` 返回 400 |
| 北交所代码 | 已统一为 `92xxxx`（如 `920002.BJ`）；旧 `43xxxx` / `83xxxx` 返回空 |

## 字段

| 字段 | 说明 |
|---|---|
| `trade_date` | 交易日 `YYYYMMDD`（int） |
| `ts_code` | 标的代码 |
| `totshare_num` | 总股本（股，string） |
| `ashare_circ_num` | A 股流通股本（股，string） |
| `pre_close` / `up_limit` / `down_limit` | 昨收 / 涨停价 / 跌停价 |
| `price` | 当日为预测开盘价，历史为收盘价 |
| `total_mv` | 总市值 = `totshare_num × price` |
| `float_mv` | 流通市值 = `ashare_circ_num × price` |

## 示例

```bash
# 单票全历史（452 条，一次拉全）
python <RUN_PY> stk-premarket --ts-code 600036.SH --start-date 20250101 --end-date 20261116 --all

# 该标的最新一天
python <RUN_PY> stk-premarket --ts-code 600036.SH

# 单日全市场（12 页 5580 只）
python <RUN_PY> stk-premarket --trade-date 20261116 --page-size 500 --all
```

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，通过请求头 `FTSHARE_API_KEY` 发送；缺少凭据时不会发起请求。
