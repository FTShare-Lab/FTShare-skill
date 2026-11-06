---
name: market-announcements
description: 查询全市场上市公司公告列表，或按 url_hash 下载公告原文 PDF（market_v2_announcements_market_announcements，GET /api/v2/market/data/announcements/market-announcements）。用户问全市场公告、按关键字/公告分类/时间窗/股票代码/板块/栏目查公告、要公告原文 PDF 时使用。支持 --keyword、--category、--stock-code、--start-date/--end-date、--plate、--column-type、分页与 --all，以及 --url-hash 下载。
---

# 全市场公告列表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 全市场公告列表（market_v2_announcements_market_announcements） |
| 外部接口 | `GET /api/v2/market/data/announcements/market-announcements`（列表）<br>`GET /api/v2/market/data/announcements/market-announcements/{url_hash}`（正文 PDF） |
| 请求方式 | GET（列表用 query 参数；下载为路径参数） |
| 适用场景 | 跨全市场按关键字、公告分类、时间窗、股票代码、板块、栏目筛选公告，或下载公告原文 |
| 数据范围 | 公告披露时间 2026-01-01 起至今；当前收录 50 万余条 |

同一子 skill 两种模式：

1. **列表模式**（不带 `--url-hash`）：全部条件均可选，自由组合分页；不传条件时返回全量公告并分页。
2. **下载模式**（带 `--url-hash`）：下载该公告的正文 PDF 到本地。

## 2. 请求参数

列表模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| keyword | string | 否 | 公告标题关键字 | 回购 | 子串匹配；去首尾空格后最长 60 字符，超出返回 400；`%`、`_` 按字面量处理 |
| category | string | 否 | 公告分类，逗号分隔多选 | annual,semi_annual | 22 个允许值：annual、semi_annual、q1、q3、earnings_forecast、daily_operations、board、shareholders_meeting、governance、intermediary、related_transaction、major_restructuring、issuance、equity_change、dividend、borrowing_credit、convertible_bond、major_contract、risk_warning、hedging、independent_director、other_financing |
| stock_code | string | 否 | 股票代码 | 000001.SZ | 支持裸代码（`000001`）、短后缀（`.SH`/`.SZ`/`.BJ`）、长后缀（`.XSHG`/`.XSHE`/`.BJSE`）与冒号格式（`SZ:000001`），后缀大小写不敏感 |
| start_date | string | 否 | 起始日期 | 20261001 | `YYYYMMDD`；单独提供时查询该单日；两日期都不传时默认最近 3 年滚动窗口 |
| end_date | string | 否 | 结束日期 | 20261031 | `YYYYMMDD`；不能单独提供，须与 `start_date` 成对使用，且不得早于 `start_date` |
| plate | string | 否 | 板块，逗号分隔多选 | sh,sz_chi_next | `sh` 上海主板 / `sz` 深圳主板 / `sz_chi_next` 创业板 / `sh_star` 科创板 / `bj` 北交所 |
| column_type | string | 否 | 栏目，逗号分隔多选 | stock | `stock` / `hke` / `fund` / `bond`；当前仅 `stock` 有数据 |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 20 | 默认 20，最大 500 |

下载模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| --url-hash | string | 是 | 公告文件哈希 | 7d3176c8…c846f8dfbc | 取自列表响应；须为 64 位小写十六进制 |
| --output | string | 否 | 落盘路径 | ./ann.pdf | 默认 `<url_hash>.pdf`；必须在当前工作目录内 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`；成功时 `code=200`、`message=success`。

`data` 为分页对象：`pageNum` / `pageSize` / `total` / `pages` / `records`；无匹配记录时 `pages` 为 0、`records` 为 `[]`。

`records` 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stock_code | string | 股票代码，统一返回 `.SH` / `.SZ` / `.BJ` 短后缀 |
| stock_name | string | 股票名称 |
| announcement_title | string | 公告标题 |
| announcement_time | string | 公告披露时间（北京时间），`YYYY-MM-DD HH:MM:SS` |
| categories | array | 分类值数组；一般为 category 允许值，可为空数组 |
| plate | string | 板块值 |
| column_type | string | 栏目类型 |
| url_hash | string | 公告原文下载标识 |

使用 `--all` 时输出聚合结构 `{"records": [...], "pages": N, "total": M}`，不再保留逐页信封。

## 4. 调用方式

```bash
# 全量公告首页（按公告时间倒序）
python <RUN_PY> market-announcements --page 1 --page-size 5

# 分类多选 + 时间窗
python <RUN_PY> market-announcements --category annual,semi_annual --start-date 20261001 --end-date 20261031 --page 1 --page-size 5

# 按标的
python <RUN_PY> market-announcements --stock-code 000001.SZ --page 1 --page-size 5

# 翻全量
python <RUN_PY> market-announcements --keyword 回购 --all

# 下载正文 PDF（默认落到当前目录的 <url_hash>.pdf）
python <RUN_PY> market-announcements --url-hash 7d3176c830063b63dbee6e93d24c3d0b5d82714b15dd7523716023c846f8dfbc

# 指定落盘路径
python <RUN_PY> market-announcements --url-hash 7d3176c830063b63dbee6e93d24c3d0b5d82714b15dd7523716023c846f8dfbc --output ./ann.pdf
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。列表模式输出 JSON；下载模式只向 stdout 输出落盘后的文件路径。

## 5. 注意事项

- 下载用的 `url_hash` 须取自列表响应，勿硬编码；非 64 位小写十六进制会在本地直接拒绝。
- 下载过程中半成品写在 `<目标文件>.part`，成功后原子改名；失败会清理半成品。
- 落盘路径必须在当前工作目录及其子目录内，否则以非零状态退出。
- 无匹配记录返回空结果（`pages=0`、`records=[]`），不是请求失败。
- `--all` 会连续请求所有分页；数据量较大（50 万余条）时耗时明显，建议先用条件收窄。
