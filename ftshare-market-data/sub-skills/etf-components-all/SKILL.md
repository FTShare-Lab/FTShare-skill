---
name: etf-components-all
description: 查询全部或单只 ETF 成份列表。可选 --symbol；不传返回全部 ETF。接口：GET /api/v2/market/data/etf-components-all。
---

# ETF成份列表

查询全部或单只 ETF 成份列表。可选 --symbol；不传返回全部 ETF。接口：GET /api/v2/market/data/etf-components-all。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> etf-components-all
```
