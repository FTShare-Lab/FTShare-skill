---
name: fund-fee-single-fund-paginated
description: "查询基金费率（当前有效，分页）。当用户需要查询基金日常申购费/赎回费/认购费/管理费/托管费/销售服务费，可按 charge_type 费率类型与 client_type 客户类型过滤时使用。"
---

# 基金费率

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金费率                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-fee`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码（如 000001 或 000001.OF） |
| `--charge_type` | string | 否 | 费率类型：日常申购费/日常赎回费/认购费/管理费/托管费/销售服务费 |
| `--client_type` | string | 否 | 客户类型：一般/机构/养老金/REITs |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-fee-single-fund-paginated --fund_code 000001 --charge_type 日常申购费 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
