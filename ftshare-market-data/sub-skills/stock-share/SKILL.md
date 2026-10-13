---
name: stock-share
description: "查询股票股本信息。当用户需要查询某只 A 股在某日的总股本、A 股流通/限售/无限售股本、B 股股本、H 股股本、境外上市股本等股本结构，或按发布日期/生效日期查询某日全市场股本记录时使用。"
---

# 查询股票股本信息

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 查询股票股本信息                                                    |
| 外部接口 | `/api/v2/market/data/share/get-stock-share`                 |
| 请求方式 | GET                                                               |
| 适用场景 | 按要求日期查询单只股票最新股本记录，或分页查询指定日期全市场股本记录    |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述            | 取值示例  | 备注                                                                                       |
|------------|--------|----------|-----------------|-----------|--------------------------------------------------------------------------------------------|
| stock_code | string | 否       | 单个股票代码    | 000001.SZ | 支持六位数字、短后缀（SH/SZ/BJ）和长后缀（XSHG/XSHE/BJSE）；不传返回全市场                   |
| date       | string | 是       | 日期 YYYYMMDD   | 20260716  | 所有查询模式下均必填；缺少时返回 HTTP 400                                                   |
| date_type  | string | 否       | 日期条件类型    | publish_date | `publish_date`（发布日期，默认）或 `end_date`（生效日期）                                 |
| page       | int    | 否       | 全市场查询页码  | 1         | 从 1 开始，默认 1；单标的查询时忽略                                                         |
| page_size  | int    | 否       | 全市场每页条数  | 200       | 默认 200，取值范围 1-500；单标的查询时忽略                                                  |
| --all      | -      | 否       | 自动翻页拉全量  | -         | 仅本子 skill 扩展参数，用于全市场查询                                                       |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-share --stock_code 000001.SZ --date 20260716
python <RUN_PY> stock-share --stock_code 920476.BJ --date 20261012 --date_type end_date
python <RUN_PY> stock-share --date 20261012 --date_type publish_date --page 1 --page_size 5
python <RUN_PY> stock-share --date 20261012 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

外层固定为 `code` / `message` / `data`；`data` 为分页对象（`items` / `total_pages` / `total_items`）。传 `stock_code` 时命中最新 1 条；不传时按指定日期返回全市场记录并分页；未命中 `items` 为空数组。

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "stock_code": "920476.BJ",
                "stock_name": "海能技术",
                "publish_date": 20260930,
                "end_date": 20261012,
                "totshare_num": "89585740",
                "ashare_circ_num": "89585740",
                "ashare_circ_limit_num": "8958382",
                "ashare_circ_unlimit_num": "80627358",
                "bshare_num": "0",
                "bshare_circ_num": "0",
                "bshare_uncirc_num": "0",
                "hshare_num": "0",
                "osshare_num": "0",
                "share_circ_num": "89585740"
            }
        ],
        "total_items": 1,
        "total_pages": 1
    }
}
```

### data 字段说明

| 字段名       | 类型  | 是否可为空 | 说明     |
|--------------|-------|------------|----------|
| items        | Array | 否         | 股本信息列表 |
| total_pages | int   | 否         | 总页数   |
| total_items | int   | 否         | 总记录数 |

### items 元素字段

| 字段名                | 类型   | 是否可为空 | 说明                  |
|-----------------------|--------|------------|-----------------------|
| stock_code            | string | 否         | 股票代码              |
| stock_name            | string | 否         | 股票名称              |
| publish_date          | int    | 否         | 发布日期 YYYYMMDD     |
| end_date              | int    | 否         | 生效日期 YYYYMMDD     |
| totshare_num          | string | 否         | 总股本                |
| ashare_circ_num       | string | 否         | A 股流通股本           |
| ashare_circ_limit_num | string | 否         | A 股限售流通股本       |
| ashare_circ_unlimit_num | string | 否       | A 股无限售流通股本     |
| bshare_num            | string | 否         | B 股股本              |
| bshare_circ_num       | string | 否         | B 股流通股本          |
| bshare_uncirc_num     | string | 否         | B 股非流通股本        |
| hshare_num            | string | 否         | H 股股本              |
| osshare_num           | string | 否         | 境外上市股本          |
| share_circ_num        | string | 否         | 流通股本合计          |

## 注意事项

- `date` 在所有查询模式下均必填，格式 YYYYMMDD；即使传入 `stock_code` 也不能省略 `date`，缺少时返回 HTTP 400。
- `stock_code` 选填；不传时查询全市场，需配合 `--page` / `--page_size`（或 `--all`）。
- `date_type` 默认 `publish_date`（按发布日期查询），可改为 `end_date`（按生效日期查询）。
- 未命中数据时 `items` 为空数组。
- 金额/股数字段以字符串返回，保持精度。
