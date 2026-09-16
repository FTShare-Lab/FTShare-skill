---
name: bullion-price
description: 查询贵金属价格。接口：GET /api/v1/market/data/bullion/price。所有请求必须设置 FTSHARE_API_KEY。
---

# 贵金属价格

接口：GET `/api/v1/market/data/bullion/price`。参数和响应以 `ftshare-doc/api-doc/现货数据/贵金属价格.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> bullion-price --symbol 600519.SH --start_date 20260828 --end_date 20260828 --page 1 --page_size 5 --date 20260828
```
