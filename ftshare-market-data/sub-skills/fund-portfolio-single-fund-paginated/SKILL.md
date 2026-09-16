---
name: fund-portfolio-single-fund-paginated
description: "按基金代码查报告期持仓明细。当用户需要查询基金持仓股票/债券/转债的代码、名称、数量、市值、占净值比等，通过 report_date 单期或 start_date+end_date 区间（互斥），publish_date 按发布日期过滤时使用。"
---

# 基金持仓明细

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金持仓明细                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-portfolio`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码 |
| `--report_date` | int | 否 | 报告期 YYYYMMDD（与 start/end 互斥） |
| `--publish_date` | int | 否 | 发布日期 YYYYMMDD |
| `--start_date` | int | 否 | 报告期起始日期（需与 end_date 同传） |
| `--end_date` | int | 否 | 报告期结束日期 |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-portfolio-single-fund-paginated --fund_code 000001 --report_date 20260331 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
