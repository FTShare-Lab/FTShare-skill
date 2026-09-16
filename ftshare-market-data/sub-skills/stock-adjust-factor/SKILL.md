---
name: stock-adjust-factor
description: 查询股票复权因子。支持 --symbol、--trade-date、--start-date、--end-date、--page、--page-size。接口：GET /api/v1/market/data/stock-adjust-factor。
---

# 股票复权因子

查询股票复权因子。支持 --symbol、--trade-date、--start-date、--end-date、--page、--page-size。接口：GET /api/v1/market/data/stock-adjust-factor。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> stock-adjust-factor
```
