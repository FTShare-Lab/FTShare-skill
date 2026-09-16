---
name: stock-description-all
description: 查询 A 股股票基础信息，支持按 symbol_id 筛选和分页。用户询问股票基础资料、股票列表详情或股票代码对应公司信息时使用。接口：GET /api/v1/market/data/stock-description。
---

# 股票基础信息

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 股票基础信息 |
| 外部接口 | `/api/v1/market/data/stock-description` |
| 请求方式 | GET |
| 数据范围 | 最新股票基础信息快照，无时间维度 |

## 请求参数

| 参数 | 必选 | 说明 |
|---|---|---|
| `--symbol-id` | 否 | 股票代码，支持 `600000.SH`、`000001.SZ`、`920001.BJ`，兼容 `.XSHG`、`.XSHE`、`.BJSE` 和不带后缀的数字代码 |
| `--page` | 否 | 页码，从 1 开始，默认由服务使用 1 |
| `--page-size` | 否 | 每页条数，范围 1–200，默认 50 |

通过根目录 `run.py` 调用：

```bash
python <RUN_PY> stock-description-all --symbol-id 600000.SH --page 1 --page-size 1
python <RUN_PY> stock-description-all --page 1 --page-size 50
```

## 响应结构

成功响应固定为 `code`、`message`、`data`，其中 `data` 是分页对象：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 1,
    "total": 1,
    "pages": 1,
    "records": [{
      "symbol": "600000.SH",
      "name": "浦发银行",
      "company_name_zh": "上海浦东发展银行股份有限公司",
      "company_name_en": "Shanghai Pudong Development Bank Co., Ltd.",
      "pinyin": "pufayinhang",
      "listing_date": "1999-11-10",
      "shares": 29352080397,
      "float_a_shares": 29352080397,
      "non_float_a_shares": 0,
      "marginable": true,
      "st": false,
      "unprofitable": false,
      "status": "normal",
      "sectors": {"concept": [], "industry": null, "region": {}}
    }]
  }
}
```

`records` 还可能包含 `base_name`、`board`、`delisting_date`、`issue_price`、`bvps`、`eps_ttm`、`revenue_ttm`、`pe_ttm`、`roe_ttm`、`cum_adjust_factor`、`introduction`、`net_inflow_main` 和 `net_inflow_small`；这些字段可能为 `null`。`sectors` 包含 `concept`、`industry` 和 `region`，板块元素使用 `name_en`、`name_zh`。

## 注意事项

- 返回股票代码统一为 `代码.SH`、`代码.SZ` 或 `代码.BJ`。
- 不带后缀的数字代码按 6 位代码匹配；不同市场存在重号时建议携带交易所后缀。
- 显式传入空字符串、无法识别的后缀、`page < 1` 或 `page-size` 不在 1–200 范围内时返回 HTTP 400。
- 合法但没有匹配记录时仍返回成功响应，`records` 为空数组，`total` 和 `pages` 为 0。
