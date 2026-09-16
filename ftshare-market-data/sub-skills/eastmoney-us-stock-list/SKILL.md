---
name: eastmoney-us-stock-list
description: 查询东方财富美股列表。Use when user asks for 美股列表、东财美股股票清单或美股代码。
---

# 东方财富美股列表

接口：`GET /api/v1/market/data/eastmoney-us-stock-list`。获取东方财富美股最新快照，支持刷新和分页。

## 调用示例

```bash
python <RUN_PY> eastmoney-us-stock-list --page 1 --page-size 5
python <RUN_PY> eastmoney-us-stock-list --refresh --page 1 --page-size 10
python <RUN_PY> eastmoney-us-stock-list --all
```

## 参数

- `--refresh`：刷新列表缓存，可选。
- `--page`：页码，从 1 开始，默认 1。
- `--page-size`：每页数量，可选。
- `--all`：自动翻页并合并全部记录。

响应为 `code/message/data` 信封，分页记录位于 `data.records`，字段包括 `secid`、`market`、`code`、`name`、`market_value_usd`、`latest_price`、`change_pct`、`volume`、`amount`、`pe_ttm`。数值字段按字符串返回；`secid` 示例为 `105.ADV`。
