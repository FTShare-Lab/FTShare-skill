---
name: fund-manager-relationship
description: "按基金代码查历任/现任基金经理，或按基金经理姓名查其管理过的任职关系。当用户需要查基金经理姓名、职务、任职/离任日期、是否在任等，按 fund_code 或 fund_manager 二选一查询时使用。"
---

# 基金经理任职关系

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金经理任职关系                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-manager`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 否 | 基金代码（与 fund_manager 二选一） |
| `--fund_manager` | string | 否 | 基金经理姓名（与 fund_code 二选一） |
| `--is_inoffice` | string | 否 | 1 在任 / 0 离任 |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-manager-relationship --fund_code 000001 --is_inoffice 1
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
