---
name: ths-industry-constituents
description: 查询同花顺行业成分股列表。当用户需要查询指定同花顺行业的全部成分股代码和名称，或按股票代码/名称反查所属同花顺行业时使用。Use when user asks about 同花顺行业成分股, THS industry constituents, 行业成分关系.
---

# 查询同花顺行业成分股列表

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--industry-code` | string | 否 | 同花顺行业代码，精确匹配 | `881157` |
| `--industry-name` | string | 否 | 同花顺行业名称，精确匹配 | `证券` |
| `--stock-code` | string | 否 | 股票代码，精确匹配 | `600905` |
| `--stock-name` | string | 否 | 股票名称，精确匹配 | `三峡能源` |
| `--page` | int | 否 | 页码，从 1 开始（默认 1） | `1` |
| `--page-size` | int | 否 | 每页数量，默认 100，最大 1000 | `100` |

筛选参数均为精确匹配，可单独或组合使用；均不传时返回最新一期全部行业成分关系。结果按 `industry_code`、`stock_code` 升序。

## 用法

通过主目录 `run.py` 调用（所有参数均可选）：

```bash
# 按行业名称查成分股
python <RUN_PY> ths-industry-constituents --industry-name 证券

# 按行业代码分页获取
python <RUN_PY> ths-industry-constituents --industry-code 881157 --page 1 --page-size 1000

# 按股票反查所属行业
python <RUN_PY> ths-industry-constituents --stock-code 600905
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出分页 JSON（`records`/`pageNum`/`pageSize`/`total`/`pages`），`records` 中每项含 `industry_code`、`industry_name`、`stock_code`、`stock_name`，以表格展示。

## 注意

- 接口始终返回数据源中的最新一期快照，无需传日期
- 需要全量数据时，循环请求直到 `page > pages`
- 筛选参数不能是空白字符串，否则服务端拒绝
