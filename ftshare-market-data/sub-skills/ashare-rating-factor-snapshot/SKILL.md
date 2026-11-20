---
name: ashare-rating-factor-snapshot
description: 查询 A 股相关性快照。用户询问股票相关性、相关公司、相关股票排名或相关性评分时使用。传 --trade-code 查单只股票的相关公司，不传则分页遍历全市场。接口：GET /api/v3/market/data/ashare-rating-factor-snapshot。
---

# A股相关性 Top-K

接口：`GET /api/v3/market/data/ashare-rating-factor-snapshot`。在线文档：[《A股相关性 Top-K》](https://market.ft.tech/gateway/doc/pages/hdns2u7u.md)

指定股票时返回该股票的相关公司列表，不指定时返回当日全市场股票的相关公司列表。每个交易日更新一份快照。

所有请求必须设置环境变量 `FTSHARE_API_KEY`；handler 将其作为 `FTSHARE_API_KEY` 请求头发送。缺失凭据时不会发起请求。

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--trade-code` | 否 | 目标股票代码，标准格式 `六位数字.SH/SZ`；也接受 `SH:600000`、`600000.XSHG` 和不带后缀的 `600000`；省略时返回当日全部股票 |
| `--date` | 否 | 快照日期，格式 `YYYYMMDD`；非交易日返回空结果，省略时使用最新交易日 |
| `--top-k` | 否 | 每只股票返回的相关公司数量，默认 10，范围 1–10 |
| `--page` | 否 | 页码，从 1 开始，默认 1 |
| `--page-size` | 否 | 每页返回的股票数，默认 200，范围 1–500 |
| `--all` | 否 | 自动翻页取回全部结果（全市场遍历时使用） |

## 命令

```bash
python <RUN_PY> ashare-rating-factor-snapshot --trade-code 600000.SH --date 20261117 --top-k 3
python <RUN_PY> ashare-rating-factor-snapshot --date 20261117 --page 1 --page-size 200
python <RUN_PY> ashare-rating-factor-snapshot --date 20261117 --all
python <RUN_PY> ashare-rating-factor-snapshot --trade-code 600000.SH
```

## 返回

- 外层：`code`、`message`、`data`
- `data`：`pageNum`、`pageSize`、`total`、`pages`、`records`
- `records[]`：`trade_code`（`六位数字.SH/SZ`）、`snapshot_date`（实际命中的快照交易日）、`related_securities[]`
- `related_securities[]`：`trade_code`、`score`、`rank`、`corr`
  - `score`：0–10 的整数评分，由 `corr` 分档得到；`0` 表示未评级，数值越大相关性越强
  - `rank`：名次，从 1 开始
  - `corr`：原始相关系数，取值 `-1 ~ 1`

## 注意

- 当前可查数据自 `20251117` 起。
- 相关公司按评分降序、相关系数降序、代码升序排列，不包含目标股票自身，同一目标股票下不重复。
- 本接口覆盖沪深股票，暂不返回北交所数据；传入北交所代码时结果为空。
- 非交易日或该日期无数据时返回 HTTP 200 和空 `records`。