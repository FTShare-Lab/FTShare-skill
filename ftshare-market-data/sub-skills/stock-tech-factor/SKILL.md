---
name: stock-tech-factor
description: "查询单只沪深北 A 股在指定交易日的基础行情、估值、股本及技术面因子。用户问某只股票的技术面因子、技术指标（MACD、KDJ、RSI、BOLL、DMI、BIAS、ATR、OBV 等）、不复权/前复权指标、换手率、量比、市盈率/市净率等单日因子快照时使用。"
---

# 股票技术面因子

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 股票技术面因子（market_stock_factor）                               |
| 外部接口 | `/api/v2/market/data/stock-factor`                         |
| 请求方式 | GET                                                               |
| 适用场景 | 查询单只沪深北 A 股在某个交易日的基础行情、估值、股本与技术面指标     |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述         | 取值示例   | 备注                                                                                            |
|------------|--------|----------|--------------|------------|-----------------------------------------------------------------------------------------------|
| symbol     | string | 是       | 证券代码     | 000001.SZ  | 必须带交易所后缀；标准后缀 `SH`/`SZ`/`BJ`（大小写均可），兼容 `XSHG`/`XSHE`/`BJSE`；不接受无后缀六位代码 |
| trade_date | string | 否       | 目标日期     | 20261012   | 格式 `YYYYMMDD`；不传按当前日期处理；未来日期或早于 `19900101` 会被拒绝                             |
| category   | string | 否       | 返回字段分类 | trend      | 可选 `quote`/`valuation`/`capital`/`trend`/`momentum`/`volatility`/`volume`/`sentiment`；不传返回全部字段 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-tech-factor --symbol 000001.SZ --trade-date 20261012 --category trend
python <RUN_PY> stock-tech-factor --symbol 000001.SZ --category quote
python <RUN_PY> stock-tech-factor --symbol 000001.SZ
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

外层固定为 `code` / `message` / `data`；成功时 `code=200`、`message=success`，`data.values` 为因子字段对象。传入 `category` 时仍会返回基础行情字段；不传时返回全部 183 个字段。

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "values": {
            "ts_code": "000001.SZ",
            "trade_date": "20261012",
            "open": 11.62,
            "high": 11.83,
            "low": 11.62,
            "close": 11.73,
            "open_qfq": 11.62,
            "high_qfq": 11.83,
            "low_qfq": 11.62,
            "close_qfq": 11.73,
            "pre_close": 11.59,
            "change": 0.14,
            "pct_chg": 1.2079,
            "vol": 1058634.56,
            "amount": 1243459.833,
            "pe": 5.3393,
            "pe_ttm": 5.2378,
            "pb": 0.4862,
            "macd_qfq": 0.0244,
            "kdj_k_bfq": 57.23,
            "rsi_bfq_6": 58.67
        }
    }
}
```

### 字段分类

| 分类（`category`） | 内容                                                                          |
|--------------------|-------------------------------------------------------------------------------|
| quote              | 基础行情（所有分类都会返回）：`ts_code`、`trade_date`、`open/high/low/close`（不复权）、`open_qfq/high_qfq/low_qfq/close_qfq`（前复权）、`pre_close`、`change`、`pct_chg`、`vol`、`amount` |
| valuation          | 估值：`pe`、`pe_ttm`、`pb`、`ps`、`ps_ttm`、`dv_ratio`、`dv_ttm`                 |
| capital            | 股本：`total_share`、`float_share`、`free_share`、`total_mv`、`circ_mv`、`adj_factor` |
| trend              | 趋势：ASI/ASIT/BBI/DFMA/DMI/EXPMA/MACD，以及 MA、EMA 各周期                     |
| momentum           | 动量：BIAS、CCI、DPO/MADPO、KDJ、MTM/MTMMA、ROC/MAROC、TRIX/TRMA、WR、RSI        |
| volatility         | 波动：ATR、BOLL、KTN、MASS、TAQ、XSII                                          |
| volume             | 量价：`turnover_rate`、`turnover_rate_f`、`volume_ratio`、EMV、MFI、OBV、VR       |
| sentiment          | 情绪：`updays`、`downdays`、`topdays`、`lowdays`，以及 BRAR、CR、PSY             |

完整字段清单（共 183 个）以源接口文档 `ftshare-doc/api-doc/股票数据/特色数据/股票技术面因子.md` 为准。

## 注意事项

- 技术指标按不复权（`_bfq`）与前复权（`_qfq`）分别给出，不返回后复权（`_hfq`）。
- 单位：`vol` 为手（1 手 = 100 股），`amount` 为千元，`total_share`/`float_share`/`free_share` 为万股，`total_mv`/`circ_mv` 为万元。
- 价格、成交量、成交额以 JSON number 返回；缺少源数据的可选字段可能为 `null`。
- 未传 `trade_date` 时按当前日期处理：交易日 15:30 前请求当日会回退到最近交易日，15:30 后才返回当日数据。
- 请求限制：`symbol` 无后缀、非沪深北代码，`trade_date` 非八位日期或超出范围，`category` 非枚举值，出现未定义 query 参数，均返回 HTTP 400。
