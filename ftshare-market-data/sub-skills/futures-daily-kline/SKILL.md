---
name: futures-daily-kline
description: 查询期货真实合约或 9999 主连的官方日 K（futures_daily_kline，GET /api/v1/market/data/futures/daily-kline）。用户问期货日线、主力连续合约日 K、某品种 9999 主连走势、某个交易日或日期区间的期货官方日行情时使用。必填 --symbol；日期用 --trade-date 单日，或用 --start-date/--end-date 区间。
---

# 期货官方日K与9999主连

接口：`GET /api/v1/market/data/futures/daily-kline`。在线文档：[《期货官方日K与9999主连》](https://market.ft.tech/gateway/doc/pages/g7x1q4wp.md)

查询单个期货真实合约或 9999 主连的官方日 K。每次只查询一个 `symbol`，返回带分页信息的 `{items,total,page,page_size}` 对象。

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 期货官方日K与9999主连（futures_daily_kline） |
| 外部接口 | `GET /api/v1/market/data/futures/daily-kline` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 单个期货真实合约日 K；9999 主连日 K；单日或日期区间查询 |
| 数据范围 | 按交易日查询 |
| 单次限量 | 每次查询一个 `symbol`；`page_size` 默认 50，最大 500 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|--------|------|----------|------|----------|
| symbol | string | 是 | 期货合约或 9999 主连代码，交易所后缀可带可不带；不带后缀时由服务端按品种推断交易所，代码不区分大小写 | A9999.DCE、A2405、AP2612.CZCE |
| trade_date | string | 单日模式必填 | 单个交易日 `YYYYMMDD`；与 `start_date`/`end_date` 二选一 | 20261117 |
| start_date | string | 区间模式必填 | 起始交易日 `YYYYMMDD`；必须与 `end_date` 成对传入 | 20261101 |
| end_date | string | 区间模式必填 | 结束交易日 `YYYYMMDD`；不能早于 `start_date` | 20261117 |
| rule_version | string | 否 | 9999 主连映射规则版本，默认 `v1`；查询真实合约时无影响 | v1 |
| page | int | 否 | 页码，从 1 开始，默认 1 | 1 |
| page_size | int | 否 | 每页条数，默认 50，最大 500 | 50 |

两种日期模式不能混用：单日只传 `--trade-date`，区间同时传 `--start-date` 与 `--end-date`，不传日期参数时接口返回参数错误。

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`。`data` 对象：

| 字段 | 类型 | 说明 |
|------|------|------|
| items | array | 当前页日 K 记录，按交易日升序；无数据时为空数组 |
| total | integer | 查询条件命中的总记录数，不随分页变化 |
| page | integer | 当前页码 |
| page_size | integer | 实际使用的每页条数，最大 500 |

`items` 字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| symbol | string | 合约代码；真实合约返回不带交易所后缀、沿用官网大小写的代码，9999 主连返回品种加 `9999`；CZCE 真实合约返回四位年份代码 |
| trade_date | integer | 交易日 `YYYYMMDD` |
| open / high / low / close | number | 开高低收价格 |
| volume | integer | 成交量（手） |
| amount | number | 成交额（元） |
| open_interest | integer | 持仓量（手） |

## 4. 调用方式

```bash
# 9999 主连：日期区间
python <RUN_PY> futures-daily-kline --symbol A9999.DCE --start-date 20261101 --end-date 20261117 --page 1 --page-size 5

# 真实合约：单个交易日
python <RUN_PY> futures-daily-kline --symbol AP2612.CZCE --trade-date 20261117

# 自动翻页取全部记录
python <RUN_PY> futures-daily-kline --symbol A9999.DCE --start-date 20261101 --end-date 20261117 --all
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- **合约代码口径**：交易所后缀不是必需，`A2405` 等价于 `A2405.DCE`；无法识别或唯一推断交易所时接口返回参数错误。CZCE 真实合约必须使用四位年份代码，例如 `AP2612.CZCE`；`AP612.CZCE` 不符合规范，返回成功空结果（`items=[]`、`total=0`）。
- 响应中的 `symbol` 统一不带交易所后缀。
- `rule_version` 仅对 9999 主连生效。`v1` 规则按交易日读取主力映射，并把映射出的真实合约当日官方日 K 作为结果：不做跨合约价格拼接、前复权或后复权；主力映射缺失或映射合约当日无官方日 K 时，该交易日不生成记录。
- 主力切换只影响切换日及之后的映射结果，历史记录不会回溯改写。
- 区间查询不会自行分页取全量，需要全部记录时加 `--all`（按 `page_size` 逐页取，直到取满 `total` 或返回空页）。