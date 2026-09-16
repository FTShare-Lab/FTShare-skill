---
name: suspension-list
description: 查询停牌股票列表。可选 --trade-date。接口：GET /api/v1/market/data/suspension-list。
---

# 停牌列表

查询停牌股票列表。可选 --trade-date。接口：GET /api/v1/market/data/suspension-list。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> suspension-list
```
