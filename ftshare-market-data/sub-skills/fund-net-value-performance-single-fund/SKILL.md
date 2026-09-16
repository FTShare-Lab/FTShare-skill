---
name: fund-net-value-performance-single-fund
description: "按基金代码查净值口径收益表现。当用户需要查询基金多区间收益率（日/周/月/近三月/六月/今年/近一至十年/成立以来及对应年化收益率），通过 stat_date 单日或 start_date+end_date 区间（互斥）查询时使用。"
---

# 基金净值收益表现

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金净值收益表现                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-net-value-performance`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码 |
| `--stat_date` | int | 否 | 统计日期 YYYYMMDD（与 start/end 互斥） |
| `--start_date` | int | 否 | 统计开始日期（需与 end_date 同传） |
| `--end_date` | int | 否 | 统计结束日期 |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-net-value-performance-single-fund --fund_code 000001 --start_date 20260101 --end_date 20260717 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
