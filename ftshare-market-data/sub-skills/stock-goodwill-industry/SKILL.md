---
name: stock-goodwill-industry
description: Get goodwill data by industry (行业商誉). Use when user asks about 行业商誉, 各行业商誉, 行业商誉占比, goodwill by industry, industry goodwill.
---

# 查询行业商誉

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询行业商誉 |
| 外部接口 | GET /api/v1/market/data/goodwill/industry |
| 请求方式 | GET |
| 适用场景 | 查询各行业的商誉规模、商誉占净资产比例、净利润规模等汇总数据 |

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
    "date": "20251231",
    "total": 127,
    "items": [
      {
        "industry_name": "IT服务Ⅱ",
        "company_count": 67,
        "goodwill_scale": "32954873172.3000",
        "net_assets": "265068390706.9200",
        "goodwill_to_net_assets_ratio": "0.12432593",
        "net_profit_scale": "-1094685130.1200"
      }
    ]
  }
}
```

### 字段说明（GoodwillIndustryItem）

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| industry_name | string | 否 | 行业名称 |
| company_count | int | 是 | 公司数量 |
| goodwill_scale | string | 是 | 商誉规模（元） |
| net_assets | string | 是 | 净资产（元） |
| goodwill_to_net_assets_ratio | string | 是 | 商誉占净资产比例 |
| net_profit_scale | string | 是 | 净利润规模（元） |

## 注意事项

- date 格式为 YYYYMMDD，按年份范围过滤
- 金额字段均为 Decimal 类型，以字符串形式返回以保持精度

## 调用示例

```bash
python <RUN_PY> stock-goodwill-industry --date 20260828
```
