---
name: security-search
description: 按名称、代码或拼音搜索标的。必填 --query，可选 --limit。接口：GET /api/v1/market/security/search/。
---

# 标的搜索

按名称、代码或拼音搜索标的。必填 --query，可选 --limit。接口：GET /api/v1/market/security/search/。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> security-search --query 贵州茅台 --limit 5
```
