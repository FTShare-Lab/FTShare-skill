---
name: ftshare-market-data
description: FTShare 市场数据技能集。根据用户对股票、ETF、指数、基金、可转债、期货、港股、美股、资金流、财务数据或宏观数据的查询意图，匹配并执行对应子 skill。
---

# FTShare Market Data Skills

本 skill 是统一路由入口。子 skill 位于 `sub-skills/`，由同目录的 `run.py` 动态发现和执行。

## 调用

```bash
python <RUN_PY> <子skill名> [参数...]
```

`<RUN_PY>` 是本文件同级的 `run.py` 绝对路径。不带参数运行会列出当前可用子 skill。

## 认证与请求约束

- 所有请求必须提供 `FTSHARE_API_KEY` 环境变量。
- handler 将其作为 `FTSHARE_API_KEY` 请求头发送，并设置 `Content-Type: application/json`。
- 未设置凭据时，handler 在发起请求前以非零状态退出。
- 默认基础地址为 `https://market.ft.tech/gateway`，可通过 `FTSHARE_BASE_URL` 覆盖。
- 请求使用各子 skill 文档声明的 `/api/v1`、`/api/v2`、`/api/v3` 或 `/api/v4` 路由；handler 会限制请求 scheme 和 host 与基础地址一致。

## 常用示例

```bash
python <RUN_PY> stock-description-all --symbol-id 600000.SH --page 1 --page-size 1
python <RUN_PY> stock-realtime-minute-kline --symbols 600519.SH 000001.SZ
python <RUN_PY> stock-minutes --symbol 600519.SH --since-ts-millis 1787189400000 --until-ts-millis 1787191200000
python <RUN_PY> etf-realtime-day-kline --symbols 510300.SH
python <RUN_PY> index-minutes --symbol 000300.SH --since-ts-millis 1787189400000 --until-ts-millis 1787191200000
python <RUN_PY> stock-reports --stock-code 600036.SH --page 1 --page-size 20
python <RUN_PY> stock-announcements --stock-code 600000 --page 1 --page-size 20
python <RUN_PY> stock-candlesticks-batch --symbols 600519.SH,510300.SH --interval-unit Day --since-ts-millis 1787000000000 --until-ts-millis 1787191200000
python <RUN_PY> etf-candlesticks-batch --symbols 510300.XSHG,159915.XSHE --interval-unit Day --since-ts-millis 1787000000000 --until-ts-millis 1787191200000
python <RUN_PY> index-candlesticks-batch --symbols 000300.XSHG,399001.XSHE --interval-unit Day --since-ts-millis 1787000000000 --until-ts-millis 1787191200000
python <RUN_PY> futures-contract-kline --symbol A2605.DCE --interval daily --limit 5
python <RUN_PY> etf-pcf-infos --symbol 510300.SH --trade-date 20260909
python <RUN_PY> etf-net-value --etf-code 510300 --nav-date 20260909
python <RUN_PY> etf-share --etf-code 510300 --page 1 --page-size 5
python <RUN_PY> etf-announcements --etf-code 159915 --page 1 --page-size 5
python <RUN_PY> etf-component-details --symbol 510300.SH
python <RUN_PY> stock-dividends-effective --symbol 600519.XSHG --page 1 --page-size 20
python <RUN_PY> executive-holdings-changes --stock-code 600519 --page 1 --page-size 20
python <RUN_PY> eastmoney-shareholder-changes --symbol 股东增持 --page 1 --page-size 20
python <RUN_PY> ashare-code-change --trade-code 001872.SZ
python <RUN_PY> ashare-status-change --trade-code 600848.SH --change-type 上市
python <RUN_PY> stock-st-history --symbol 600735.SH,000004.SZ
python <RUN_PY> nth-trade-date --n 5
python <RUN_PY> continuous-auction-volume --trade-date 20260620 --page 1 --page-size 50
python <RUN_PY> semantic-search-news --query 人工智能
```

## 能力范围

当前子 skill 仅覆盖《FTShare 四档套餐全量接口表》中的接口；接口详细参数、响应字段和限制以对应子目录的 `SKILL.md` 及 `ftshare-doc/api-doc/` 活动源文档为准。`api-doc/已下线` 和 `api-doc/未发布` 不属于当前范围。

## 输出与错误

- 成功响应以格式化 JSON 输出到 stdout。
- HTTP、网络、参数和认证诊断输出到 stderr。
- 请求失败时返回非零退出状态。
- 下载类子 skill 只允许将文件写入当前工作目录及其子目录。

## 运行时发现

`run.py` 仅执行 `sub-skills/<名称>/scripts/handler.py` 形式的动态发现结果，不维护重复的静态注册表。新增或移除子 skill 时，应同步其目录中的 `SKILL.md` 和 handler，并以套餐接口表和源接口文档进行核对。

本包是 Agent Skill，不是 Python SDK；SDK 的同步由独立任务负责。
