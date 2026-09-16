---
name: fund-support-symbols-all-funds-paginated
description: Get paginated list of all supported fund symbols with code and name. Use when user asks about 支持的基金列表, 基金代码清单, 所有基金标的.
---

# 查询所有支持基金的标的列表（分页）

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--page` | int | 否 | 页码，从 1 开始（默认 1） | `1` |
| `--page-size` | int | 否 | 每页记录数，最大 1000（默认 20） | `20` |

## 用法

通过主目录 `run.py` 调用（可选 `--page`、`--page-size`）：

```bash
python <RUN_PY> fund-support-symbols-all-funds-paginated --page 1 --page-size 20
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出带分页信息的 JSON，每项含 `fund_code`（基金代码）和 `fund_name`（基金名称），以表格展示。

## 注意

- 需要全量数据时，循环请求直到 `page > total_pages`
- `page-size` 最大不超过 1000
