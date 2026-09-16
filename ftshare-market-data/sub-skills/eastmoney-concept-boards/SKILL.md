---
name: eastmoney-concept-boards
description: "查询东财概念板块列表。当用户需要查询东财概念板块基础信息与成分代码列表，返回全量板块，或了解东财概念板块列表时使用。"
---

# 查询东财概念板块列表

## 接口说明

| 项目 | 说明 |
|---|---|
| 接口名称 | 查询东财概念板块列表 |
| 外部接口 | `/api/v1/market/data/eastmoney-concept-boards` |
| 请求方式 | GET |
| 适用场景 | 查询东财概念板块基础信息与成分代码列表，返回全量板块 |

## 请求参数

无需任何参数，接口返回全量概念板块列表。

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> eastmoney-concept-boards
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径，参见主 SKILL.md 的「调用方式」说明。

## 响应结构

返回值为概念板块数组（直接返回数组，非对象包装）：

```json
[
    {
        "code": "BK1024",
        "name": "绿色电力",
        "constituents": ["600089", "600905", "000591"]
    }
]
```

### 字段说明（ConceptBoard）

| 字段名 | 类型 | 是否可为空 | 说明 |
|---|---|---|---|
| `code` | String | 否 | 板块代码（BK 前缀） |
| `name` | String | 否 | 板块名称 |
| `constituents` | Array[String] | 否 | 成分标的代码列表 |

## 注意事项

- 接口直接返回数组，无分页包装结构
- 板块代码以 `BK` 开头，可用于 `eastmoney-board-daily-ohlc` 和 `eastmoney-board-latest-ohlc` 查询K线
- 成分代码不含市场后缀（如 `600089` 而非 `600089.SH`）
