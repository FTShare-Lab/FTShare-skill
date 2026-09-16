---
name: ashare-news-sentiment-factors
description: 查询指定 A 股的新闻情绪因子。必填 --trade-code；可选 --start-date、--end-date、--page、--page-size。接口：GET /api/v3/market/data/ashare-news-sentiment-factors。
---

# A股新闻情绪因子

查询指定 A 股的新闻情绪因子。必填 --trade-code；可选 --start-date、--end-date、--page、--page-size。接口：GET /api/v3/market/data/ashare-news-sentiment-factors。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

通过主目录 `run.py` 调用：

```bash
python <RUN_PY> ashare-news-sentiment-factors --trade-code 600000.SH
```
