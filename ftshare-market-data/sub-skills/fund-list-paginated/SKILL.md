---
name: fund-list-paginated
description: "分页查询公募基金基础列表。当用户需要查询基金代码/名称/交易代码/基金公司/经理/托管人/运作方式/类型/成立日期/规模等基金基础档案，可按 fund_code 查单只或按 fund_type 过滤时使用。"
---

# 基金列表

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金列表                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-list`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 否 | 基金代码，精确查单只 |
| `--fund_type` | string | 否 | 基金类型，精确匹配（股票型/混合型/债券型/货币型/保本型/其他型/REITs） |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-list-paginated --fund_type 股票型 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
