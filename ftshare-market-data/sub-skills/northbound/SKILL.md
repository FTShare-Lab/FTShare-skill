---
name: northbound
description: "查询北向资金交易数据。当用户需要查询指定交易日北向资金（沪股通、深股通）交易汇总数据，或了解北向资金交易数据时使用。"
---

# 查询北向资金交易数据

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询北向资金交易数据 |
| 外部接口 | `/api/v1/market/data/northbound` |
| 请求方式 | GET |
| 适用场景 | 查询指定交易日北向资金（沪股通、深股通）交易汇总数据 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `date` | string | 是 | 交易日期 | `20250101` | 格式 `YYYYMMDD` |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> northbound --date 20250101
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "code": 0,
    "message": "success",
    "data": {
        "date": "20250101",
        "currency": "CNY",
        "total_amount": "100.50",
        "channels": {
            "SH": { "amount": "60.00", "trade_count": 10 },
            "SZ": { "amount": "40.50", "trade_count": 8 }
        }
    }
}
```

### 顶层字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `code` | int | 否 | 业务状态码，0 表示成功 |
| `message` | string | 否 | 状态说明 |
| `data` | object | 否 | 北向资金数据 |

### data 字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `date` | string | 否 | 交易日期 |
| `currency` | string | 否 | 币种（CNY） |
| `total_amount` | string | 否 | 北向资金合计成交额 |
| `channels` | object | 否 | 分市场通道数据 |

### channels 字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `SH` | object | 否 | 沪股通数据 |
| `SH.amount` | string | 否 | 成交额 |
| `SH.trade_count` | int | 否 | 成交笔数 |
| `SZ` | object | 否 | 深股通数据 |
| `SZ.amount` | string | 否 | 成交额 |
| `SZ.trade_count` | int | 否 | 成交笔数 |

## 注意事项

- `date` 为必填参数，格式 `YYYYMMDD`
- 金额类字段以字符串格式返回
- 响应为信封结构（`code` / `message` / `data`）
