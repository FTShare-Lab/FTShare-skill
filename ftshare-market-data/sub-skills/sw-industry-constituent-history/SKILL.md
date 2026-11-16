---
name: sw-industry-constituent-history
description: "查询单个申万行业当前有效的成份股归属记录。可用参数：--industry_code。接口：GET /api/v1/market/data/sw-industry/constituent-history。"
---

# 申万行业成份股历史

接口：GET `/api/v1/market/data/sw-industry/constituent-history`。参数和响应以 [《申万行业成份股历史》](https://market.ft.tech/gateway/doc/pages/os0w8opk.md) 为准。

请求必须从环境变量 `FTSHARE_API_KEY` 读取凭据，并通过请求头发送 `FTSHARE_API_KEY` 和 `Content-Type: application/json`；缺少凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--industry_code` | 是 | 行业代码，带 .SI 后缀，如 801010.SI |

## 返回

- 记录容器：`data.items`
- 分页字段：`total`
- 记录字段：`stockCode`、`stockName`、`inDate`、`outDate`、`swLevel1Code`、`swLevel1Name`、`swLevel2Code`、`swLevel2Name`、`swLevel3Code`、`swLevel3Name`

## 调用示例

```bash
python <RUN_PY> sw-industry-constituent-history --industry_code 801780.SI
```

`industry_code` 必填，须为带 `.SI` 后缀的行业代码（如 `801780.SI`）；传行业名（如 `银行`）取不到数据。该接口无分页，一次返回符合条件的全部成份股。
