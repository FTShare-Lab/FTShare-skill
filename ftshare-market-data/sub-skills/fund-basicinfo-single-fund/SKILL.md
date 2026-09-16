---
name: fund-basicinfo-single-fund
description: Get basic information of funds by fund code with pagination. Use when user asks about fund details, 基金基本信息, 基金管理人, 基金经理, 基金类型, 投资目标.
---

# 查询基金基础信息（分页）

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--fund-code` | string | 否 | 6 位数字基金代码；不传时返回全市场数据的默认分页 | `000001` |
| `--page` | int | 否 | 页码，从 1 开始（默认 1） | `1` |
| `--page-size` | int | 否 | 每页记录数，默认 200，最大 500 | `200` |

## 用法

通过主目录 `run.py` 调用（所有参数均可选）：

```bash
python <RUN_PY> fund-basicinfo-single-fund --fund-code 000001
python <RUN_PY> fund-basicinfo-single-fund --page 1 --page-size 200
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出分页 JSON（`items`/`page_num`/`page_size`/`total`/`pages`），`items` 中每项含 `fund_code`、`fund_name`、管理人、经理、类型、投资理念/目标/范围、业绩基准等完整字段，按用户关注点展示。

## 注意

- `fund_code` 必须是 6 位数字；不传时查询全市场数据的默认分页
- 响应为分页结构，基金档案在 `items` 数组中；需要全量数据时循环请求直到 `page > pages`
- 若用户只给基金名称，建议先用 `fund-support-symbols-all-funds-paginated` 或 `fund-overview-all-funds-paginated` 查到对应 6 位 `fund-code` 再调用本接口。
