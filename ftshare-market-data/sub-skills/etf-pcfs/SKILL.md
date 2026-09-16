---
name: etf-pcfs
description: 指定日期 ETF PCF 列表（market.ft.tech）。用户问 ETF PCF、申购赎回清单、指定日期 PCF 列表时使用。
---

# 指定日期 ETF PCF 列表 - 获取指定日期 ETF PCF 列表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 获取指定日期 ETF PCF 列表 |
| 外部接口 | `GET /api/v1/market/data/etf-pcf/etf-pcfs` |
| 请求方式 | GET |
| 适用场景 | 获取指定交易日 ETF 申购赎回清单（PCF）文件列表，支持分页，数据来自外部 PCF 服务 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| date | int | 是 | 日期 | 20260309 | YYYYMMDD 整型 |
| page | int | 否 | 页码，从 1 开始 | 1 | 默认 1 |
| page_size | int | 否 | 每页记录数 | 20 | 默认 20，最大 100 |

## 3. 响应说明

返回分页的 PCF 文件列表。

```json
{
  "total": 850,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "etf_code": 159003,
      "date": 20260309,
      "filename": "pcf_159003_20260309.xml"
    },
    {
      "etf_code": 159005,
      "date": 20260309,
      "filename": "pcf_159005_20260309.xml"
    }
  ]
}
```

### EtfPcfItem 字段

| 字段名 | 类型 | 是否可为空 | 说明 |
|--------|------|------------|------|
| etf_code | int | 否 | ETF 代码 |
| date | int | 否 | 日期 YYYYMMDD |
| filename | string | 否 | PCF 文件名，如 pcf_159152_20260316.xml |

## 4. 用法

通过主目录 `run.py` 调用（必填 `--date`，可选 `--page`、`--page_size`）：

```bash
python <RUN_PY> etf-pcfs --date 20260309
python <RUN_PY> etf-pcfs --date 20260309 --page 1 --page_size 20
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON；本接口无需额外请求头。

## 5. 请求示例

```
GET /api/v1/market/data/etf-pcf/etf-pcfs?date=20260309&page=1&page_size=20
```

## 6. 注意事项

- `date` 为 YYYYMMDD 整型（如 20260309），需为交易日
- `page_size` 最大 100
- 无数据时 `items` 为空数组，`total` 为 0
