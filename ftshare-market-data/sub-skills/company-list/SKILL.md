---
name: company-list
description: 查询公司列表。可选 --page、--page-size。接口：GET /api/v1/market/data/company-list。
---

# 公司列表

查询公司列表。可选 --page、--page-size。接口：GET /api/v1/market/data/company-list。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> company-list
```
