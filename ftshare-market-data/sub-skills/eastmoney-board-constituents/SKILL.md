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
| 适用场景 | 查询指定东财板块的成分股代码和名称，支持按日期回溯历史成分 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `board_code` | string | 是 | 板块代码 | `BK0475` | BK 前缀，取东方财富板块代码；可先查 `eastmoney-concept-boards` 拿板块代码 |
| `date` | string | 否 | 查询日期 | `20260930` | 格式 `YYYYMMDD`；不传返回当前仍在板块内的成分股 |
| `page` | integer | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `page_size` | integer | 否 | 每页数量 | `200` | 默认 200，最大 500 |

> `date` 的口径是「截至该日仍在板块内」：查询日早于该板块首次采集日时，会抬到首次采集日并返回当天的在籍名单，不返回空。成分股进出记录自 `20260929` 起采集，无历史回填。

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 查询银行板块当前成分股
python <RUN_PY> eastmoney-board-constituents --board_code BK0475

# 截至某日的成分股
python <RUN_PY> eastmoney-board-constituents --board_code BK0490 --date 20260930

# 翻页取大板块（如广东板块 905 只）
python <RUN_PY> eastmoney-board-constituents --board_code BK0153 --page 2 --page_size 200

# 自动翻页取全量
python <RUN_PY> eastmoney-board-constituents --board_code BK0153 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "pageNum": 1,
        "pageSize": 200,
        "total": 42,
        "pages": 1,
        "records": [
            {
                "board_code": "BK0475",
                "board_name": "银行Ⅱ",
                "board_type": "industry",
                "level": 2,
                "stock_code": "000001",
                "stock_name": "平安银行"
            }
        ]
    }
}
```

### 字段说明

`data` 为分页对象，含 `pageNum`、`pageSize`、`total`、`pages` 与 `records`。

### records 元素字段说明

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `board_code` | String | 否 | 板块代码 |
| `board_name` | String | 否 | 板块名称 |
| `board_type` | String | 否 | 板块类型：`industry` 行业 / `concept` 概念 / `regional` 地域 |
| `level` | Integer | 是 | 行业层级：`1` 一级 / `2` 二级 / `3` 三级；概念、地域板块为 `null` |
| `stock_code` | String | 否 | 股票代码（6 位，不含市场后缀） |
| `stock_name` | String | 否 | 股票名称 |

## 注意事项

- 分页返回，默认 `page=1`、`page_size=200`，`page_size` 最大 500；结果按 `stock_code` 升序。
- `board_type` 中地域取值的拼写是 `regional`，不是 `region`。
- `stock_code` 不含市场后缀（如 `000001` 而非 `000001.SZ`）。
- 不传 `date` 时结果中不含已退出的个股。
