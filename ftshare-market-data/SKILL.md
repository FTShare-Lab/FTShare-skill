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
python <RUN_PY> stock-minute-seal --trade-date 20260923 --symbol 000560.SZ
python <RUN_PY> etf-realtime-day-kline --symbols 510300.SH
python <RUN_PY> index-minutes --symbol 000300.SH --since-ts-millis 1787189400000 --until-ts-millis 1787191200000
python <RUN_PY> stock-reports --stock-code 600036.SH --page 1 --page-size 20
python <RUN_PY> stock-announcements --stock-code 600000.SH --page 1 --page-size 20
python <RUN_PY> stock-prospectuses --stock-code 600000.SH --page 1 --page-size 20
python <RUN_PY> stock-candlesticks-batch --symbols 600519.SH,600036.SH --interval-unit Day --since-ts-millis 1787000000000 --until-ts-millis 1787191200000
python <RUN_PY> etf-candlesticks-batch --symbols 510300.XSHG,159915.XSHE --interval-unit Day --since-ts-millis 1787000000000 --until-ts-millis 1787191200000
python <RUN_PY> index-candlesticks-batch --symbols 000300.XSHG,399001.XSHE --interval-unit Day --since-ts-millis 1787000000000 --until-ts-millis 1787191200000
python <RUN_PY> futures-kline --symbol A2605.DCE --interval daily --limit 5
python <RUN_PY> futures-kline-batch --symbols A2605.DCE,M2605.DCE --interval daily --limit 5
python <RUN_PY> futures-minutes --symbol A2605.DCE --interval 5min --start 1787000000000 --end 1787191200000 --limit 5
python <RUN_PY> futures-realtime-day-kline --symbols A2605.DCE,M2605.DCE
python <RUN_PY> etf-pcf-infos --symbol 510300.SH --trade-date 20260909
python <RUN_PY> etf-net-value --etf-code 510300 --nav-date 20260909
python <RUN_PY> etf-share --etf-code 510300 --page 1 --page-size 5
python <RUN_PY> etf-announcements --etf-code 159915 --page 1 --page-size 5
python <RUN_PY> etf-component-details --symbol 510300.SH
python <RUN_PY> stock-dividends-effective --symbol 600519.XSHG --page 1 --page-size 20
python <RUN_PY> executive-holdings-changes --stock-code 600519 --page 1 --page-size 20
python <RUN_PY> eastmoney-shareholder-changes --symbol 股东增持 --page 1 --page-size 20
python <RUN_PY> ashare-code-change --trade-code 001872.SZ
python <RUN_PY> ashare-code-change-timeline
python <RUN_PY> ashare-status-change --trade-code 600848.SH --change-type 上市
python <RUN_PY> stock-st-history --symbol 600735.SH,000004.SZ
python <RUN_PY> nth-trade-date --n 5
python <RUN_PY> continuous-auction-volume --trade-date 20260918 --page 1 --page-size 50
python <RUN_PY> news-reaction-snapshot --symbol 600519.SH --start-date 20260818 --end-date 20260828 --lookback-hours 48 --page 1 --page-size 5
python <RUN_PY> semantic-search-news --query 人工智能
python <RUN_PY> stock-candlesticks-daily --trade_date 20261008 --page 1 --page_size 500
python <RUN_PY> ths-board-constituents --board-name 军工 --page 1 --page-size 100
python <RUN_PY> stock-tech-factor --symbol 000001.SZ --trade-date 20261012 --category trend
python <RUN_PY> sge-spot-description-all --category spot_deferred --active-only
python <RUN_PY> market-announcements --keyword 回购 --start-date 20261001 --end-date 20261031 --page 1 --page-size 20
python <RUN_PY> periodic-reports --stock-code 000001.SZ --report-type annual --page 1 --page-size 20
python <RUN_PY> index-fut-depth --trade-date 20261030 --code-prefix IF
```

下载类：

```bash
# 公告正文 PDF：先查列表拿 url_hash，再下载
python <RUN_PY> stock-announcements --url-hash d8d54544...cf574adf --output ./ann.pdf
python <RUN_PY> etf-announcements --url-hash d8d54544...cf574adf
python <RUN_PY> market-announcements --url-hash 7d3176c8...c846f8dfbc --output ./ann.pdf
python <RUN_PY> periodic-reports --url-hash 37801609...68090432 --output ./report.pdf
```

## 能力范围

接口详细参数、响应字段和限制以对应子目录的 `SKILL.md` 及其链接的在线文档为准（文档首页：`https://market.ft.tech/gateway/doc/`）。

## 子技能索引与路由

**两条硬性要求：**

1. **先定位，再调用**：不要凭记忆猜子技能名，按下面顺序定位。
2. **输出/调用前必须核对真实目录名**：子技能目录名以 `sub-skills/` 下的真实目录为准（可用 `ls sub-skills`、`sub-skills/INDEX.md` 或 `python <RUN_PY> --index` 核对）。近似前缀很容易拼错，例如 `sw-industry-*`（申万行业）不等于 `sw-index-*`，`supply-chain-subsubindustry-companies` 不等于 `supply-chain-subindustry-companies`。目录名拼错会导致「找不到 subskill」而调用失败。

定位顺序：

1. **快速路由**：`python <RUN_PY> --index` 输出「名称 + 触发场景」一行一个；`--index --json` 输出结构化 JSON（含 route / doc_url / tier），便于程序化匹配。
2. **完整索引**：`sub-skills/INDEX.md`，246 个子技能按业务域分组，含「子技能 / 接口 / 路由 / 触发场景 / 套餐 / 在线文档」；按需读取，不必整体加载。
3. **机器可读映射**：`sub-skills/manifest.tsv`（`skill / route / doc_title / doc_url / tier / category / description`）；`sub-skills/doc-map.tsv` 保存路由到文档标题/链接/套餐的映射。
4. **单接口细节**：读对应 `sub-skills/<名称>/SKILL.md`；完整字段与示例见其指向的在线文档（markdown 链接可直接抓取）。

索引与映射由 `python tools/index_skills.py --write` 从仓库自身生成（路由取 handler、文档标题与链接取 `sub-skills/doc-map.tsv`），不要手改；`--check` 校验是否过期并检查路由与文档映射是否齐全。

各业务域子技能数量（以 `INDEX.md` 为准）：股票 134、宏观 23、基金 18、期货 17、ETF 17、指数 15、债券 9、大模型语料 7、美股 2、现货 2、港股 2。

## 输出与错误

- 成功响应以格式化 JSON 输出到 stdout。
- HTTP、网络、参数和认证诊断输出到 stderr。
- 请求失败时返回非零退出状态。
- 下载类子 skill 只允许将文件写入当前工作目录及其子目录，越界以非零状态退出。
- 下载完成只向 stdout 输出落盘后的文件路径（不打印 JSON）。

## 运行时发现

`run.py` 仅执行 `sub-skills/<名称>/scripts/handler.py` 形式的动态发现结果，不维护重复的静态注册表。新增或移除子 skill 时，应同步其目录中的 `SKILL.md` 和 handler，并以套餐接口表和源接口文档进行核对。

本包是 Agent Skill，不是 Python SDK；SDK 的同步由独立任务负责。
