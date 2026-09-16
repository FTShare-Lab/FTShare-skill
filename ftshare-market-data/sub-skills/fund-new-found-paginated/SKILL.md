---
name: fund-new-found-paginated
description: "查询新发基金（按成立日范围 + 倒序，分页）。当用户需要查询新发基金代码/名称/管理人/托管人/运作方式/类型/成立日期/成立规模等，可按 fund_type 过滤、按 start_date/end_date 限定成立日范围时使用。"
---

# 基金新发

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金新发                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-new-found`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--start_date` | int | 否 | 成立日起始日期 YYYYMMDD（不传默认近 1 年） |
| `--end_date` | int | 否 | 成立日截止日期 YYYYMMDD（不传默认今天） |
| `--fund_type` | string | 否 | 基金类型过滤：混合型/债券型/股票型/货币型/其他型/保本型/REITs |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-new-found-paginated --fund_type 混合型 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
