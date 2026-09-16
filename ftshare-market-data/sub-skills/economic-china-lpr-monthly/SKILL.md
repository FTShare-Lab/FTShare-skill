---
name: economic-china-lpr-monthly
description: Get China LPR (Loan Prime Rate) monthly data (LPR 贷款市场报价利率 月度). Use when user asks about LPR, 贷款市场报价利率, 1年期LPR, 5年期LPR, 中国 LPR, 房贷利率, China LPR.
---

# 中国经济 - LPR 贷款市场报价利率（月度）

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | LPR 贷款市场报价利率（月度汇总计算结果） |
| 外部接口 | GET /api/v1/market/data/economic/china-lpr |
| 请求方式 | GET |
| 适用场景 | 获取中国 LPR 1 年期与 5 年期利率按日期汇总数据 |

## 2. 请求参数

说明：该接口无需请求参数。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| - | - | - | 无需参数 | - | - |

## 3. 用法

直接执行：

```bash
python script/handler.py
```

脚本输出 JSON 数组，按时间倒序，每项含 `date`（如 2025-12-22）、`lpr_1y`（1 年期 LPR %）、`lpr_5y`（5 年期 LPR %），以表格展示给用户。

## 4. 响应说明

返回值为 LPR 按日期计算结果列表，按时间倒序。

### LprComputed 结构

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| date | String | 否 | 日期，格式如 2025-12-22 | - |
| lpr_1y | float | 是 | LPR 1 年期利率 | % |
| lpr_5y | float | 是 | LPR 5 年期利率 | % |

## 5. 请求示例

```
GET /api/v1/market/data/economic/china-lpr
```

## 6. 注意事项

- 返回按报价日期（通常为每月 20 日左右）汇总，列表已按时间倒序，最新日期在前。
- `lpr_1y`、`lpr_5y` 单位为 %，可为 null。

## 调用示例

```bash
python <RUN_PY> economic-china-lpr-monthly
```
