---
name: stock-goodwill-predict
description: Get goodwill impairment prediction data (商誉减值预期) for stocks. Use when user asks about 商誉减值预期, 商誉减值预告, 业绩预告, goodwill impairment prediction, goodwill forecast.
---

# 查询商誉减值预期明细

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询商誉减值预期明细 |
| 外部接口 | GET /api/v1/market/data/goodwill/predict |
| 请求方式 | GET |
| 适用场景 | 查询商誉减值业绩预告数据，包含预测净利润上下限、业绩变动幅度、上年同期净利润等字段 |

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
    "total": 820,
    "pages": 17,
    "records": [
      {
        "seq": 0,
        "security_code": "601211",
        "security_name": "国泰海通",
        "perform_change_explain": "业绩变动原因说明...",
        "predict_period": "20251231",
        "newest_goodwill": "10000000000.0000",
        "goodwill_previous": "9500000000.0000",
        "predict_netprofit_lower": "50000000000.0000",
        "predict_netprofit_upper": "60000000000.0000",
        "perform_change_lower": "10.50000000",
        "perform_change_upper": "20.50000000",
        "pe_samereport_netprofit": "45000000000.0000",
        "notice_date": "2025-04-01 00:00:00",
        "trade_market": "主板"
      }
    ]
  }
}
```

### 字段说明（GoodwillPredictItem）

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| seq | int | 否 | 序号 |
| security_code | string | 否 | 证券代码 |
| security_name | string | 是 | 证券简称 |
| perform_change_explain | string | 是 | 业绩变动原因 |
| predict_period | string | 是 | 预告周期 |
| newest_goodwill | string | 是 | 最新商誉（元） |
| goodwill_previous | string | 是 | 上期商誉（元） |
| predict_netprofit_lower | string | 是 | 预测净利润下限（元） |
| predict_netprofit_upper | string | 是 | 预测净利润上限（元） |
| perform_change_lower | string | 是 | 业绩变动下限（%） |
| perform_change_upper | string | 是 | 业绩变动上限（%） |
| pe_samereport_netprofit | string | 是 | 上年同期净利润（元） |
| notice_date | string | 是 | 公告日期，格式 YYYY-MM-DD HH:MM:SS |
| trade_market | string | 是 | 交易市场 |

## 注意事项

- date 格式为 YYYYMMDD，按年份范围过滤
- 金额字段均为 Decimal 类型，以字符串形式返回以保持精度
- 业绩变动上/下限为百分比值（如 10.5 表示 10.5%）

## 调用示例

```bash
python <RUN_PY> stock-goodwill-predict --date 20260828
```
