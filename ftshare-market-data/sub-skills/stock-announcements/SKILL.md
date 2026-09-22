---
name: stock-announcements
description: 查询 A 股公告列表，或按 url_hash 下载公告正文 PDF。用户问某只股票的公告、按日期查全市场公告、要公告原文 PDF 时使用。
---

# A 股公告列表 / 公告正文下载

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | A 股公告（stock_announcements / stock_announcements_download） |
| 外部接口 | `GET /api/v2/market/data/announcements/stock-announcements`（列表）<br>`GET /api/v2/market/data/announcements/stock-announcements/{url_hash}`（正文 PDF） |
| 请求方式 | GET（列表用 query 参数；下载为路径参数） |

同一个子 skill 两种模式：

1. **列表模式**（不带 `--url-hash`）：按标的或日期查公告列表。
2. **下载模式**（带 `--url-hash`）：下载该公告的正文 PDF 到本地。

必须提供 `--stock-code` 或 `--start-date`，`--type` 当前固定为 `stock`，列表模式下 `--page` 与 `--page-size` 必填。按日期范围查询时日期跨度最多 3 天。所有请求必须设置环境变量 `FTSHARE_API_KEY`；缺失凭据时不会发起请求。

## 2. 请求参数

列表模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 |
|--------|------|----------|------|----------|
| stock_code | string | 二选一 | 股票代码 | 002142.XSHE |
| start_date | string | 二选一 | 起始日期 | 20260908 |
| end_date | string | 否 | 结束日期 | 20260908 |
| type | string | 否 | 公告类型，固定 `stock` | stock |
| page | int | 是 | 页码 | 1 |
| page_size | int | 是 | 每页条数 | 5 |

下载模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| --url-hash | string | 是 | 公告文件 URL 哈希 | d8d54544…cf574adf | 取自列表响应；传入即下载 |
| --output | string | 否 | 落盘路径 | ./ann.pdf | 默认 `<url_hash>.pdf`；必须在当前工作目录内 |

## 3. 调用方式

```bash
# 列表
python <RUN_PY> stock-announcements --start-date 20260918 --end-date 20260918 --page 1 --page-size 5

# 下载正文 PDF（默认落到当前目录的 <url_hash>.pdf）
python <RUN_PY> stock-announcements --url-hash d8d54544...cf574adf

# 指定落盘路径
python <RUN_PY> stock-announcements --url-hash d8d54544...cf574adf --output ./ann.pdf
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。列表模式输出 JSON；下载模式只向 stdout 输出落盘后的文件路径。

## 4. 注意事项

- 下载用的 `url_hash` 须取自列表响应，勿硬编码。
- 下载过程中半成品写在 `<目标文件>.part`，成功后原子改名；失败会清理半成品。
- 落盘路径必须在当前工作目录及其子目录内，否则以非零状态退出。
- 下载失败（HTTP 错误、网络异常、响应地址跳出基础地址）以非零状态退出并清理半成品。
