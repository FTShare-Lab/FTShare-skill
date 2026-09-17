---
name: stock-prospectuses
description: 查询 A 股招股书及相关发行公告列表（stock_prospectuses，GET /api/v2/market/data/announcements/stock-prospectuses）。用户问招股书、招股说明书、招股意向书、某只股票的发行公告、某个披露日的全市场招股书、招股书文件下载标识时使用。必填 --stock-code 或 --start-date 之一；可选 --end-date、--page、--page-size、--all。
---

# 招股书列表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 招股书列表（stock_prospectuses） |
| 外部接口 | `GET /api/v2/market/data/announcements/stock-prospectuses` |
| 请求方式 | GET（query 参数） |
| 适用场景 | 按标的查单只股票的招股书及发行公告，或按披露日查全市场记录；文件可按返回的 `url_hash` 另行下载 |
| 数据范围 | 上交所、深交所、北交所公开披露的招股书及相关发行文件 |

两种模式二选一：

1. **按标的**：传 `stock_code`，查该股票的全部记录（此时忽略 `start_date` / `end_date`）。
2. **按日期**：未传 `stock_code` 时，按 `start_date` 查该披露日的全市场记录；仅支持单日。

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| stock_code | string | 二选一 | 股票代码 | 600000.SH | 支持裸代码（`600000`）、短后缀（`.SH`/`.SZ`/`.BJ`）和长后缀（`.XSHG`/`.XSHE`/`.BJSE`），后缀大小写不敏感 |
| start_date | string | 二选一 | 披露日期 | 20240517 | `YYYYMMDD`；未提供 `stock_code` 时必填，仅支持单日 |
| end_date | string | 否 | 披露日期 | 20240517 | 不填默认等于 `start_date`，传入时必须与 `start_date` 相同 |
| page | int | 否 | 页码 | 1 | 从 1 开始，默认 1 |
| page_size | int | 否 | 每页条数 | 20 | 默认 20，最大 500 |
| --all | - | 否 | 自动翻页拉全量 | - | 仅本子 skill 扩展参数，按 `pages` 翻页 |

## 3. 响应说明

外层固定为 `code`（成功 200）/ `message`（成功 `success`）/ `data`（失败为 `null`）。`data` 为分页对象：`pageNum` / `pageSize` / `total` / `pages` / `records`（无记录时 `pages` 为 0、`records` 为 `[]`）。

`records` 元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| stock_code | string | 股票代码，统一返回 `.SH` / `.SZ` / `.BJ` 短后缀 |
| stock_name | string | 股票名称；源数据未提供时为空字符串 |
| announcement_title | string | 公告标题 |
| announcement_time | string | 公告披露时间，格式 `YYYY-MM-DD HH:MM:SS` |
| column_type | string | 栏目类型，固定为 `stock` |
| url_hash | string | 文件下载标识，用于下载关联文件 |

使用 `--all` 时输出聚合结构 `{"records": [...], "pages": N, "total": M}`，不再保留逐页信封。

## 4. 调用方式

```bash
python <RUN_PY> stock-prospectuses --stock-code 600000.SH --page 1 --page-size 5
python <RUN_PY> stock-prospectuses --stock-code 600000 --page 1 --page-size 5
python <RUN_PY> stock-prospectuses --start-date 20240517 --page 1 --page-size 20
python <RUN_PY> stock-prospectuses --stock-code 600000.SH --all
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。输出 JSON；HTTP 错误输出到 stderr 并以非零状态退出。

## 5. 注意事项

- 必须提供 `stock_code` 或 `start_date` 之一，否则服务端返回 400「需要 stock_code 或 start_date 参数」（handler 会本地校验并拒绝）。
- 同时提供两者时按标的查询，`start_date` / `end_date` 被忽略。
- 按日期查询仅支持单日：`end_date` 不填默认等于 `start_date`，填了则必须相等，否则服务端返回 400。
- `page_size` 超过 500 返回 400；`--page` / `--page-size` 可不传，默认 `1` / `20`。
- `stock_name` 可能为空字符串，不是缺失字段。
- 文件下载：`GET /api/v2/market/data/announcements/stock-prospectuses/{url_hash}`，响应为附件（PDF 为 `application/pdf`，另可能为 `text/plain` 或 `text/html`）；`url_hash` 须取自本接口返回值且为 64 位小写十六进制 sha256，勿硬编码。本子 skill 不直接下载，需要时用 `curl -OJ` 取文件。