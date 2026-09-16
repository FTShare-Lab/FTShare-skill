---
name: eastmoney-board-constituents
description: "查询东财板块成分股。当用户需要查询指定东财板块的全部成分股代码和名称，或了解东财板块成分股时使用。"
---

# 查询东财板块成分股

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财板块成分股 |
| 外部接口 | `/api/v1/market/data/eastmoney-board-constituents` |
| 请求方式 | GET |
| 适用场景 | 查询指定东财板块的全部成分股代码和名称 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `board_code` | string | 是 | 板块代码 | `BK1024` | BK 前缀，可通过 `eastmoney-concept-boards` 或 `eastmoney-board-latest-ohlc` 获取 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 查询绿色电力板块成分股
python <RUN_PY> eastmoney-board-constituents --board_code BK1024

# 查询工程建设板块成分股
python <RUN_PY> eastmoney-board-constituents --board_code BK0425
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "board_code": "BK1024",
    "board_name": "绿色电力",
    "constituents": [
        {
            "stock_code": "600905",
            "stock_name": "三峡能源"
        },
        {
            "stock_code": "601016",
            "stock_name": "节能风电"
        }
    ]
}
```

### 字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `board_code` | String | 否 | 板块代码 |
| `board_name` | String | 否 | 板块名称 |
| `constituents` | Array | 否 | 成分股列表 |

### constituents 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `stock_code` | String | 否 | 股票代码（不含市场后缀） |
| `stock_name` | String | 否 | 股票名称 |

## 注意事项

- 接口返回指定板块的全量成分股，无分页
- `stock_code` 不含市场后缀（如 `600905` 而非 `600905.SH`）
- 板块代码对行业板块和概念板块通用
