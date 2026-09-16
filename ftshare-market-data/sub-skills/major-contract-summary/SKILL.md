---
name: major-contract-summary
description: 近一年A股个股重大合同汇总排名（market.ft.tech）。用户问重大合同排行榜、哪些公司签合同最多/金额最大、合同总额排名时使用。
---

# 重大合同 - 近一年个股汇总

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 近一年个股重大合同汇总 |
| 外部接口 | `GET /api/v1/market/data/corporate/contract/summary` |
| 请求方式 | GET |
| 适用场景 | 近一年各股票重大合同数量与金额汇总排名，按合同总额降序，支持分页 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| page | int | 否 | 页码，从 1 开始 | `1` | 默认 1 |
| page_size | int | 否 | 每页数量 | `50` | 默认 50，最大 200 |

## 3. 响应说明

返回 `PaginatedApiResponse` 包装的 JSON 对象。

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pageNum": 1,
    "pageSize": 50,
    "total": 35,
    "pages": 1,
    "records": [
      {
        "seq": 0,
        "security_code": "002307",
        "security_short_name": "北新路桥",
        "contract_count": "1",
        "total_amount": "3249000000.0000",
        "prev_year_total": "3249000000.0000",
        "last_year_revenue": null,
        "revenue_ratio": null,
        "latest_revenue": null
      }
    ]
  }
}
```

### data.records 元素结构

| 字段名 | 类型 | 说明 |
|--------|------|------|
| seq | int | 序号 |
| security_code | string | 股票代码 |
| security_short_name | string | 股票简称 |
| contract_count | string | 重大合同签署数量 |
| total_amount | string | 合同金额总计（元） |
| prev_year_total | string | 上年度合同金额总计（元） |
| last_year_revenue | string | 上年度营业收入（元） |
| revenue_ratio | string | 占上年营业收入比例（%） |
| latest_revenue | string | 最新财务报表营业收入（元） |

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> major-contract-summary
python <RUN_PY> major-contract-summary --page 1 --page_size 50
```

## 5. 请求示例

```
GET /api/v1/market/data/corporate/contract/summary?page=1&page_size=50
```

## 6. 注意事项

- 近一年范围 = `dim_rdate >= DATE_SUB(NOW(), INTERVAL 1 YEAR)`。
- 按合同总额降序排列。
