---
name: major-contract-by-date
description: 按公告日期范围查询A股重大合同信息（market.ft.tech）。用户问重大合同、某日/某月重大合同、合同金额、签约方时使用。
---

# 重大合同 - 按公告日期范围查询

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 按公告日期范围查询重大合同 |
| 外部接口 | `GET /api/v1/market/data/corporate/contract` |
| 请求方式 | GET |
| 适用场景 | 按公告日期范围查询 A 股上市公司重大合同，包括合同方、金额、收入影响等 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| start_date | string | 是 | 开始日期 | `20260526` | 格式 YYYYMMDD |
| end_date | string | 是 | 结束日期 | `20260526` | 格式 YYYYMMDD |

## 3. 响应说明

返回 `ApiResponse` 包装的 JSON 对象。

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 2,
    "items": [
      {
        "seq": 0,
        "security_code": "300209",
        "security_short_name": "行云科技",
        "signatory": "行云存算(深圳)科技有限公司",
        "signatory_rel_name": "控股子公司",
        "counter_party": "浙江甚湖科技有限公司",
        "counter_party_rel_name": "无关联关系",
        "contract_type_name": "销售合同",
        "contract_name": "设备销售框架协议",
        "amounts": "321750000.0000",
        "snd_yysr": null,
        "zsnd_yysr_bl": null,
        "operate_reve": null,
        "sign_date": null,
        "dim_rdate": "2026-05-26"
      }
    ]
  }
}
```

### data.items 元素结构

| 字段名 | 类型 | 说明 |
|--------|------|------|
| seq | int | 序号 |
| security_code | string | 股票代码 |
| security_short_name | string | 股票简称 |
| signatory | string | 签约方 |
| signatory_rel_name | string | 签约方关联名称 |
| counter_party | string | 对方签约方 |
| counter_party_rel_name | string | 对方签约方关联名称 |
| contract_type_name | string | 合同类型名称 |
| contract_name | string | 合同名称 |
| amounts | string | 合同金额（元） |
| snd_yysr | string | 上年度营业收入 |
| zsnd_yysr_bl | string | 占上年度营业收入比例 |
| operate_reve | string | 最近营业收入 |
| sign_date | string | 签约日期 |
| dim_rdate | string | 公告日期 |

## 4. 用法

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> major-contract-by-date --start_date 20260526 --end_date 20260526
```

## 5. 请求示例

```
GET /api/v1/market/data/corporate/contract?start_date=20260526&end_date=20260526
```

## 6. 注意事项

- 金额字段为 Decimal 类型，以字符串返回保持精度。
- 按 `dim_rdate` 降序排列。
