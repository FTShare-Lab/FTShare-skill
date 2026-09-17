---
name: stock-intraday
description: 股票跨日分时行情，含均价与日累计量额（stock_intraday，GET /api/v4/market/data/stock-intraday）。用户问某只股票的分时数据、当日/近五日逐分钟价格与均价、日累计成交量额时使用。必填 --symbol；可选 --range、--days、--ts-ms，三者按 ts_ms > days > range 优先级生效。
---

# 股票跨日分时行情

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 股票跨日分时行情（stock_intraday） |
| 外部接口 | `GET /api/v4/market/data/stock-intraday` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 查询单只股票的分钟分时价格、均价及日累计成交量额；支持当日实时分时与近期历史分时合并返回 |
| 数据范围 | 当日及近期历史交易日，时间范围按北京时间（Asia/Shanghai）计算 |
| 单次限量 | 单只股票；`days` 为 1～5；无分页，返回所选范围内的可用数据点 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| symbol | string | 是 | 股票代码（需带市场后缀） | 600000.SH | 不接受裸代码；也接受 `600000.XSHG` 等 MIC 后缀 |
| range | string | 否 | 预置区间 | Today | `Today`（当日）/`FiveDays`（当日及此前 4 个交易日，默认）；大小写敏感 |
| days | int | 否 | 查询当日及此前 N−1 个交易日 | 3 | 范围 1～5，`1` 表示当日 |
| ts_ms | int | 否 | 当日过滤起点（毫秒，包含起点） | 1789522140000 | 只过滤当日数据，不能通过它指定历史日期；早于当日零点时按当日零点处理 |

三个时间参数可以同时传入，按 `ts_ms` > `days` > `range` 选择生效参数，低优先级参数不参与范围计算；三者均不传时默认 `FiveDays`。

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`。`data` 为分时点数组，按时间升序排列，同一分钟只返回一个数据点，无分页：

| 字段名 | 类型 | 说明 | 单位 |
|--------|------|------|------|
| ts_ms | int | 分钟起点的 Unix 毫秒时间戳 | 毫秒 |
| price | number | 成交价格；历史分钟取该分钟收盘价，不复权 | 元 |
| avg_price | number / null | 当日累计成交均价；不可用时为 `null`，字段仍返回 | 元 |
| volume | int | 当日累计成交量 | 股 |
| turnover | number | 当日累计成交额 | 元 |

注：`price` / `avg_price` / `turnover` 是 JSON 数字，不是字符串。历史均价按当日累计成交额除以累计成交量计算，累计成交量为零时均价为 `null`。

## 4. 调用方式

```bash
# 当日分时
python <RUN_PY> stock-intraday --symbol 600000.SH --range Today

# 默认五日范围（不传任何时间参数）
python <RUN_PY> stock-intraday --symbol 600000.SH

# 当日及此前两个交易日
python <RUN_PY> stock-intraday --symbol 600000.SH --days 3

# 显式指定五日范围
python <RUN_PY> stock-intraday --symbol 600000.SH --range FiveDays

# 同时传入 days 与 range 时 days 优先，此请求按三日范围查询
python <RUN_PY> stock-intraday --symbol 600000.SH --days 3 --range Today
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- `symbol` 必填且需带市场后缀，不接受裸代码。
- `days=3` 表示当日及此前 2 个交易日，历史日期跳过休市日；例如在周二且周一、上周五均为交易日时，范围覆盖上周五、周一和周二。
- 当日按自然日计算：非交易日不会自动用上一个交易日替换当日，因此实际有数据的日期数可能少于 `days`。
- `ts_ms` 只过滤当日数据；传入过去日期的时间戳不会返回该历史日期。跨日查询使用 `days` 或 `range`。
- 历史分钟价格不复权。
- 行情查询所需数据不可用时接口返回错误，不会以缺少部分日期的数据冒充完整成功结果；HTTP 400 表示参数问题，405 不支持的方法，502 行情查询失败，503 行情服务暂不可用。