---
name: fund-holder-structure-single-fund
description: "查询基金持有人结构（按报告期）。当用户需要查询基金持有人户数、户均持有份额、机构/个人/前十大持有人份额与比例等，可按 report_type 与 start_date/end_date 过滤时使用。直接返回数组（非分页）。"
---

# 基金持有人结构

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金持有人结构                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-holder-structure`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码（如 000001 或 000001.OF） |
| `--report_type` | string | 否 | 报告类型：年度报告/中期报告/上市公告书/基金合同生效公告，缺省全部 |
| `--start_date` | int | 否 | 报告期起始日期 YYYYMMDD |
| `--end_date` | int | 否 | 报告期截止日期 YYYYMMDD |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-holder-structure-single-fund --fund_code 000001 --report_type 年度报告
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
