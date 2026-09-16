---
name: stock-holder-ten
description: "查询 A 股十大股东。当用户需要获取 A 股十大股东信息（按 stock_code 查全部历史，或以 is_last=true 查全市场最新一期），支持沪深京股票，或了解单票/全市场十大股东时使用。"
---

# 查询 A 股十大股东

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 查询 A 股十大股东                                                  |
| 外部接口 | `/api/v1/market/data/holder/stock-holder-ten`                  |
| 请求方式 | GET                                                                |
| 适用场景 | 指定 stock_code 查全部历史十大股东，或 is_last=true 查全市场最新一期 |

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
python <RUN_PY> stock-holder-ten --stock_code 603323.SH
python <RUN_PY> stock-holder-ten --is_last --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

```json
{
    "items": [
        {
            "stock_code": "603323.SH",
            "stock_name": "苏农银行",
            "publish_date": "2026-03-31",
            "share_holding": 50.96,
            "fen_holders": [
                {
                    "rank": 1,
                    "shareholder_name": "苏州国际发展集团有限公司",
                    "shareholder_type": "国有法人",
                    "share_type": "A股",
                    "shareholding": 200000000,
                    "share_ratio": 10.55,
                    "limit_num": 0,
                    "unlimit_num": 200000000,
                    "change_shares": 0,
                    "change_type": "不变",
                    "change_percentage": 0
                }
            ]
        }
    ],
    "total_pages": 1,
    "total_items": 21
}
```

### 顶层字段说明

| 字段名      | 类型  | 是否可为空 | 说明                             |
|-------------|-------|------------|----------------------------------|
| items       | Array | 否         | 公告期列表                       |
| total_pages | int   | 否         | 总页数                           |
| total_items | int   | 否         | 总记录数                         |

### fen_holders 数组元素字段

| 字段名            | 类型   | 是否可为空 | 说明                                       |
|-------------------|--------|------------|--------------------------------------------|
| rank              | int    | 否         | 股东名次                                   |
| shareholder_name  | String | 否         | 股东名称                                   |
| shareholder_type  | String | 否         | 股东性质                                   |
| share_type        | String | 否         | 股份类型                                   |
| shareholding      | string | 否         | 持股数（股）                                |
| share_ratio       | string | 否         | 占股本持股比例（%）                          |
| limit_num         | string | 是         | 限售数量                                    |
| unlimit_num       | string | 是         | 无限售数量                                  |
| change_shares     | string | 否         | 增减（股）                                  |
| change_type       | String | 是         | 变动类型                                    |
| change_percentage | string | 是         | 变动比例（%）                                |

## 注意事项

- 必须至少指定 `--stock_code` 或 `--is_last` 其一。
- 指定 `--stock_code` 时返回该标的全部历史，通常 `total_pages` 为 1。
- `--is_last` 模式按 `page`/`page_size` 分页返回全市场最新一期。
- `is_last` 在 query string 中传字符串 `"true"`。
- `fen_holders` 中 `limit_num`/`unlimit_num`/`change_type`/`change_percentage` 可能为空。
