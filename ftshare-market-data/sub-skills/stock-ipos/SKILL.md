---
name: stock-ipos
description: "获取股票 IPO 列表。当用户需要获取 A 股 IPO 列表，含发行价格、发行数量、申购日期、上市日期等，支持分页查询，或了解股票 IPO 列表时使用。"
---

# 获取股票 IPO 列表

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 获取股票 IPO 列表 |
| 外部接口 | `/api/v1/market/data/stock-ipos` |
| 请求方式 | GET |
| 适用场景 | 获取 A 股 IPO 列表，含发行价格、发行数量、申购日期、上市日期等，支持分页查询 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `page` | int | 是 | 页码，从 1 开始 | `1` | 必须大于等于 1 |
| `page_size` | int | 是 | 每页记录数 | `20` | 必须大于等于 1，建议不超过 100 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 获取第 1 页，每页 20 条
python <RUN_PY> stock-ipos --page 1 --page_size 20

# 获取第 2 页，每页 50 条
python <RUN_PY> stock-ipos --page 2 --page_size 50

# 获取全量数据（自动翻页合并）
python <RUN_PY> stock-ipos --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "items": [
        {
            "symbol": "600989.SH",
            "industry_pe": 15.8,
            "listing_date": "2019-05-16",
            "max_subscription_shares": 120000,
            "online_shares": 600000000,
            "pe": 22.5,
            "price": "11.25",
            "shares": 734000000,
            "subscription_date": "2019-05-10",
            "subscription_symbol_id": "730989"
        }
    ],
    "total_pages": 10,
    "total_items": 200
}
```

### 顶层字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `items` | Array | 否 | 当前页 IPO 列表 |
| `total_pages` | int | 否 | 总页数 |
| `total_items` | int | 否 | 总记录数（未分页前） |

### items 元素字段说明（StockIpo）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|---|---|---|---|---|
| `symbol` | String | 否 | 标的代码，带 `.SZ`/`.SH`/`.BJ` 市场后缀 | - |
| `industry_pe` | float | 是 | 行业市盈率 | - |
| `listing_date` | String | 是 | 上市日期，格式 `YYYY-MM-DD` | - |
| `max_subscription_shares` | int | 是 | 申购上限 | 股 |
| `online_shares` | int | 否 | 网上发行数量 | 股 |
| `pe` | float | 是 | 发行市盈率 | - |
| `price` | String | 是 | 发行价格 | 元 |
| `shares` | int | 否 | 发行数量 | 股 |
| `subscription_date` | String | 是 | 申购日期，格式 `YYYY-MM-DD` | - |
| `subscription_symbol_id` | String | 是 | 申购代码 | - |

## 注意事项

- `page` 和 `page_size` 为必填项
- 如需全量数据，按 `page` 递增循环请求至 `total_pages`，合并所有 `items`
- 可为空字段（如 `industry_pe`、`listing_date` 等）可能返回 `null`，展示时需做空值处理
- `price` 为字符串类型，比较或计算前需转为数值
