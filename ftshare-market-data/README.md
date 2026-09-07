# ftshare-market-data

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

`ftshare-market-data` 的当前可用范围不包含暂不支持的美股资产负债表、美股现金流、美股利润表、美股复权因子、港股资产负债表、港股现金流量表、港股利润表、港股估值分析、港股市值和炸板池接口。当前 README 及 `sub-skills/` 仅介绍和提供仍在支持范围内的接口。

## 在 ftshare 生态中的位置

`ftshare-market-data` 处于 ftshare 生态的数据 Skill 层。它连接 FTShare 数据服务 `market.ft.tech`，为投研任务、MCP 工具和 Agent 应用提供结构化、可直接调用的行情、财报和宏观数据。

```text
FTShare 数据服务 (market.ft.tech)
    ↓  HTTP GET（Python 标准库 urllib）
ftshare-market-data        # run.py 统一路由 + sub-skills 目录中的实际子 skill
    ↓
Claude Code / Codex / OpenClaw   # Agent 运行时加载本 Skill
    ↓
用户                       # 自然语言提问 → JSON 结果
```

> 这是一份 **Skill**（给 Agent 运行时消费），不是给人 `import` 的 Python 库。如果你需要在数据分析脚本里编程调用、想要 pandas `DataFrame`，请使用独立维护的 `ftshare-python-sdk`；本次 Skill 调整不修改 SDK。

## 作为 Skill 加载

本目录已包含标准 Skill 描述文件 `SKILL.md`（带 `name` / `description` frontmatter），把它作为一个 Skill 放进你的 Agent 运行时即可，无需安装任何包。

**Claude Code**：将本目录放入 skills 路径——项目级 `.claude/skills/ftshare-market-data/`，或用户级 `~/.claude/skills/ftshare-market-data/`。Claude Code 会自动读取 `SKILL.md`，在用户提问匹配到行情 / 财报 / 宏观等数据需求时触发。

**Codex / OpenClaw**：同样将本目录作为一个 Skill 加载，运行时读取 `SKILL.md` 的 frontmatter 完成路由（各家具体加载命令请以对应运行时文档为准）。

获取仓库：

```bash
git clone https://github.com/ftshare-lab/ftshare-skills.git
```

运行时只需要 Python 3：子 skill 仅使用标准库 `urllib`、`json`，**零第三方依赖**，不需要 `pandas`、`requests`。

## 快速开始

加载 Skill 后，用户用自然语言提问即可。运行时根据 `SKILL.md` 匹配子 skill、执行 `run.py`，并将返回的 JSON 交回用户。

```bash
python <RUN_PY> stock-list-all-stocks
python <RUN_PY> stock-realtime-minute-kline --symbols 600519.SH 000001.SZ
python <RUN_PY> hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24
```

`<RUN_PY>` 是本目录下 `run.py` 的绝对路径。当前子 skill 仅对应《FTShare 四档套餐全量接口表》及其活动源文档；已下线、未发布和暂不支持的接口不在范围内。

```json
{
    "items": [
        { "stock_code": "000001.SZ", "stock_name": "平安银行" },
        { "stock_code": "000002.SZ", "stock_name": "万科A" }
    ]
}
```

## 调用方式（唯一规则）

`run.py` 是统一调度入口，与 `SKILL.md` 同级。执行时：

1. 取 `SKILL.md` 的绝对路径，将末尾 `/SKILL.md` 替换为 `/run.py`，得到 `<RUN_PY>`。
2. 调用：`python <RUN_PY> <子skill名> [参数...]`

```bash
# 示例
python <RUN_PY> stock-list-all-stocks
python <RUN_PY> stock-ipos --page 1 --page_size 20
python <RUN_PY> semantic-search-news --query 人工智能
python <RUN_PY> etf-pcfs --date 20260309
python <RUN_PY> index-weight-summary --index-code 000300 --page 1 --page-size 20
python <RUN_PY> index-weight-list --index-code 000300 --page 1 --page-size 20
python <RUN_PY> hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24
python <RUN_PY> nth-trade-date --n 5
python <RUN_PY> eastmoney-shareholder-changes --symbol 股东增持 --page 1 --page-size 20
python <RUN_PY> ashare-code-change --trade-code 001872.SZ
python <RUN_PY> ashare-status-change --trade-code 600848.SH --change-type 上市
python <RUN_PY> economic-china-cpi-monthly
```

