---
name: southbound
description: "查询南向资金交易数据。当用户需要查询指定交易日南向资金（港股通沪、港股通深）交易汇总数据，或了解南向资金交易数据时使用。"
---

# 查询南向资金交易数据

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询南向资金交易数据 |
| 外部接口 | `/api/v1/market/data/southbound` |
| 请求方式 | GET |
| 适用场景 | 查询指定交易日南向资金（港股通沪、港股通深）交易汇总数据 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `date` | string | 是 | 交易日期 | `20250101` | 格式 `YYYYMMDD` |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> southbound --date 20250101
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "code": 0,
    "message": "success",
    "data": {
        "date": "20250101",
        "currency": "HKD",
        "total": {
            "buy_amount": "100.00",
            "sell_amount": "80.00",
            "net_buy_amount": "20.00",
            "trade_count": 15
        },
        "channels": {
            "SH_HK": {
                "buy_amount": "60.00",
                "sell_amount": "50.00",
                "net_buy_amount": "10.00",
                "trade_count": 8
            },
            "SZ_HK": {
                "buy_amount": "40.00",
                "sell_amount": "30.00",
                "net_buy_amount": "10.00",
                "trade_count": 7
            }
        }
    }
}
```

### 顶层字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `code` | int | 否 | 业务状态码，0 表示成功 |
| `message` | string | 否 | 状态说明 |
| `data` | object | 否 | 南向资金数据 |

### data 字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `date` | string | 否 | 交易日期 |
| `currency` | string | 否 | 币种（HKD） |
| `total` | object | 否 | 南向合计数据 |
| `total.buy_amount` | string | 否 | 买入额 |
| `total.sell_amount` | string | 否 | 卖出额 |
| `total.net_buy_amount` | string | 否 | 净买入额 |
| `total.trade_count` | int | 否 | 成交笔数 |
| `channels` | object | 否 | 分市场通道数据 |

### channels 字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `SH_HK` | object | 否 | 港股通（沪）数据 |
| `SH_HK.buy_amount` | string | 否 | 买入额 |
| `SH_HK.sell_amount` | string | 否 | 卖出额 |
| `SH_HK.net_buy_amount` | string | 否 | 净买入额 |
| `SH_HK.trade_count` | int | 否 | 成交笔数 |
| `SZ_HK` | object | 否 | 港股通（深）数据 |
| `SZ_HK.buy_amount` | string | 否 | 买入额 |
| `SZ_HK.sell_amount` | string | 否 | 卖出额 |
| `SZ_HK.net_buy_amount` | string | 否 | 净买入额 |
| `SZ_HK.trade_count` | int | 否 | 成交笔数 |

## 注意事项

- `date` 为必填参数，格式 `YYYYMMDD`
- 金额类字段以字符串格式返回
- 响应为信封结构（`code` / `message` / `data`）
- 南向资金币种为 HKD（港币）
