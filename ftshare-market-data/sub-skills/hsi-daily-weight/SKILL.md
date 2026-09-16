---
name: hsi-daily-weight
description: 查询恒生系列指数成份股权重（HSI 恒生指数 / HSCEI 国企指数 / HSAIT 等）。按交易日/日期范围/指数/股票过滤。Use when user asks about 港股指数权重, 恒生指数成份股权重, 国企指数权重, 恒生科技权重, hsi daily weight, 港股权重. 注意：HSAIT 的"恒生科技"映射存疑（见注意事项），HSI/HSCEI 可用。
---

# 查询恒生系列指数成份股权重

## 接口说明

| 项目 | 说明 |
|------|------|
| 接口名称 | 对外接口-查询恒生指数成分权重 |
| 接口列表 | `hsi-daily-weight` |
| 外部接口 | GET /api/v1/market/data/hk/hsi-daily-weight |
| 请求方式 | GET |
| 适用场景 | 查询恒生系列指数成份股的权重数据，支持按交易日、日期范围、指数代码、股票代码过滤。 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| trade_date | int | 否 | 交易日 | 20260529 | YYYYMMDD；**与 start_date/end_date 互斥** |
| start_date | int | 否 | 交易日下界 | 20260501 | YYYYMMDD；须与 end_date 同时提供 |
| end_date | int | 否 | 交易日上界 | 20260529 | YYYYMMDD；须与 start_date 同时提供 |
| index_slug | string | 否 | 指数代码（大小写不敏感） | HSI | `HSI`(恒生)/`HSCEI`(国企)/`HSAIT`(见注意) |
| stock_code | string | 否 | 4 位港股代码 | 0700 | 如 `0700`(腾讯)，**4 位非 5 位** |
| page / page_size | int | 否 | 分页 | 1 / 50 | 默认 1 / 50，page_size 最大 200 |

> **至少需要一个过滤条件**：`trade_date`、`start_date`+`end_date`、`index_slug`、`stock_code`，否则 400。

## 执行方式

```bash
# 恒生指数 HSI 某日成份权重（先按指数取，再按最新交易日筛）
python scripts/handler.py --index_slug HSI --page 1 --page_size 200
# 某日某指数成份权重
python scripts/handler.py --trade_date 20260529 --index_slug HSCEI
# 某股票在各指数的权重历史
python scripts/handler.py --stock_code 0700
# 日期范围 + 指数
python scripts/handler.py --start_date 20260501 --end_date 20260529 --index_slug HSI
```

## 响应结构（信封：code/message/data.records）

```json
{
  "code": 0, "message": "success",
  "data": {
    "pageNum": 1, "pageSize": 50, "total": 90, "pages": 2,
    "records": [
      { "trade_date": "2026-05-29", "index_slug": "hsi", "index_name": "hsi",
        "stock_code": "0700", "stock_name": "TENCENT 騰訊控股", "weight_pct": "8.4",
        "source_file": "con_29May26.pdf", "url_hash": "...", "processed_at": "2026-05-29 19:34:36" }
    ]
  }
}
```

> ⚠️ 数据在 `data.records`，**不是顶层数组**。

### records 字段

| 字段 | 说明 |
|---|---|
| trade_date | 交易日 YYYY-MM-DD |
| index_slug | 指数代码（小写，如 `hsi`/`hscei`/`hsait`） |
| index_name | 当前与 index_slug 相同（小写代码，非中文名） |
| stock_code | 4 位港股代码（`0700`，非 `00700`） |
| stock_name | 股票名称（多为英文/繁体，如 `TENCENT 騰訊控股`） |
| weight_pct | 权重百分比，**字符串**（如 `"8.4"`）；未缩放，直接是百分数 |
| source_file / url_hash / processed_at | 来源文件 / URL 哈希 / 处理时间 |

## 注意事项

- **⚠️ `HSAIT` 的"恒生科技"映射存疑（实测发现，2026-05-29 验证）**：
  - 文档称 `HSAIT = 恒生科技指数`，但实测返回 **40 只成份股**，且**中国移动(0941)以 10.86% 排第一**。
  - 官方恒生科技指数(HSTECH)为 **30 只**、**8% 个股权重上限**、**不含中国移动**——三点均不符。
  - → **勿将 `HSAIT` 直接当作恒生科技指数权重**。其真实对应指数未确定（可能为恒生港股通科技/综合类）。需数据团队核对 `index_slug` 映射或上游 PDF 解析。
  - 另：kline 接口里恒生科技叫 `HSTECH`，与本接口的 `HSAIT` 命名不一致。
- **`HSI` / `HSCEI` 权重可用**：HSI 实测返回 ~90 只成份股（恒指规模相符），Top 为汇丰/阿里/腾讯/友邦/建行，合理。
- `weight_pct` 是字符串百分数（**未做 ×1e4 缩放**，与港股财报的金额缩放不同）。
- `stock_code` 为 **4 位**（`0700`，非 `00700`/`00700.HK`）。
- `index_slug` 大小写不敏感，响应中始终返回小写。
- `trade_date` 与 `start_date`/`end_date` 互斥；`start_date`/`end_date` 必须成对且 `start_date ≤ end_date`。
- 排序：`trade_date DESC, index_slug, stock_code`。
- HTTP 恒为 200，业务错误通过 `code`/`message` 携带（非 0 为错误）；高频调用建议用 `trade_date` 精确过滤。

## 调用示例

```bash
python <RUN_PY> hsi-daily-weight --trade_date 20260821 --index_slug HSI --page 1
```