所有 `market.ft.tech` handler 默认使用 `https://market.ft.tech/gateway`。认证 key 从环境变量 `FTSHARE_API_KEY` 读取，并作为 `FTSHARE_API_KEY` 请求头发送；同时发送 `Content-Type: application/json`。缺少凭据时 handler 不会发起请求。本地或内网服务可通过环境变量切换 API 地址：

```bash
FTSHARE_BASE_URL=http://127.0.0.1:8000/ python <RUN_PY> stock-list-all-stocks
```

> `run.py` 内部通过 `__file__` 自定位，无论安装在何处都能正确找到各子 skill 的脚本。

## 返回类型

所有子 skill 一律向 **标准输出打印 JSON**，运行时（Agent）会直接读取这份 JSON，再决定如何以表格 / 要点形式展示给用户。

需要手工解析时（如冒烟测试、定时任务）：Shell 中配合 `jq`：

```bash
python run.py stock-list-all-stocks | jq '.items[0:3]'
```

响应中常见的表格数据信封包括：`data.records`、`data.items`、顶层 `items`、顶层数组。各子 skill 的 `SKILL.md` 会标注其具体响应结构与字段含义。

## 分页

分页接口同时支持传统 `--page / --page_size` 和更方便的 `--all` 自动翻页。

取单页：

```bash
python run.py stock-ipos --page 1 --page_size 20
```

自动翻页拉取全量数据：

```bash
python run.py stock-ipos --all
```

`--all` 仅在具体子 skill 的 `SKILL.md` 明确说明时可用；分页参数也以对应源文档为准。

## 能力总览

子 skill 以《FTShare 四档套餐全量接口表》为范围依据，按股票、ETF、指数、基金、可转债、期货、港股、板块、资金流、财务、公司治理、新闻公告研报和宏观经济等领域组织。每个接口的参数、响应字段和限制见对应子目录的 `SKILL.md` 及活动源文档；`api-doc/已下线`、`api-doc/未发布` 不计入范围。


| 域 | 代表子 skill |
|---|---|
| **交易日 / 财经日历 / 新闻公告研报** | `nth-trade-date`、`trading-calendar`、`financial-calendar`、`semantic-search-news`、`stock-announcements`、`stock-reports` |
| **A 股行情 / 基础** | `stock-list-all-stocks`、`stock-description-all`、`stock-quotes-list`、`stock-ipos`、`eastmoney-all-board-daily-ohlc`、`block-trades`、`margin-trading-details`、`continuous-auction-volume`、`intraday-auction-volume` |
| **A 股财报 / 业绩** | `stock-income-*`、`stock-balance-*`、`stock-cashflow-*`、`stock-performance-express-*`、`stock-performance-forecast-*` |
| **A 股股东 / 质押 / 增减持** | `stock-holder-ten`、`stock-holder-ften`、`stock-holder-nums`、`pledge-summary`、`pledge-detail`、`stock-share-chg`、`executive-holdings-changes`、`eastmoney-shareholder-changes` |
| **A 股公司行动 / 代码与状态** | `shareholder-meeting`、`major-contract-by-date`、`major-contract-by-symbol`、`major-contract-summary`、`ashare-code-change`、`ashare-status-change` |
| **A 股估值 / 千股千评 / 热度 / 资金流** | `eastmoney-stock-valuation`、`eastmoney-market-valuation`、`stock-comment-index/score/org-participate/desire/focus`、`stock-rank-xueqiu`、`stock-rank-eastmoney`、`stock-capital-flows` |
| **A 股涨跌停** | `limit-up-pool`、`limit-up-pool-yesterday`、`limit-down-pool` |
| **A 股商誉** | `stock-goodwill-detail`、`stock-goodwill-impairment`、`stock-goodwill-industry`、`stock-goodwill-market-overview`、`stock-goodwill-predict` |
| **可转债** | `cb-lists`、`cb-base-data` |
| **ETF** | `etf-description-all`、`etf-components-all`、`etf-pre-single`、`etf-pcfs`、`etf-adjust-factor`、`etf-minutes`、`etf-minutes-batch`、`etf-realtime-minute-kline`、`etf-realtime-day-kline` |
| **基金** | `fund-basicinfo-single-fund`、`fund-cal-return-...`、`fund-nav-single-fund-paginated`、`fund-overview-all-funds-paginated`、`fund-support-symbols-all-funds-paginated` |
| **指数** | `index-detail`、`index-list-paginated`、`index-ohlcs`、`index-prices`、`index-minutes`、`index-minutes-batch`、`sw-index-history-minutes`、`index-realtime-minute-kline`、`index-realtime-day-kline`、`index-description-all/paginated/download`、`index-weight-summary/list/download` |
| **板块（东财 / 同花顺）** | `eastmoney-concept-boards`、`eastmoney-board-constituents/daily-ohlc/latest-ohlc`、`10jqk-board-list/kline/all-kline`、`ths-industry-constituents` |
| **港股** | `company-hk`、`hk-candlesticks`、`northbound`、`southbound`、`eastmoney-hk-index-daily-kline`、`hsi-daily-weight` |
| **美股** | `eastmoney-us-stock-list`、`eastmoney-us-stock-daily-ohlc`、`us-basic` |
| **期货** | `futures-base-data`、`futures-lists`、`futures-limit`、`futures-settle`、`futures-weekly-detail`、`futures-warehouse-receipt`、`eastmoney-futures-position`、`eastmoney-futures-strange`、`member-build-process`、`member-position-ranking` |
| **宏观经济（中国 + 美国）** | `economic-china-gdp/cpi/ppi/pmi/lpr/...-monthly`（15 项）、`economic-us-economic-by-type`（16 类，按 `--type`） |

