---
name: fund-risk-level-single-fund
description: "查询基金风险等级。当用户需要查询基金风险等级（低/中低/中/中高/高，对应适当性 R1-R5）及其变更历史，可按 history=true 返回全部历史或仅当前有效时使用。直接返回数组（非分页）。"
---

# 基金风险等级

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金风险等级                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-risk-level`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码（如 000001 或 000001.OF） |
| `--history` | flag | 否 | 返回全部变更历史（缺省仅当前有效） |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-risk-level-single-fund --fund_code 000001 --history
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
