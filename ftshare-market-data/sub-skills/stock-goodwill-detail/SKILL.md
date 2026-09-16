---
name: stock-goodwill-detail
description: Get goodwill detail (商誉明细) for all stocks in a specific year. Use when user asks about 商誉, 商誉明细, 商誉规模, 商誉占净资产比例, goodwill.
---

# 查询个股商誉明细

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询个股商誉明细 |
| 外部接口 | GET /api/v1/market/data/goodwill/stock-detail |
| 请求方式 | GET |
| 适用场景 | 查询个股的商誉规模、商誉占净资产比例、净利润同比变化等明细数据 |

## 请求参数

说明：date 为必填项。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| date | string | 是 | 报告期日期 | 20251231 | 格式 YYYYMMDD，按年份范围过滤，如 20251231 查询 2025 全年 |

## 执行方式

```bash
python scripts/handler.py --date 20251231
```

## 响应结构

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 50,
    "total": 2676,
    "pages": 54,
    "records": [
      {
        "seq": 0,
        "security_code": "300860",
        "security_name": "锋尚文化",
        "goodwill_scale": "28235811.5900",
        "goodwill_to_net_assets_ratio": "0.00898123",
        "net_profit_scale": "-16592410.5300",
        "net_profit_yoy_ratio": "-1.39720928",
        "goodwill_previous": "28235811.5900",
        "notice_date": "2026-05-13 00:00:00",
        "trade_board": "cyb"
      }
    ]
  }
}
```

### 字段说明（GoodwillStockDetailItem）

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| seq | int | 否 | 序号 |
| security_code | string | 否 | 证券代码 |
| security_name | string | 是 | 证券简称 |
| goodwill_scale | string | 是 | 商誉规模（元） |
| goodwill_to_net_assets_ratio | string | 是 | 商誉占净资产比例 |
| net_profit_scale | string | 是 | 净利润规模（元） |
| net_profit_yoy_ratio | string | 是 | 净利润同比变化率 |
| goodwill_previous | string | 是 | 上期商誉（元） |
| notice_date | string | 是 | 公告日期，格式 YYYY-MM-DD HH:MM:SS |
| trade_board | string | 是 | 交易板块（sh/sz/cyb/star/bj/hk） |

## 注意事项

- date 格式为 YYYYMMDD，按年份范围过滤（如 20251231 查询 2025 全年数据）
- 金额字段均为 Decimal 类型，以字符串形式返回以保持精度
- notice_date 大部分常规商誉记录为 null，仅减值相关记录有公告日期
- trade_board 取值：sh（上交所主板）、sz（深交所主板）、cyb（创业板）、star（科创板）、bj（北交所）、hk（港股）

## 调用示例

```bash
python <RUN_PY> stock-goodwill-detail --date 20260828
```
