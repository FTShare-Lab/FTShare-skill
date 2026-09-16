---
name: stock-connect-members
description: 查询互联互通成份。接口：GET /api/v1/market/data/stock-connect-members。所有请求必须设置 FTSHARE_API_KEY。
---

# 互联互通成份

接口：GET `/api/v1/market/data/stock-connect-members`。参数和响应以 `ftshare-doc/api-doc/股票数据/基础数据/互联互通成份.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> stock-connect-members --direction north --channel SH --page 1
```
