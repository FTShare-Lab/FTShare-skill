---
name: etf-announcements
description: 查询 ETF 公告列表（etf_announcements），或按 url_hash 下载公告正文 PDF。用户问 ETF 公告、基金公告、ETF 中期报告/年报公告、按日期查全市场 ETF 公告、要公告原文 PDF 时使用。
---

# ETF 公告列表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | ETF 公告列表（etf_announcements） |
| 外部接口 | `GET /api/v2/market/data/announcements/etf-announcements`（列表）<br>`GET /api/v2/market/data/announcements/etf-announcements/{url_hash}`（正文 PDF） |
| 请求方式 | GET（列表用 query 参数；下载为路径参数） |
| 适用场景 | 按标的查单只 ETF 全部公告，或按单日日期查全市场 ETF 公告；拿到 `url_hash` 后可下载公告正文 PDF |

同一个子 skill 三种模式：

1. **按标的**：传 `etf_code`，查单只 ETF 所有公告。
2. **按日期**：传 `start_date`（必须等于 `end_date`，仅支持单日），查指定日期全市场 ETF 公告。
3. **下载正文**：传 `--url-hash`，下载该公告的正文 PDF 到本地（`url_hash` 取自列表响应）。

## 2. 请求参数

列表模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| etf_code | string | 二选一 | ETF 代码 | 159915 | 支持裸代码/短后缀/长后缀（`159915.SZ`、`510300.XSHG`），大小写不敏感 |
| start_date | string | 二选一 | 日期 | 20260831 | YYYYMMDD；按日期查询时必填，仅支持单日 |
| end_date | string | 否 | 日期 | 20260831 | 不填默认等于 `start_date`，且必须等于 `start_date` |
| page | int | 是 | 页码 | 1 | 必填 |
| page_size | int | 是 | 每页条数 | 5 | 必填 |
| --all | - | 否 | 自动翻页拉全量 | - | 仅本子 skill 扩展参数 |

下载模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| --url-hash | string | 是 | 公告文件 URL 哈希 | d8d54544…cf574adf | 取自列表响应；传入即下载 |
| --output | string | 否 | 落盘路径 | ./etf.pdf | 默认 `<url_hash>.pdf`；必须在当前工作目录内 |

## 3. 响应说明

外层固定为 `code` / `message` / `data`。`data` 为分页对象：`pageNum` / `pageSize` / `total` / `pages` / `records`。

records 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| etf_code | string | ETF 代码，6 位裸代码，不带交易所后缀 |
| etf_name | string | ETF 名称 |
| announcement_id | string | 公告 id |
| announcement_title | string | 公告标题 |
| announcement_time | string | 公告时间，格式 YYYY-MM-DD HH:MM:SS |
| url_hash | string | 公告文件 URL 哈希，用于下载正文文件 |

## 4. 调用方式

```bash
python <RUN_PY> etf-announcements --etf-code 159915 --page 1 --page-size 5
python <RUN_PY> etf-announcements --start-date 20260831 --page 1 --page-size 20
python <RUN_PY> etf-announcements --etf-code 159915 --page 1 --page-size 20 --all

# 下载正文 PDF（默认落到当前目录的 <url_hash>.pdf）
python <RUN_PY> etf-announcements --url-hash d8d54544...cf574adf --output ./etf.pdf
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。列表模式输出 JSON；下载模式只向 stdout 输出落盘后的文件路径。HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 必须提供 `etf_code` 或 `start_date` 之一，否则服务端报错（handler 会本地校验并拒绝）。
- 按日期查询仅支持单日：`end_date` 不填默认等于 `start_date`，填了则必须相等。
- ETF 范围为场内 ETF，不含联接基金、LOF。
- 下载用的 `url_hash` 须取自列表响应，勿硬编码。
- 下载过程中半成品写在 `<目标文件>.part`，成功后原子改名；失败会清理半成品。落盘路径必须在当前工作目录及其子目录内，否则以非零状态退出。
- 当前数据源仅覆盖深市 ETF（`159` 开头）；查询沪市代码会返回空列表。
