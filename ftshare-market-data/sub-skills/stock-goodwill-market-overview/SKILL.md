---
name: stock-goodwill-market-overview
description: Get A-share market-wide goodwill overview (A股商誉市场概况) with historical trends. Use when user asks about 商誉市场概况, 全市场商誉, 商誉历史趋势, goodwill market overview.
---

# 查询A股商誉市场概况

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询A股商誉市场概况 |
| 外部接口 | GET /api/v1/market/data/goodwill/market-overview |
| 请求方式 | GET |
| 适用场景 | 查询 A 股全市场商誉历史概况，包含商誉规模、减值金额、占净资产/净利润比例等汇总指标 |

## 请求参数

无需参数，返回全部历史数据，按报告期倒序排列。

## 执行方式

```bash
python scripts/handler.py
```

## 响应结构

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 17,
    "items": [
      {
        "report_date": "2026-03-31 00:00:00",
        "goodwill_scale": "1224218430250.2300",
        "goodwill_impairment": null,
        "net_assets": "56278253157394.5000",
        "goodwill_to_net_assets_ratio": "0.02175296",
        "impairment_to_net_assets_ratio": null,
        "net_profit_scale": "1133013378865.3600",
        "impairment_to_net_profit_ratio": null
      }
    ]
  }
}
```

### 字段说明（GoodwillMarketOverviewItem）

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| report_date | string | 是 | 报告期，格式 YYYY-MM-DD HH:MM:SS |
| goodwill_scale | string | 是 | 全市场商誉规模（元） |
| goodwill_impairment | string | 是 | 全市场商誉减值金额（元） |
| net_assets | string | 是 | 全市场净资产（元） |
| goodwill_to_net_assets_ratio | string | 是 | 商誉占净资产比例 |
| impairment_to_net_assets_ratio | string | 是 | 减值占净资产比例 |
| net_profit_scale | string | 是 | 全市场净利润规模（元） |
| impairment_to_net_profit_ratio | string | 是 | 减值占净利润比例 |

## 注意事项

- 无需参数，返回全量历史数据，按 report_date 倒序
- 金额字段均为 Decimal 类型，以字符串形式返回以保持精度
- goodwill_impairment 对应数据库 goodwill_change 列（response 层做了语义化重命名）

## 调用示例

```bash
python <RUN_PY> stock-goodwill-market-overview
```
