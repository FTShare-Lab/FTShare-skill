---
name: bse-mapping
description: 查询北交所代码映射。可选 --o-code。接口：GET /api/v1/market/data/bse-mapping。
---

# 北交所映射

查询北交所代码映射。可选 --o-code。接口：GET /api/v1/market/data/bse-mapping。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> bse-mapping
```
