---
name: stock-share-chg
description: "查询 A 股股东增减持明细。当用户需要获取 A 股股东增减持数据（按 stock_code 分页查询全部历史，或以 is_last=true 查全市场最新一期），支持沪深京股票时使用。"
---

# 查询 A 股股东增减持

## 接口说明

| 项目     | 说明                                                                            |
|----------|---------------------------------------------------------------------------------|
| 接口名称 | 查询 A 股股东增减持                                                              |
| 外部接口 | `/api/v1/market/data/holder/stock-share-chg`                               |
| 请求方式 | GET                                                                             |
| 适用场景 | 指定 stock_code 分页查询该标的全部历史增减持，或 is_last=true 查全市场最新一期 |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述            | 取值示例  | 备注                                                                                     |
|------------|--------|----------|-----------------|-----------|------------------------------------------------------------------------------------------|
| stock_code | string | 否       | 单个股票代码    | 603323.SH | 不传时需配合 `--is_last`；支持沪深京 A 股，需 6 位数字+后缀（SH/SZ/BJ），单次仅支持一个代码 |
| is_last    | flag   | 否       | 取所有标的最新一期 | （flag）  | 传字符串 `"true"`；与 `stock_code` 二选一                                                    |
| page       | int    | 否       | 页码            | 1         | 默认 1                                                                                    |
| page_size  | int    | 否       | 每页记录数      | 50        | 默认 50                                                                                   |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-share-chg --stock_code 603323.SH
python <RUN_PY> stock-share-chg --stock_code 603323.SH --page 2 --page_size 20
python <RUN_PY> stock-share-chg --is_last --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

```json
{
    "items": [
        {
            "trade_code": "000001",
            "stock_name": "平安银行",
            "holder_name": "张某某",
            "shareholding_change_info": "增持",
            "change_quantity": "30000",
            "pre_change_quantity": "0",
            "pre_change_total_capital_ratio": null,
            "post_change_quantity": "30000",
            "post_change_total_capital_ratio": null,
            "transfer_method": null,
            "latest_price": "18.45",
            "price_change_rate": "0",
            "transaction_price": null,
            "transaction_amount": null,
            "progress_description": null,
            "change_start_date": "2021-09-06",
            "change_end_date": "2021-09-06",
            "announcement_date": "2021-09-07"
        }
    ],
    "total_pages": 1,
    "total_items": 11036
}
```

### items 元素字段

| 字段名                          | 类型   | 是否可为空 | 说明                                        |
|---------------------------------|--------|------------|---------------------------------------------|
| trade_code                      | String | 否         | 股票交易代码，6 位数字                       |
| stock_name                      | String | 否         | 上市公司官方简称                            |
| holder_name                     | String | 否         | 持股变动主体（股东名称）                     |
| shareholding_change_info        | String | 否         | 持股变动类型：增持/减持                       |
| change_quantity                 | string | 否         | 持股变动数量                                |
| pre_change_quantity             | string | 否         | 变动前持股数量                              |
| pre_change_total_capital_ratio  | String | 是         | 变动前持股占总股本比例（暂空）               |
| post_change_quantity            | string | 否         | 变动后持股数量                              |
| post_change_total_capital_ratio | String | 是         | 变动后持股占总股本比例（暂空）               |
| transfer_method                 | String | 是         | 股份转让方式（暂空）                         |
| latest_price                    | string | 否         | 股票最新价                                  |
| price_change_rate               | string | 否         | 股票涨跌幅                                  |
| transaction_price               | String | 是         | 股份交易价格（暂空）                         |
| transaction_amount              | String | 是         | 股份交易金额（暂空）                         |
| progress_description            | String | 是         | 持股变动进展说明（暂空）                     |
| change_start_date               | String | 否         | 变动开始日期 YYYY-MM-DD                      |
| change_end_date                 | String | 否         | 变动截止日期 YYYY-MM-DD                      |
| announcement_date               | String | 否         | 公告发布日期 YYYY-MM-DD                      |

## 注意事项

- 必须至少指定 `--stock_code` 或 `--is_last` 其一。
- `shareholding_change_info` 仅为「增持」「减持」两种取值。
- `pre_change_total_capital_ratio`/`post_change_total_capital_ratio`/`transfer_method`/`transaction_price`/`transaction_amount`/`progress_description` 当前接口均暂为空值。
- `is_last` 在 query string 中传字符串 `"true"`。
