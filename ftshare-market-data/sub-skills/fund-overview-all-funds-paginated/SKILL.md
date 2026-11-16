---
name: fund-overview-all-funds-paginated
description: Get paginated overview information for all funds. Use when user asks about 基金概览, 所有基金信息, fund overview list, 基金列表概况.
---

# 查询所有基金概览信息（分页）

接口：`GET /api/v1/market/data/fund/fund-overview`。在线文档：[《基金总览》](https://market.ft.tech/gateway/doc/pages/gt3vpuzr.md)

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--page` | int | 否 | 页码，从 1 开始（默认 1） | `1` |
| `--page-size` | int | 否 | 每页记录数，最大 1000（默认 20） | `20` |

## 用法

通过主目录 `run.py` 调用（可选 `--page`、`--page-size`）：

```bash
python <RUN_PY> fund-overview-all-funds-paginated --page 1 --page-size 20
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出带分页信息的 JSON，每项含基金代码、基金名称、基金类型、规模等概览字段，以表格展示给用户。

## 注意

- 需要全量数据时，循环请求直到 `page > total_pages`
- `page-size` 最大不超过 1000
