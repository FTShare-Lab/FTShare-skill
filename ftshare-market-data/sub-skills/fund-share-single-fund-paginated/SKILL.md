---
name: fund-share-single-fund-paginated
description: "按基金代码分页查询基金份额变动。当用户需要查询基金份额变动（期末/期初份额、申购赎回、份额变动率），按 stati_perd 统计周期（日/季度/年度/截止时点/半年/全部）过滤时使用。"
---

# 基金份额

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金份额                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-share`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码 |
| `--stati_perd` | string | 否 | 统计周期：日/季度/年度/截止时点/半年/全部，默认日 |
| `--start_date` | int | 否 | 开始日期 YYYYMMDD（按 trade_date 过滤） |
| `--end_date` | int | 否 | 结束日期 YYYYMMDD |
| `--page` | int | 否 | 页码，默认 1 |
| `--page_size` | int | 否 | 每页记录数，默认 50，上限 200 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-share-single-fund-paginated --fund_code 000001 --stati_perd 日 --start_date 20260101 --end_date 20260717 --page 1 --page_size 50
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
