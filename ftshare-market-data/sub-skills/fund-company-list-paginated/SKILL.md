---
name: fund-company-list-paginated
description: "分页查询基金公司列表及名下基金数量。当用户需要查询基金公司名称与名下基金数量，可按公司名精确过滤时使用。"
---

# 基金公司

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金公司                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-company`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_company` | string | 否 | 基金公司名称，精确匹配 |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-company-list-paginated --fund_company 华夏基金 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
