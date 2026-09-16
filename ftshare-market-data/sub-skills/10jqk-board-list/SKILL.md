---
name: 10jqk-board-list
description: Get all THS board list (同花顺板块列表). Use when user asks about 同花顺板块列表、概念板块、行业板块、地域板块、证监会板块、有哪些板块.
---

# 同花顺板块列表

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 查询同花顺板块列表 |
| 外部接口 | `GET /api/v1/market/data/ths-board-list` |
| 请求方式 | GET |
| 适用场景 | 查询同花顺全部板块（概念/证监会/行业/地域）的代码与名称列表 |

## 2. 请求参数

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| 无 | - | - | - | - | 接口返回全量板块列表 |

## 3. 响应说明

成功响应外层为 `code`、`message`、`data`，板块列表位于 `data` 数组中。
|--------|------|------|
| module | string | 板块类型：`concept`（概念）/ `csrc`（证监会）/ `industry`（行业）/ `region`（地域） |
| code | string | 板块代码 |
| name | string | 板块名称 |

示例响应：
```json
{
  "code": 200,
  "message": "success",
  "data": [
    { "module": "concept", "code": "885311", "name": "5G概念" },
    { "module": "industry", "code": "881001", "name": "银行" },
    { "module": "region", "code": "883001", "name": "北京" }
  ]
}
```

## 4. 用法

```bash
python <RUN_PY> 10jqk-board-list
python <RUN_PY> 10jqk-board-list --module concept
python <RUN_PY> 10jqk-board-list --module industry
python <RUN_PY> 10jqk-board-list --search 人工智能
```

## 5. 请求示例

```
GET /api/v1/market/data/ths-board-list
```

## 6. 注意事项

- 返回四类板块（concept/csrc/industry/region），客户端按 `module` 字段过滤
- 板块代码用于后续查询 K 线等数据
