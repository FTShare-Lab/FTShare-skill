---
name: stock-share
description: "获取单票指定日期股本信息。当用户需要查询某只 A 股股票在某日的总股本、A 股流通/限售/无限售股本、B 股股本、H 股股本、境外上市股本等股本快照时使用。"
---

# 获取单票指定日期股本信息

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 获取单票指定日期股本信息                                            |
| 外部接口 | `/api/v1/market/data/share/get-stock-share`                 |
| 请求方式 | GET                                                               |
| 适用场景 | 按日期快照查询单票股本结构                                          |

## 请求参数

| 参数名     | 类型   | 是否必填 | 描述            | 取值示例  | 备注                                                                                       |
|------------|--------|----------|-----------------|-----------|--------------------------------------------------------------------------------------------|
| stock_code | string | 是       | 单个股票代码    | 000001.SZ | 支持 6 位数字+后缀（SH/SZ/BJ）                                                              |
| date       | string | 是       | 日期 YYYYMMDD   | 20260716  | 按指定日期快照查询                                                                          |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stock-share --stock_code 000001.SZ --date 20260716
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

返回分页结构（items/total_pages/total_items），命中时仅返回 1 条；未命中 items 为空数组。

```json
{
    "items": [
        {
            "stock_code": "000001.SZ",
            "stock_name": "平安银行",
            "totshare_num": "19405918198",
            "ashare_circ_num": "19405918198",
            "ashare_circ_limit_num": "317545",
            "ashare_circ_unlimit_num": "19405600653",
            "bshare_num": "0",
            "bshare_circ_num": "0",
            "bshare_uncirc_num": "0",
            "hshare_num": "0",
            "osshare_num": "0",
            "share_circ_num": "19405918198"
        }
    ],
    "total_pages": 1,
    "total_items": 1
}
```

### 顶层字段说明

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

- `stock_code` 与 `date` 均必填，`date` 格式 YYYYMMDD。
- 未命中数据时 `items` 为空数组。
- 金额/股数字段以字符串返回，保持精度。
