---
name: stock-ggmx-buy-ranking
description: 查询董监高增持排行。可选 --time-range（1m/3m/6m/1y/2y）、--page、--page-size。接口：GET /api/v2/market/data/holder/stock-ggmx-buy-ranking。
---

# 董监高增持排名

查询董监高增持排行。可选 --time-range（1m/3m/6m/1y/2y）、--page、--page-size。接口：GET /api/v2/market/data/holder/stock-ggmx-buy-ranking。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-ggmx-buy-ranking
```
