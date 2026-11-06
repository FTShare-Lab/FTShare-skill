---
name: periodic-reports
description: 查询上市公司定期报告（年报/半年报/一季报/三季报）列表，或按 url_hash 下载报告原文 PDF（market_v2_announcements_periodic_reports，GET /api/v2/market/data/announcements/periodic-reports）。用户问某公司年报/半年报/季报、某年份全市场定期报告、报告更正/修订版本、定期报告原文 PDF 时使用。支持 --stock-code、--report-type、--report-year、--document-variant、分页与 --all，以及 --url-hash 下载。
---

# 定期报告列表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 定期报告列表（market_v2_announcements_periodic_reports） |
| 外部接口 | `GET /api/v2/market/data/announcements/periodic-reports`（列表）<br>`GET /api/v2/market/data/announcements/periodic-reports/{url_hash}`（原文 PDF） |
| 请求方式 | GET（列表用 query 参数；下载为路径参数） |
| 适用场景 | 按股票、报告类型、报告年份、文件版本查询定期报告，或下载报告原文 |
| 数据范围 | 报告年份 1999 年起至今；披露日期最早 2000-01-18；当前收录 10 万余条 |

同一子 skill 两种模式：

1. **列表模式**（不带 `--url-hash`）：全部条件均可选，自由组合分页；不传条件时返回全部定期报告。
2. **下载模式**（带 `--url-hash`）：下载该报告原文 PDF 到本地。

结果按报告年份倒序、股票代码升序排列；同一报告的原文与更正、修订版全部返回，同一报告各版本相邻且最新披露在前。

## 2. 请求参数

列表模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | 否 | 股票代码 | 000001.SZ | 支持裸代码（`000001`）、短后缀（`.SH`/`.SZ`/`.BJ`）与长后缀（`.XSHG`/`.XSHE`/`.BJSE`），后缀大小写不敏感；不支持冒号格式（如 `SZ:000001`），传入返回 400 |
| report_type | string | 否 | 报告类型 | annual | `annual` 年报 / `semi_annual` 半年报 / `q1` 一季报 / `q3` 三季报；白名单外返回 400；不传返回全部四类 |
| report_year | int | 否 | 报告年份 | 2025 | 非数字或超出 0～65535 返回 400 |
| document_variant | string | 否 | 文件版本类型 | full | `full` 正式全文 / `summary` 摘要版 / `english` 英文版；白名单外返回 400；当前数据均为 `full` |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 20 | 默认 20，最大 500 |

下载模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| --url-hash | string | 是 | 报告文件哈希 | 37801609…68090432 | 取自列表响应；须为 64 位小写十六进制 |
| --output | string | 否 | 落盘路径 | ./report.pdf | 默认 `<url_hash>.pdf`；必须在当前工作目录内 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`；成功时 `code=200`、`message=success`。

`data` 为分页对象：`pageNum` / `pageSize` / `total` / `pages` / `records`；无匹配记录时 `pages` 为 0、`records` 为 `[]`。

`records` 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stock_code | string | 股票代码，统一返回 `.SH` / `.SZ` / `.BJ` 短后缀 |
| stock_name | string | 股票名称；源数据缺失时为空字符串 |
| report_year | integer | 报告年份 |
| report_type | string | 报告类型：annual / semi_annual / q1 / q3 |
| document_variant | string | 文件版本类型：full / summary / english |
| revision_type | string | 版本标识：`original` 原文 / `revised` 修订后 / `corrected` 更正后 |
| title | string | 报告公告标题 |
| publish_date | string | 披露日期，`YYYY-MM-DD` |
| url_hash | string | 报告原文下载标识 |

使用 `--all` 时输出聚合结构 `{"records": [...], "pages": N, "total": M}`，不再保留逐页信封。

## 4. 调用方式

```bash
# 按标的查询全部定期报告
python <RUN_PY> periodic-reports --stock-code 000637.SZ --page 1 --page-size 5

# 按报告类型 + 年份过滤全市场年报
python <RUN_PY> periodic-reports --report-type annual --report-year 2025 --page 1 --page-size 5

# 翻全量
python <RUN_PY> periodic-reports --stock-code 000001.SZ --all

# 下载报告原文 PDF（默认落到当前目录的 <url_hash>.pdf）
python <RUN_PY> periodic-reports --url-hash 378016094c7e1577795838e837c289b1d859508e5b86afc6d7010168d8090432

# 指定落盘路径
python <RUN_PY> periodic-reports --url-hash 378016094c7e1577795838e837c289b1d859508e5b86afc6d7010168d8090432 --output ./report.pdf
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。列表模式输出 JSON；下载模式只向 stdout 输出落盘后的文件路径。

## 5. 注意事项

- 同一报告可能返回多条版本记录（`original` / `revised` / `corrected`），接口不做仅最新版过滤；需要最新版时请自行按 `publish_date` 排序或按 `revision_type` 筛选。
- `stock_code` 不支持冒号格式（如 `SZ:000001`），传入返回 400。
- 下载用的 `url_hash` 须取自列表响应，勿硬编码；非 64 位小写十六进制会在本地直接拒绝。
- 下载过程中半成品写在 `<目标文件>.part`，成功后原子改名；失败会清理半成品。
- 落盘路径必须在当前工作目录及其子目录内，否则以非零状态退出。
