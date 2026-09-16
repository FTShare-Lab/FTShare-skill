---
name: etf-adjust-factor
description: 查询 ETF 复权因子。支持 --symbol、--trade-date 或带 symbol 的 --start-date/--end-date 区间查询，以及 --page/--page-size。接口：GET /api/v1/market/data/etf-adjust-factor。
---

# ETF复权因子

查询 ETF 复权因子。支持 --symbol、--trade-date 或带 symbol 的 --start-date/--end-date 区间查询，以及 --page/--page-size。接口：GET /api/v1/market/data/etf-adjust-factor。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> etf-adjust-factor
```
