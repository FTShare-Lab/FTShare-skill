---
name: block-trades
description: "查询大宗交易列表。当用户需要获取 A 股大宗交易记录，包含买卖方营业部、成交价、成交量、溢价率等，或了解大宗交易列表时使用。"
---

# 查询大宗交易列表

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询大宗交易列表 |
| 外部接口 | `/api/v1/market/data/block-trades` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股大宗交易记录，包含买卖方营业部、成交价、成交量、溢价率等 |

## 请求参数

无需任何参数。

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> block-trades
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

返回值为大宗交易记录数组（直接返回数组，非对象包装）：

```json
[
    {
        "symbol": "000001.SZ",
        "name": "平安银行",
        "date": "2025-03-10",
        "price": "10.50",
        "close": "10.48",
        "volume": 1000000,
        "premium_rate": 0.19,
        "buyer_name": "某某营业部",
        "seller_name": "某某证券营业部"
    }
]
```

### 字段说明（BlockTrade）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `symbol` | String | 否 | 标的代码，带市场后缀 | - |
| `name` | String | 否 | 标的名称 | - |
| `date` | String | 否 | 成交日期，格式 `YYYY-MM-DD` | - |
| `price` | Number | 否 | 成交价 | 元 |
| `close` | Number | 否 | 收盘价 | 元 |
| `volume` | int | 否 | 成交量 | 股 |
| `premium_rate` | Number | 否 | 溢价率（小数形式，如 `0.19` 表示 19%） | - |
| `buyer_name` | String | 否 | 买方营业部名称 | - |
| `seller_name` | String | 否 | 卖方营业部名称 | - |

## 注意事项

- 接口直接返回数组，无分页包装结构
- `premium_rate` 为小数形式，展示时乘以 100 转为百分比
- `price` 和 `close` 在文档中标注为 Number，但部分情况可能以字符串返回，比较前注意类型转换