## 名称 → 代码映射

部分接口只接受代码而非名称。具体代码格式与映射方式以对应子 skill 文档为准。

## 查看可用接口

不带参数运行 `run.py` 会打印用法并列出全部可用子 skill：

```bash
python run.py
```

查看某个接口的详细参数、响应结构与字段说明：

```bash
cat sub-skills/stock-list-all-stocks/SKILL.md
```

## Base URL 配置

`market.ft.tech` 接口默认以 `https://market.ft.tech/gateway` 为基础地址，使用 HTTP GET；每个请求均需在请求头携带 `FTSHARE_API_KEY` 和 `Content-Type: application/json`：

```text
/api/v1/market/data/<接口路径>
```

如需切到本地或内网服务，设置 `FTSHARE_BASE_URL`。变量里是否带 `/gateway` 会原样保留：

```bash
FTSHARE_BASE_URL=http://127.0.0.1:8000/ python <RUN_PY> stock-list-all-stocks
FTSHARE_BASE_URL=http://127.0.0.1:8000/gateway/ python <RUN_PY> stock-list-all-stocks
```

- 所有 `market.ft.tech` 接口都通过 `FTSHARE_BASE_URL` 切换基础地址。

## 安全与约束

- **域名白名单**：使用 `safe_urlopen` 的 handler 会校验请求协议和主机匹配当前基础地址；设置 `FTSHARE_BASE_URL` 后按该地址校验。
- **子 skill 白名单**：`run.py` 仅允许 `sub-skills/<名称>/scripts/handler.py` 形态的子 skill，防止路径遍历。
- **下载落盘限制**：含 `--output` 的下载类接口仅允许写入**当前工作目录**下的路径。
- **依赖前序接口的参数**：下载类接口的 `url_hash` / `filename` 须先由对应的列表接口取得，勿硬编码。

## 项目结构

```text
ftshare-market-data/
  SKILL.md                # Skill 入口文档：frontmatter（name/description）+ 能力总览 + 调用规则
  run.py                  # 统一调度入口：校验并执行子 skill 的 handler
  README.md               # 本文档
  sub-skills/
    <子skill名>/
      SKILL.md            # 该接口的参数、响应结构、字段说明
      scripts/
        handler.py        # 具体实现：HTTP GET → 打印 JSON
```

## 与 ftshare-python-sdk 的关系

本仓库是 **Skill（命令行驱动，给 Agent 运行时）**；`ftshare-python-sdk` 是 **Python 库（给开发者编程）**。两者覆盖同一批 FTShare 数据接口，按使用形态区分：

| | ftshare-market-data（本仓库） | ftshare-python-sdk |
|---|---|---|
| 形态 | Skill（被运行时加载） | pip 包 |
| 入口 | `python run.py <子skill>` | `ft.market_api().<方法>()` |
| 返回 | 原始 JSON（stdout） | pandas `DataFrame` |
| 消费者 | Claude Code / Codex / OpenClaw | 数据分析脚本 / 量化研究 |
| 依赖 | 仅 Python 标准库 | `pandas`、`requests` |
