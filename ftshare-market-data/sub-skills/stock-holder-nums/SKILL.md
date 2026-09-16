---
name: stock-holder-nums
description: "查询 A 股股东人数。当用户需要获取 A 股股东人数信息（按 stock_code 查全部历史，或以 is_last=true 查全市场最新一期），含人均流通股、筹码集中度、十大股东持股比例等衍生指标时使用。"
---

# 查询 A 股股东人数

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 查询 A 股股东人数                                                  |
| 外部接口 | `/api/v1/market/data/holder/stock-holder-nums`                |
| 请求方式 | GET                                                                |
| 适用场景 | 指定 stock_code 查全部历史股东人数，或 is_last=true 查全市场最新一期 |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述            | 取值示例  | 备注                                                                                       |
|------------|--------|----------|-----------------|-----------|--------------------------------------------------------------------------------------------|
| stock_code | string | 否       | 单个股票代码    | 603323.SH | 不传时需配合 `--is_last`；支持沪深京 A 股，需 6 位数字+后缀（SH/SZ/BJ），单次仅支持一个代码 |
| is_last    | flag   | 否       | 取所有标的最新一期 | （flag）  | 传字符串 `"true"`；与 `stock_code` 二选一                                                    |
| page       | int    | 否       | 页码            | 1         | 默认 1，仅 `is_last=true` 模式下生效                                                        |
| page_size  | int    | 否       | 每页记录数      | 50        | 默认 50                                                                                     |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-holder-nums --stock_code 603323.SH
python <RUN_PY> stock-holder-nums --is_last --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

```json
{
    "items": [
        {
            "stock_code": "000001.SZ",
            "stock_name": "平安银行",
            "publish_date": "2026-04-29",
            "report_date": "2026-03-31",
            "holder_num": 11215,
            "holder_num_change_ratio": -5.5022,
            "per_capita_circ_share": 4895.6833,
            "per_capita_share_change_ratio": null,
            "chip_concentration": null,
            "close_price": "0",
            "per_capita_hold_amount": "0",
            "ten_holder_ratio": null,
            "ften_holder_ratio": null
        }
    ],
    "total_pages": 1,
    "total_items": 5784
}
```

### 顶层字段说明

| 字段名      | 类型  | 是否可为空 | 说明           |
|-------------|-------|------------|-----------------|
| items       | Array | 否         | 股东人数列表    |
| total_pages | int   | 否         | 总页数          |
| total_items | int   | 否         | 总记录数        |

### items 元素字段

| 字段名                       | 类型   | 是否可为空 | 说明                              |
|------------------------------|--------|------------|-----------------------------------|
| stock_code                   | string | 否         | 股票代码                          |
| stock_name                   | string | 否         | 股票名称                          |
| publish_date                 | string | 否         | 发布日期                          |
| report_date                  | string | 否         | 报告期                            |
| holder_num                   | int    | 否         | 股东人数                          |
| holder_num_change_ratio      | string | 是         | 股东人数较上期变化比例             |
| per_capita_circ_share        | string | 是         | 人均流通股数                       |
| per_capita_share_change_ratio| string | 是         | 人均流通股变化比例                 |
| chip_concentration           | string | 是         | 筹码集中度                         |
| close_price                  | string | 否         | 收盘价                            |
| per_capita_hold_amount       | string | 否         | 人均持股金额                       |
| ten_holder_ratio             | string | 是         | 十大股东持股比例                   |
| ften_holder_ratio            | string | 是         | 十大流通股东持股比例               |

## 注意事项

- 必须至少指定 `--stock_code` 或 `--is_last` 其一。
- `chip_concentration`/`ten_holder_ratio`/`ften_holder_ratio` 等字段部分标的暂为空。
- `is_last` 在 query string 中传字符串 `"true"`。
