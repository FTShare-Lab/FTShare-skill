---
name: ths-board-constituents
description: "查询同花顺板块成分股。当用户需要查同花顺概念/行业/地域/证监会板块包含哪些股票，或按板块名称、代码、类型检索成分股时使用。"
---

# 查询同花顺板块成分股

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 同花顺板块成分股 |
| 外部接口 | `/api/v1/market/data/ths-board-constituents` |
| 请求方式 | GET |
| 适用场景 | 按同花顺板块查询其成分股，覆盖概念 / 行业 / 地域 / 证监会（csrc）四类 |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|---|---|---|---|---|---|
| `board_code` | string | 否 | 板块代码 | `300082` | 概念 `300xxx`/`308xxx`/`309xxx`、行业 `881xxx`、地域 `882xxx`、csrc 为大写单字母 |
| `board_name` | string | 否 | 板块名称 | `军工` | 概念板块建议直接传名称 |
| `board_type` | string | 否 | 板块类型 | `csrc` | `industry` / `concept` / `region` / `csrc`，用于同名板块消歧 |
| `date` | string | 否 | 查询日期 | `20260915` | 格式 `YYYYMMDD`；不传返回当前成分股 |
| `page` | integer | 否 | 页码 | `1` | 从 1 开始，默认 1 |
| `page_size` | integer | 否 | 每页数量 | `100` | 默认 100，最大 1000 |

> `board_code` 与 `board_name` 至少传一个，两者都传时取交集，都不传返回 400。

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
# 概念板块（建议用名称，编号易与其它类型混淆）
python <RUN_PY> ths-board-constituents --board-name 军工

# 按代码
python <RUN_PY> ths-board-constituents --board-code 300082

# 同名板块用类型消歧
python <RUN_PY> ths-board-constituents --board-name 教育 --board-type csrc

# 截至某日的成分股，自动翻页取全量
python <RUN_PY> ths-board-constituents --board-code 300082 --date 20260915 --all
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "pageNum": 1,
        "pageSize": 100,
        "total": 551,
        "pages": 6,
        "records": [
            {
                "board_code": "300082",
                "board_name": "军工",
                "stock_code": "000009",
                "stock_name": "中国宝安"
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
| `stock_code` | String | 否 | 股票代码（6 位，不含市场后缀） |
| `stock_name` | String | 否 | 股票名称 |

## 注意事项

- 概念板块的 `board_code` 是本接口自己的编号段（`300xxx`/`308xxx`/`309xxx`）；其它编号体系的概念代码在本接口查不到，建议概念板块直接用 `board_name`，或先查一次本接口拿到回带的 `board_code`。
- 板块名称跨类型可能重名（如「教育」同时属于行业 `881178` 与 csrc `P`）；命中多个时返回 400，`message` 会列出候选，据此补 `board_type` 或改用 `board_code`。
- `date` 的语义是「截至该日最近一次采集」的成分股，非精确历史；查询日早于板块首次采集日时会抬到首次采集日并返回当天名单，不返回空。成分股进出记录自 `20260907` 起采集，无历史回填。
- 分页返回，默认 `page=1`、`page_size=100`，`page_size` 最大 1000；结果按 `stock_code` 升序。
