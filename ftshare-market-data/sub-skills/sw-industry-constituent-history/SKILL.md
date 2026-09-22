---
name: sw-industry-constituent-history
description: 查询申万行业成份股历史。接口：GET /api/v1/market/data/sw-industry/constituent-history。所有请求必须设置 FTSHARE_API_KEY。
---

# 申万行业成份股历史

接口：GET `/api/v1/market/data/sw-industry/constituent-history`。参数和响应以 `ftshare-doc/api-doc/指数专题/申万行业/申万行业成份股历史.md` 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 调用示例

```bash
python <RUN_PY> sw-industry-constituent-history --industry_code 801780.SI
python <RUN_PY> sw-industry-constituent-history --industry_code 801780.SI --stock-code 601009
```

`industry_code` 必填，须为带 `.SI` 后缀的行业代码（如 `801780.SI`）；传行业名（如 `银行`）取不到数据。`--stock-code`、`--stock-name`、`--sw-level1-code`、`--sw-level1-name` 等均为可选筛选项。该接口无分页，一次返回符合条件的全部成份股。
