---
name: fund-index-tracking-funds
description: "按指数代码查询跟踪该指数的基金。当用户需要查询跟踪某只指数（如沪深 300）的全部基金（场内 ETF + 场外联接基金），或仅场内 ETF（scope=etf）时使用。直接返回数组（非分页）。"
---

# 指数跟踪基金

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 指数跟踪基金                                                   |
| 外部接口 | `/api/v1/market/data/fund/index-fund`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--index_code` | string | 是 | 指数代码，支持裸码（如 000300）或带后缀（如 000300.SH） |
| `--scope` | string | 否 | all 全市场（默认）/ etf 仅场内 ETF |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-index-tracking-funds --index_code 000300 --scope etf
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
