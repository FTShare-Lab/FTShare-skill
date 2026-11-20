# 子技能索引

> 本文件由 `tools/index_skills.py --write` 生成，请勿手改。
> 共 249 个子技能；「在线文档」为可直接抓取的 markdown 链接。
> 按需读取本文件做路由，日常对话不必加载；文件较大，建议按分组或关键词检索，
> 精简清单用 `python run.py --index`（名称 + 触发场景）。

## 股票数据（134）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `10jqk-board-list` | 同花顺板块列表 | `/api/v1/market/data/ths-board-list` | Get all THS board list (同花顺板块列表). Use when user asks about 同花顺板块列表、概念… | 免费版 | [同花顺板块列表](https://market.ft.tech/gateway/doc/pages/o11ndmcf.md) |
| `abnormal-trading-details` | 龙虎榜明细 | `/api/v1/market/data/abnormal-trading-details` | 查询龙虎榜明细，按交易日返回上榜标的的涨跌幅、收盘价、成交额、上榜原因，以及买入额/卖出额前 5 名营业部明细。可用参数：--date、-… | 免费版 | [龙虎榜明细](https://market.ft.tech/gateway/doc/pages/yxmc9f7y.md) |
| `abnormal-trading-overview` | 龙虎榜总览 | `/api/v1/market/data/abnormal-trading-overview` | 查询龙虎榜总览，按交易日返回上榜标的的代码、名称、涨跌幅、收盘价、成交额和上榜原因。可用参数：--date、--page、--page_s… | 免费版 | [龙虎榜总览](https://market.ft.tech/gateway/doc/pages/9swt9vv8.md) |
| `ashare-code-change` | A股代码变更 | `/api/v1/market/data/stk-code-change` | 查询 A 股代码变更历史。Use when user asks about 股票代码变更、改名换码、代码迁移或北交所升板代码历史。 | 免费版 | [A股代码变更](https://market.ft.tech/gateway/doc/pages/yuzopjw5.md) |
| `ashare-code-change-timeline` | A股代码变更时间线 | `/api/v1/market/data/stk_code_change_timeline` | 查询 A 股代码变更时间线（全量）。Use when user asks about A 股代码变更时间线、换码事件全量列表、代码迁移对照… | 免费版 | [A股代码变更时间线](https://market.ft.tech/gateway/doc/pages/0a0mfc8k.md) |
| `ashare-interactions` | e互动 | `/api/v2/market/data/ashare-interactions` | 按提问日期范围查询 A 股上市公司互动问答，返回公司、行业、问题、答复及其时间等业务信息。接口：GET /api/v2/market/da… | 基础版 | [e互动](https://market.ft.tech/gateway/doc/pages/wzxfo6gw.md) |
| `ashare-news-sentiment-factors` | A股新闻情绪因子 | `/api/v3/market/data/ashare-news-sentiment-factors` | 查询指定 A 股的新闻情绪因子。必填 --trade-code 与 --start-date；区间跨度不得超过 31 天。接口：GET /… | 进阶版 | [A股新闻情绪因子](https://market.ft.tech/gateway/doc/pages/zdxwn9lx.md) |
| `ashare-rating-factor-snapshot` | A股相关性 Top-K | `/api/v3/market/data/ashare-rating-factor-snapshot` | 查询指定 A 股的 Top-K 相关公司。用户询问股票相关性、相关公司排名或相关性评分时使用。 | 进阶版 | [A股相关性 Top-K](https://market.ft.tech/gateway/doc/pages/hdns2u7u.md) |
| `ashare-status-change` | A股状态变更 | `/api/v1/market/data/stk-status-change` | 查询 A 股状态变更记录。Use when user asks about 上市、退市、暂停上市或股票状态变更。 | 免费版 | [A股状态变更](https://market.ft.tech/gateway/doc/pages/2zhtv2q3.md) |
| `auction-results` | 集合竞价结果 | `/api/v2/market/data/auction-results` | 返回当日所有股票的盘前集合竞价结果（9:25 开盘集合竞价快照）：集合竞价开盘价/收盘价（最新价）、最高价、最低价、成交量、成交额、均价（… | 基础版 | [集合竞价结果](https://market.ft.tech/gateway/doc/pages/z7n8ucgi.md) |
| `block-trades` | 大宗交易 | `/api/v1/market/data/block-trades` | 查询大宗交易列表。当用户需要获取 A 股大宗交易记录，包含买卖方营业部、成交价、成交量、溢价率等，或了解大宗交易列表时使用。 | 免费版 | [大宗交易](https://market.ft.tech/gateway/doc/pages/h7eun4xp.md) |
| `bse-mapping` | 北交所映射 | `/api/v1/market/data/bse-mapping` | 查询北交所代码映射。可选 --o-code。接口：GET /api/v1/market/data/bse-mapping。 | 免费版 | [北交所映射](https://market.ft.tech/gateway/doc/pages/dk0d6dqi.md) |
| `cashflow-stock-code` | 现金流支持股票代码 | `/api/v2/market/data/finance/cashflow-stock-code` | 获取所有有现金流量表数据的股票代码与名称列表，不分页，一次返回全量。接口：GET /api/v2/market/data/finance/… | 基础版 | [现金流支持股票代码](https://market.ft.tech/gateway/doc/pages/skukfb13.md) |
| `company-list` | 公司列表 | `/api/v1/market/data/company-list` | 查询公司列表。可选 --page、--page-size。接口：GET /api/v1/market/data/company-list。 | 免费版 | [公司列表](https://market.ft.tech/gateway/doc/pages/92awt2dx.md) |
| `continuous-auction-volume` | 连续竞价成交量 | `/api/v2/market/data/intraday-auction-volume` | 查询全市场连续竞价成交量和成交额占比。用户询问全市场、沪深北市场的分时成交占比时使用。 | 基础版 | [连续竞价成交量](https://market.ft.tech/gateway/doc/pages/6xp6q54v.md) |
| `daec-history-prices` | 标的分时数据 | `/api/v4/market/data/daec/history/prices` | 查询指定标的的 1 分钟分时数据（价格、均价、成交量、成交额）。可用参数：--symbol、--range、--days、--ts_ms。… | 专业版 | [标的分时数据](https://market.ft.tech/gateway/doc/pages/2fc0d5ut.md) |
| `daec-market-snapshot` | 市场行情快照 | `/api/v1/market/data/daec/market/snapshot` | 查询全市场或单个交易所的行情快照，返回市场状态、涨跌幅、成交量、成交额，以及按涨跌幅区间统计的涨跌分布（9 档）。可用参数：--scope… | 免费版 | [市场行情快照](https://market.ft.tech/gateway/doc/pages/6fn39pnw.md) |
| `daec-prev-closes` | 标的昨收价 | `/api/v1/market/data/daec/history/prev-closes` | 查询指定标的在一段日期区间内每个交易日的昨收价（前收盘价）。可用参数：--symbol、--since、--until。接口：GET /a… | 免费版 | [标的昨收价](https://market.ft.tech/gateway/doc/pages/0tati78l.md) |
| `eastmoney-all-board-daily-ohlc` | 东方财富全板块日线OHLC | `/api/v1/market/data/eastmoney-all-board-daily-ohlc` | 分页查询东方财富全部板块历史日线 OHLC（板块代码/名称/市场/日期/开高低收/成交量/成交额/振幅/涨跌幅/涨跌额/换手率）。用户提到… | 免费版 | [东方财富全板块日线OHLC](https://market.ft.tech/gateway/doc/pages/7eeaj9ic.md) |
| `eastmoney-board-constituents` | 东方财富板块成分股 | `/api/v1/market/data/eastmoney-board-constituents` | 查询东财板块成分股。当用户需要查询指定东财板块的全部成分股代码和名称，或了解东财板块成分股时使用。 | 免费版 | [东方财富板块成分股](https://market.ft.tech/gateway/doc/pages/xojk0kx8.md) |
| `eastmoney-board-daily-ohlc` | 东方财富板块日线OHLC | `/api/v1/market/data/eastmoney-board-daily-ohlc` | 查询东财单板块历史 OHLC。当用户需要查询指定东财板块历史 OHLC 数据，支持日期范围过滤与分页，或了解东财单板块历史 OHLC时使用。 | 免费版 | [东方财富板块日线OHLC](https://market.ft.tech/gateway/doc/pages/h203ey6u.md) |
| `eastmoney-concept-boards` | 东方财富概念板块 | `/api/v1/market/data/eastmoney-concept-boards` | 查询东财概念板块列表。当用户需要查询东财概念板块基础信息与成分代码列表，返回全量板块，或了解东财概念板块列表时使用。 | 免费版 | [东方财富概念板块](https://market.ft.tech/gateway/doc/pages/i21jsfx7.md) |
| `eastmoney-dapan-flow` | 东方财富大盘资金流 | `/api/v1/market/data/eastmoney-dapan-flow` | 获取东方财富大盘指数（沪深两市）日资金流数据，含主力/超大单/大单/中单/小单五档净流入及净占比，以及上证/深证收盘价与涨跌幅。接口：GE… | 免费版 | [东方财富大盘资金流](https://market.ft.tech/gateway/doc/pages/v32o6wwz.md) |
| `eastmoney-etf-flow` | 东方财富ETF资金流 | `/api/v1/market/data/eastmoney-etf-flow` | 查询东方财富 ETF 日资金流。接口：GET /api/v1/market/data/eastmoney-etf-flow。用户问 ETF… | 免费版 | [东方财富ETF资金流](https://market.ft.tech/gateway/doc/pages/nh3wc690.md) |
| `eastmoney-market-valuation` | 东方财富市场估值 | `/api/v1/market/data/eastmoney-market-valuation` | 查询东财市场日估值。当用户需要查询 A 股主要市场指数（上证指数、沪深300、深证成指、创业板指、科创50、北证50）的每日估值数据，包括… | 免费版 | [东方财富市场估值](https://market.ft.tech/gateway/doc/pages/t4ewt2c8.md) |
| `eastmoney-rank` | 东方财富股票排名 | `/api/v1/market/data/eastmoney-rank` | 查询东方财富股票排行榜最新一期快照。可用参数：--rank_group、--market、--trade_date。接口：GET /api… | 免费版 | [东方财富股票排名](https://market.ft.tech/gateway/doc/pages/178klizp.md) |
| `eastmoney-sector-flow` | 东方财富板块资金流 | `/api/v1/market/data/eastmoney-sector-flow` | 查询东方财富板块资金流（行业/概念/地域日资金流）。用户问东财板块资金流、板块主力净流入、行业/概念/地域资金流向、BK 板块代码资金流、… | 免费版 | [东方财富板块资金流](https://market.ft.tech/gateway/doc/pages/upr04twl.md) |
| `eastmoney-shareholder-changes` | 东方财富股东增减持 | `/api/v1/market/data/holder/stock-ggcg-em` | 查询东方财富股东增减持。Use when user asks about 股东增持、股东减持或东方财富股东变动。 | 免费版 | [东方财富股东增减持](https://market.ft.tech/gateway/doc/pages/t9hrpidk.md) |
| `eastmoney-stock-flow` | 东方财富个股资金流 | `/api/v1/market/data/eastmoney-stock-flow` | 获取东方财富个股日资金流数据，含主力/超大单/大单/中单/小单五档净流入及净占比，以及收盘价与涨跌幅。接口：GET /api/v1/mar… | 免费版 | [东方财富个股资金流](https://market.ft.tech/gateway/doc/pages/x9fhxzl5.md) |
| `eastmoney-stock-valuation` | 东方财富个股估值 | `/api/v1/market/data/eastmoney-stock-valuation` | 查询东财个股日估值。当用户需要查询全部 A 股个股的每日估值数据，包括市盈率（TTM/LYR）、市净率、市现率、市销率、PEG、总市值、流… | 免费版 | [东方财富个股估值](https://market.ft.tech/gateway/doc/pages/z885d6r1.md) |
| `exchange-margin-summaries` | 交易所融资融券汇总日度 | `/api/v1/market/data/exchange-margin-summaries` | 查询交易所融资融券汇总日度数据。用户询问沪深北交易所融资融券余额、买入额、偿还额或融券数据时使用。同义：两融。 | 免费版 | [交易所融资融券汇总日度](https://market.ft.tech/gateway/doc/pages/1gb9y7b9.md) |
| `executive-holdings-changes` | 董监高持股变动 | `/api/v1/market/data/holder/stock-ggmx` | 查询董监高持股变动明细。用户询问董监高、高管持股变动、增持减持、变动股数或变动日期时使用。 | 免费版 | [董监高持股变动](https://market.ft.tech/gateway/doc/pages/iuma9fkg.md) |
| `institution-share-holdings` | 机构股本持股 | `/api/v2/market/data/institution/institution-share-holdings` | 查询指定机构在指定报告期的持股汇总。可用参数：--institution_id、--year、--report_type、--invest… | 基础版 | [机构股本持股](https://market.ft.tech/gateway/doc/pages/9vj4t4f2.md) |
| `intraday-auction-volume` | 单标的连续竞价成交量 | `/api/v1/market/data/intraday-auction-volume/symbol` | 查询单只标的的连续竞价成交量/成交额占比分时序列（按分钟）。不传 --trade-date 返回当日实时，传入历史日期返回当日分时；必填 … | 免费版 | [单标的连续竞价成交量](https://market.ft.tech/gateway/doc/pages/bskofshl.md) |
| `kline-pattern-annotations` | K线形态标注 | `/api/v3/market/data/kline-pattern-annotations` | 查询指定快照日的 K 线形态识别标注，包含形态名、窗口区间、方向、状态、置信度和识别理由。接口：GET /api/v3/market/da… | 进阶版 | [K线形态标注](https://market.ft.tech/gateway/doc/pages/l31zj3q1.md) |
| `limit-event-timeline` | 涨跌停事件时间线 | `/api/v2/market/data/limit-event-timeline-3s` | 查询个股涨跌停事件 3 秒级时间线。可用参数：--symbol、--trade_date、--page、--page_size。接口：GE… | 基础版 | [涨跌停事件时间线](https://market.ft.tech/gateway/doc/pages/wykygobl.md) |
| `limit-list` | 涨跌停池 | `/api/v1/market/data/limit-list` | 统一查询涨停、跌停或炸板股票池。可用参数：--limit_type、--trade_date。接口：GET /api/v1/market/… | 免费版 | [涨跌停池](https://market.ft.tech/gateway/doc/pages/qt0y1loe.md) |
| `limit-up-briefs` | 涨停简报 | `/api/v3/market/data/limit-up-reports/briefs` | 查询指定交易日全部涨停简报，每条为一段 Markdown 文本；成功时 `data.items` 为简报列表，元素含 `security_… | 进阶版 | [涨停简报](https://market.ft.tech/gateway/doc/pages/ycngxjlu.md) |
| `limit-up-public-report` | 涨停对外归因报告 | `/api/v3/market/data/limit-up-reports/public-report` | 查询指定标的的对外涨停归因报告，成功时 `data.text` 为报告 Markdown 原文。可用参数：--date、--securit… | 进阶版 | [涨停对外归因报告](https://market.ft.tech/gateway/doc/pages/thz9lvyg.md) |
| `major-contract-by-date` | 重大合同 | `/api/v1/market/data/corporate/contract` | 按公告日期范围查询A股重大合同信息（market.ft.tech）。用户问重大合同、某日/某月重大合同、合同金额、签约方时使用。 | 免费版 | [重大合同](https://market.ft.tech/gateway/doc/pages/2kakg1xc.md) |
| `major-contract-by-symbol` | 重大合同按标的 | `/api/v1/market/data/corporate/contract/by-symbol` | 按股票代码查询重大合同历史（market.ft.tech）。用户问某股票的重大合同、某公司签了哪些大单、合同金额时使用。 | 免费版 | [重大合同按标的](https://market.ft.tech/gateway/doc/pages/bv3yxxhz.md) |
| `major-contract-summary` | 重大合同汇总 | `/api/v1/market/data/corporate/contract/summary` | 近一年A股个股重大合同汇总排名（market.ft.tech）。用户问重大合同排行榜、哪些公司签合同最多/金额最大、合同总额排名时使用。 | 免费版 | [重大合同汇总](https://market.ft.tech/gateway/doc/pages/5sahxrk6.md) |
| `margin-trading-details` | 融资融券明细 | `/api/v1/market/data/margin-trading-details` | 获取融资融券明细。当用户需要获取 A 股融资融券明细列表（按交易日快照），支持单日、区间或标的过滤查询，或了解融资融券明细时使用。同义：两… | 免费版 | [融资融券明细](https://market.ft.tech/gateway/doc/pages/sx26v1nk.md) |
| `market-distribution-intraday` | 市场涨跌分布分时 | `/api/v2/market/data/market-distribution-intraday` | 获取市场涨跌分布的日内分时序列。接口：GET /api/v2/market/data/market-distribution-intrad… | 基础版 | [市场涨跌分布分时](https://market.ft.tech/gateway/doc/pages/c8hl03ku.md) |
| `namechange` | 股票曾用名 | `/api/v1/market/data/namechange` | 查询 A 股股票曾用名。用户问股票曾用名、历史名称、改名记录、之前叫什么、原名称、股票改名、600848 曾用名、自仪股份改名时使用。参数… | 免费版 | [股票曾用名](https://market.ft.tech/gateway/doc/pages/hcone123.md) |
| `news-reaction-snapshot` | 消息量价共振 | `/api/v3/market/data/news-reaction-snapshot` | 查询指定 A 股的新闻市场反应快照（消息量价共振）。用户询问个股消息面与量价的共振、新闻反应方向或阶段时使用。 | 进阶版 | [消息量价共振](https://market.ft.tech/gateway/doc/pages/96o5mbkw.md) |
| `northbound` | 北向资金交易 | `/api/v1/market/data/northbound` | 查询北向资金交易数据。当用户需要查询指定交易日北向资金（沪股通、深股通）交易汇总数据，或了解北向资金交易数据时使用。同义：陆股通。 | 免费版 | [北向资金交易](https://market.ft.tech/gateway/doc/pages/q89f0uwz.md) |
| `nth-trade-date` | 第N个交易日 | `/api/v1/market/data/time/get-nth-trade-date` | 查询第 N 个交易日。Use when user asks for 前 N 个交易日、某日期对应的第 N 个交易日或交易日倒推。 | 免费版 | [第N个交易日](https://market.ft.tech/gateway/doc/pages/ocqw0qc8.md) |
| `pledge-detail` | 股权质押明细 | `/api/v1/market/data/pledge/pledge-detail` | 查询单票股权质押个股详细信息。当用户需要获取 A 股上市公司单只股票所有报告期的股权质押详细信息，支持沪深京股票，支持分页查询，或了解单票… | 免费版 | [股权质押明细](https://market.ft.tech/gateway/doc/pages/atshpwbu.md) |
| `pledge-summary` | 股权质押汇总 | `/api/v1/market/data/pledge/pledge-summary` | 查询所有期股权质押总揽数据。当用户需要获取 A 股市场所有报告期的股权质押总揽数据，包括质押公司数量、质押笔数、质押总股数、质押总市值、沪… | 免费版 | [股权质押汇总](https://market.ft.tech/gateway/doc/pages/ovns66g1.md) |
| `price-change` | 价格变动 | `/api/v2/market/data/price/get-price-change` | 单票 N 日涨跌幅接口。可用参数：--stock_code、--base_date、--n、--direction。接口：GET /api… | 基础版 | [价格变动](https://market.ft.tech/gateway/doc/pages/d953tpbb.md) |
| `report-announcement-list` | 报告公告列表 | `/api/v1/market/data/report-announcements/list` | 按公告日期分页查询报告公告列表，可选按证券代码过滤。用户提到「报告公告列表」「公告列表」「某日公告」「report announcemen… | 免费版 | [报告公告列表](https://market.ft.tech/gateway/doc/pages/4qspcoqt.md) |
| `report-announcement-summary` | 报告公告摘要 | `/api/v2/market/data/report-announcements/summary` | 根据公告 ID 查询单条报告公告的摘要、标题、证券信息和处理状态。用户提到「报告公告摘要」「公告摘要」「单条公告详情」「report an… | 基础版 | [报告公告摘要](https://market.ft.tech/gateway/doc/pages/kfe01dfi.md) |
| `risk-warning-stocks` | 风险警示股 | `/api/v1/market/data/risk-warning-stocks` | 按交易日查询风险警示股票列表。必填 --date，可选 --page、--page-size。接口：GET /api/v1/market/… | 免费版 | [风险警示股](https://market.ft.tech/gateway/doc/pages/3o4clccl.md) |
| `security-search` | 标的搜索 | `/api/v1/market/security/search` | 按名称、代码或拼音搜索标的。必填 --query，可选 --limit。接口：GET /api/v1/market/security/se… | — | 标的搜索 |
| `southbound` | 南向资金交易 | `/api/v1/market/data/southbound` | 查询南向资金交易数据。当用户需要查询指定交易日南向资金（港股通沪、港股通深）交易汇总数据，或了解南向资金交易数据时使用。 | 免费版 | [南向资金交易](https://market.ft.tech/gateway/doc/pages/ujoa8eup.md) |
| `stk-ah-comparison` | AH股对比 | `/api/v1/market/data/hk/stk-ah-comparison` | 查询 A/H 股比价、涨跌幅和溢价率。用户询问港股与对应 A 股估值比较时使用。 | 免费版 | [AH股对比](https://market.ft.tech/gateway/doc/pages/8fr77co1.md) |
| `stk-alert-broker` | 交易所重点提示证券 | `/api/v2/market/data/stk-alert-broker` | 查询交易所重点提示证券及提示有效期间。接口：GET /api/v2/market/data/stk-alert-broker。同义：打板。 | 基础版 | [交易所重点提示证券](https://market.ft.tech/gateway/doc/pages/pp359u6x.md) |
| `stk-manager-hold` | 上市公司管理层持股 | `/api/v1/market/data/stk-manager-hold` | 查询上市公司管理层人员持股变动明细。用户问管理层持股、高管持股、董监高持股、持股变动、变动原因时使用。参数 trade_code 必填且需… | 免费版 | [上市公司管理层持股](https://market.ft.tech/gateway/doc/pages/vik756y6.md) |
| `stk-manager-pay` | 上市公司管理层薪酬 | `/api/v1/market/data/stk-manager-pay` | 查询上市公司管理层人员年度薪酬。用户问高管薪酬、董事薪酬、董监高薪酬、管理层年薪、变动原因时使用。参数 trade_code 必填且需带 … | 免费版 | [上市公司管理层薪酬](https://market.ft.tech/gateway/doc/pages/szjpqfmh.md) |
| `stk-managers` | 上市公司管理层 | `/api/v1/market/data/stk-managers` | 查询上市公司管理层人员信息。用户问上市公司管理层、高管、董事、独立董事、董事长、总经理、任职区间、候选日期、董监高、平安银行管理层、600… | 免费版 | [上市公司管理层](https://market.ft.tech/gateway/doc/pages/moz0yjm6.md) |
| `stk-premarket` | 盘前数据 | `/api/v2/market/data/stk-premarket` | 查询盘前数据（每日股本、昨收、涨跌停价、价格与总市值 / 流通市值）。适用于\"某只股票某天的总股本 / 流通股本\"\"历史股本是多少\… | 基础版 | [盘前数据](https://market.ft.tech/gateway/doc/pages/q1zs7bsw.md) |
| `stk-shock` | 个股异常波动 | `/api/v2/market/data/stk-shock` | 查询个股异常波动及买卖营业部明细。接口：GET /api/v2/market/data/stk-shock。同义：打板。 | 基础版 | [个股异常波动](https://market.ft.tech/gateway/doc/pages/d66clwan.md) |
| `stk-surv` | 个股严重异常波动 | `/api/v2/market/data/stk-surv` | 查询 A 股个股严重异常波动记录，返回证券、市场、异常原因和异常期间。接口：GET /api/v2/market/data/stk-sur… | 基础版 | [个股严重异常波动](https://market.ft.tech/gateway/doc/pages/hflud05f.md) |
| `stock-adjust-factor` | 股票复权因子 | `/api/v1/market/data/stock-adjust-factor` | 查询股票复权因子。支持 --symbol、--trade-date、--start-date、--end-date、--page、--pa… | 免费版 | [股票复权因子](https://market.ft.tech/gateway/doc/pages/1eu6rgc8.md) |
| `stock-balance-all-stocks-specific-period` | A股资产负债表 | `/api/v1/market/data/finance/balance` | Get balance sheet (资产负债表) for all stocks in a specific reporting peri… | 免费版 | [A股资产负债表](https://market.ft.tech/gateway/doc/pages/qf2a0ocw.md) |
| `stock-candlesticks` | 股票K线 | `/api/v1/market/data/stock-candlesticks` | 单只股票/ETF/指数/可转债历史日/周/月/年 K 线 GET 接口（market.ft.tech，stock-candlesticks… | 免费版 | [股票K线](https://market.ft.tech/gateway/doc/pages/owq0364i.md) |
| `stock-candlesticks-batch` | 批量股票K线 | `/api/v2/market/data/stock-candlesticks/batch` | 批量获取多只 A 股股票 K 线 GET 接口（market.ft.tech，stock-candlesticks/batch）。用户问多… | 基础版 | [批量股票K线](https://market.ft.tech/gateway/doc/pages/rpk1uury.md) |
| `stock-candlesticks-daily` | 股票日K快照 | `/api/v1/market/data/stock-candlesticks-daily` | 查询股票日K快照。当用户需要某个交易日全部普通 A 股的日 K（开高低收、成交量额、换手率），或要对某日全市场做横截面分析时使用。 | 免费版 | [股票日K快照](https://market.ft.tech/gateway/doc/pages/6b24gsjc.md) |
| `stock-capital-flows` | 股票资金流向 | `/api/v1/market/data/stock-capital-flows` | 查询 A 股股票资金流向（主力净流入）。支持当前实时快照，或指定日期的 15 分钟切片快照（默认日终 time=1530）。Use whe… | 免费版 | [股票资金流向](https://market.ft.tech/gateway/doc/pages/rt2hibwf.md) |
| `stock-cashflow-all-stocks-specific-period` | A股现金流量表 | `/api/v1/market/data/finance/cashflow` | Get cash flow statement (现金流量表) for all stocks in a specific reportin… | 免费版 | [A股现金流量表](https://market.ft.tech/gateway/doc/pages/6ch0qd83.md) |
| `stock-comment-desire` | 千股千评意愿度 | `/api/v1/market/data/stock-comment/desire` | 查询指定股票的千股千评市场参与意愿及5日均值变化（market.ft.tech）。用户问市场参与意愿、散户参与度时使用。 | 免费版 | [千股千评意愿度](https://market.ft.tech/gateway/doc/pages/6olp75vh.md) |
| `stock-comment-focus` | 千股千评关注度 | `/api/v1/market/data/stock-comment/focus` | 查询指定股票的千股千评市场热度用户关注指数及排名变动（market.ft.tech）。用户问用户关注指数、市场关注度排名时使用。 | 免费版 | [千股千评关注度](https://market.ft.tech/gateway/doc/pages/fu7619ln.md) |
| `stock-comment-index` | 千股千评 | `/api/v1/market/data/stock-comment/index` | 查询东方财富千股千评综合诊断主表（market.ft.tech），含收盘价、涨跌幅、换手率、市盈率、主力成本、机构参与度、综合评分、排名、… | 免费版 | [千股千评](https://market.ft.tech/gateway/doc/pages/t6k24jo7.md) |
| `stock-comment-org-participate` | 机构参与度 | `/api/v1/market/data/stock-comment/org-participate` | 查询指定股票的千股千评机构参与度走势（market.ft.tech）。用户问机构参与度、机构关注度时使用。 | 免费版 | [机构参与度](https://market.ft.tech/gateway/doc/pages/2p8ebvd0.md) |
| `stock-comment-score` | 千股千评评分 | `/api/v1/market/data/stock-comment/score` | 查询指定股票的千股千评历史综合评分走势（market.ft.tech）。用户问某股票历史评分、综合评分走势时使用。 | 免费版 | [千股千评评分](https://market.ft.tech/gateway/doc/pages/yrx27y0e.md) |
| `stock-connect-members` | 互联互通成份 | `/api/v1/market/data/stock-connect-members` | 按互联互通方向和交易通道查询沪股通、深股通、沪市港股通或深市港股通的最新成份名单。可用参数：--direction、--channel、-… | 免费版 | [互联互通成份](https://market.ft.tech/gateway/doc/pages/vu1fxtpg.md) |
| `stock-description-all` | 股票基础信息 | `/api/v1/market/data/stock-description` | 查询 A 股股票基础信息，支持按 symbol_id 筛选和分页。用户询问股票基础资料、股票列表详情或股票代码对应公司信息时使用。接口：G… | 免费版 | [股票基础信息](https://market.ft.tech/gateway/doc/pages/sw2o1vsr.md) |
| `stock-dividends` | 股票分红记录 | `/api/v1/market/data/stock-dividends` | 获取 A 股分红记录（派息、送股、转增）分页视图；可按标的和公告日期范围筛选。接口：GET /api/v1/market/data/sto… | 免费版 | [股票分红记录](https://market.ft.tech/gateway/doc/pages/0fxhla7v.md) |
| `stock-dividends-effective` | 股票有效分红记录 | `/api/v2/market/data/stock-dividends-effective` | 查询 A 股已实施（有效）分红记录（stock_dividends_effective）。用户问已实施分红、每股派息、送股、转增、除权除息… | 基础版 | [股票有效分红记录](https://market.ft.tech/gateway/doc/pages/jylv7533.md) |
| `stock-filter-v2` | 股票筛选 | `/api/v2/market/data/stock-list/filter` | A 股实时行情筛选接口：可按 symbol 精确查单标的，或按 board（板块/交易所）与 listing_date_since（上市日… | 基础版 | [股票筛选](https://market.ft.tech/gateway/doc/pages/r7bgm5w0.md) |
| `stock-ggmx-buy-ranking` | 董监高增持排名 | `/api/v2/market/data/holder/stock-ggmx-buy-ranking` | 查询董监高增持排行。可选 --time-range（1m/3m/6m/1y/2y）、--page、--page-size。接口：GET /… | 基础版 | [董监高增持排名](https://market.ft.tech/gateway/doc/pages/zbq8gkmi.md) |
| `stock-ggmx-sell-ranking` | 董监高减持排名 | `/api/v2/market/data/holder/stock-ggmx-sell-ranking` | 查询董监高减持排行。可选 --time-range（1m/3m/6m/1y/2y）、--page、--page-size。接口：GET /… | 基础版 | [董监高减持排名](https://market.ft.tech/gateway/doc/pages/sqg80974.md) |
| `stock-goodwill-detail` | 商誉个股明细 | `/api/v1/market/data/goodwill/stock-detail` | Get goodwill detail (商誉明细) for all stocks in a specific year. Use whe… | 免费版 | [商誉个股明细](https://market.ft.tech/gateway/doc/pages/qtl1iak0.md) |
| `stock-goodwill-impairment` | 商誉减值 | `/api/v1/market/data/goodwill/stock-impairment` | Get goodwill impairment detail (商誉减值明细) for all stocks in a specific … | 免费版 | [商誉减值](https://market.ft.tech/gateway/doc/pages/p7iit8mt.md) |
| `stock-goodwill-industry` | 商誉行业 | `/api/v1/market/data/goodwill/industry` | Get goodwill data by industry (行业商誉). Use when user asks about 行业商誉, … | 免费版 | [商誉行业](https://market.ft.tech/gateway/doc/pages/v4l12equ.md) |
| `stock-goodwill-market-overview` | 商誉市场总览 | `/api/v1/market/data/goodwill/market-overview` | Get A-share market-wide goodwill overview (A股商誉市场概况) with historical … | 免费版 | [商誉市场总览](https://market.ft.tech/gateway/doc/pages/20nmy527.md) |
| `stock-goodwill-predict` | 商誉预测 | `/api/v1/market/data/goodwill/predict` | Get goodwill impairment prediction data (商誉减值预期) for stocks. Use when… | 免费版 | [商誉预测](https://market.ft.tech/gateway/doc/pages/p5g2tkdk.md) |
| `stock-history-list` | 股票历史列表 | `/api/v1/market/data/stock-history-list` | 按交易日查询股票历史行情截面列表。必填 --trade-date，可选 --code、--page、--page-size。接口：GET … | 免费版 | [股票历史列表](https://market.ft.tech/gateway/doc/pages/jmcwf10j.md) |
| `stock-holder-ften` | 十大流通股东 | `/api/v1/market/data/holder/stock-holder-ften` | 查询 A 股十大流通股东。当用户需要获取 A 股十大流通股东信息（按 stock_code 查全部历史，或以 is_last=true 查… | 免费版 | [十大流通股东](https://market.ft.tech/gateway/doc/pages/era9uwoi.md) |
| `stock-holder-nums` | 股东人数 | `/api/v1/market/data/holder/stock-holder-nums` | 查询 A 股股东人数。当用户需要获取 A 股股东人数信息（按 stock_code 查全部历史，或以 is_last=true 查全市场最… | 免费版 | [股东人数](https://market.ft.tech/gateway/doc/pages/oecit8qn.md) |
| `stock-holder-ten` | 十大股东 | `/api/v1/market/data/holder/stock-holder-ten` | 查询 A 股十大股东。当用户需要获取 A 股十大股东信息（按 stock_code 查全部历史，或以 is_last=true 查全市场最… | 免费版 | [十大股东](https://market.ft.tech/gateway/doc/pages/t6m1ygo3.md) |
| `stock-income-all-stocks-specific-period` | A股利润表 | `/api/v1/market/data/finance/income` | Get income statement (利润表) for all stocks in a specific reporting per… | 免费版 | [A股利润表](https://market.ft.tech/gateway/doc/pages/dv3kxyb2.md) |
| `stock-institution-holdings` | 机构持股 | `/api/v2/market/data/share/stock-institution-holdings` | 查询 A 股指定报告期机构持股汇总信息。接口：GET /api/v2/market/data/share/stock-institutio… | 基础版 | [机构持股](https://market.ft.tech/gateway/doc/pages/nrsskpy6.md) |
| `stock-institution-holdings-detail` | 机构持股明细 | `/api/v2/market/data/share/stock-institution-holdings-detail` | 查询 A 股单票机构持仓详细信息。接口：GET /api/v2/market/data/share/stock-institution-h… | 基础版 | [机构持股明细](https://market.ft.tech/gateway/doc/pages/ov1vnlsg.md) |
| `stock-intraday` | 标的分时数据 2.0 | `/api/v4/market/data/stock-intraday` | 股票跨日分时行情，含均价与日累计量额（stock_intraday，GET /api/v4/market/data/stock-intra… | 专业版 | [标的分时数据 2.0](https://market.ft.tech/gateway/doc/pages/yl2uyd8x.md) |
| `stock-ipos` | 股票IPO | `/api/v1/market/data/stock-ipos` | 获取股票 IPO 列表。当用户需要获取 A 股 IPO 列表，含发行价格、发行数量、申购日期、上市日期等，支持分页查询，或了解股票 IPO… | 免费版 | [股票IPO](https://market.ft.tech/gateway/doc/pages/zrq7obzx.md) |
| `stock-limit` | 涨跌停价 | `/api/v1/market/data/stk-limit` | 查询每个标的每个交易日的昨收、涨停价、跌停价：可按交易日查全市场或单票，也可按标的分页查询历史区间。用户问涨跌停价、涨停/跌停幅度或某日全… | 免费版 | [涨跌停价](https://market.ft.tech/gateway/doc/pages/vh0xsf7t.md) |
| `stock-list-all-stocks` | 股票列表 | `/api/v1/market/data/stock-list` | 获取所有股票代码列表。当用户需要获取所有 A 股股票的代码和名称列表，支持沪深京股票，自动返回最新交易日的数据，或了解所有股票代码列表时使… | 免费版 | [股票列表](https://market.ft.tech/gateway/doc/pages/3ot2m3sk.md) |
| `stock-minute-seal` | 股票分钟封单金额 | `/api/v2/market/data/stock-minute-seal` | 查询股票分钟封单金额。接口：GET /api/v2/market/data/stock-minute-seal。用户问个股某日的分钟封单金… | 基础版 | [股票分钟封单金额](https://market.ft.tech/gateway/doc/pages/flxy83s5.md) |
| `stock-minutes` | 股票历史分钟行情 | `/api/v2/market/data/stock_minutes` | 股票历史分钟行情。必填 --symbol；可选日期和分页参数。 用户询问股票历史分钟行情时使用。 | 基础版 | [股票历史分钟行情](https://market.ft.tech/gateway/doc/pages/z9lsvrvu.md) |
| `stock-minutes-batch` | 批量股票历史分钟行情 | `/api/v2/market/data/stock_minutes/batch` | 批量查询多只 A 股的历史分钟 K 线（1 分钟及多分钟周期），含开高低收、成交量额、换手率与复权处理；必填 --symbols（逗号分隔… | 基础版 | [批量股票历史分钟行情](https://market.ft.tech/gateway/doc/pages/n12sln7b.md) |
| `stock-performance-express-all-stocks-specific-period` | 业绩快报 | `/api/v1/market/data/finance/stock-performance-express` | Get performance express (业绩快报) for all stocks in a specific reporting… | 免费版 | [业绩快报](https://market.ft.tech/gateway/doc/pages/ny95bwo1.md) |
| `stock-performance-forecast-all-stocks-specific-period` | 业绩预告 | `/api/v1/market/data/finance/stock-performance-forecast` | Get performance forecast (业绩预告) for all stocks in a specific reportin… | 免费版 | [业绩预告](https://market.ft.tech/gateway/doc/pages/zl1f9z4u.md) |
| `stock-quotes-list` | A股行情列表 | `/api/v1/market/data/daec/stocks` | 查询 A 股行情列表（分页）。当用户需要获取 A 股（沪深京）股票行情列表，支持按板块筛选、多字段排序与分页，用于行情中心「个股行情」等列… | 免费版 | [A股行情列表](https://market.ft.tech/gateway/doc/pages/mdsj0xyo.md) |
| `stock-realtime-day-kline` | 股票实时日K线 | `/api/v4/market/data/stock-realtime-day-kline` | 查询股票当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/stock-… | 专业版 | [股票实时日K线](https://market.ft.tech/gateway/doc/pages/pe9d82db.md) |
| `stock-realtime-minute-kline` | 股票实时分钟K线 | `/api/v4/market/data/stock-realtime-minute-kline` | 查询股票当前交易日实时 1 分钟 K 线。必填 --symbols，按空格分隔，单次最多 20 个。接口：GET /api/v4/mark… | 专业版 | [股票实时分钟K线](https://market.ft.tech/gateway/doc/pages/k4qem4nh.md) |
| `stock-share` | 股本 | `/api/v2/market/data/share/get-stock-share` | 查询股票股本信息。当用户需要查询某只 A 股在某日的总股本、A 股流通/限售/无限售股本、B 股股本、H 股股本、境外上市股本等股本结构，… | 基础版 | [股本](https://market.ft.tech/gateway/doc/pages/rmoimhs7.md) |
| `stock-share-chg` | 股东增减持 | `/api/v1/market/data/holder/stock-share-chg` | 查询 A 股股东增减持明细。当用户需要获取 A 股股东增减持数据（按 stock_code 分页查询全部历史，或以 is_last=tru… | 免费版 | [股东增减持](https://market.ft.tech/gateway/doc/pages/8n24xrdq.md) |
| `stock-signal-latest-snapshot` | 信号最新快照 | `/api/v3/market/data/stock-signal-latest-snapshot` | 查询股票最新计算信号快照。用户询问创新高/新低、连续上涨下跌、均线突破或量价信号时使用。 | 进阶版 | [信号最新快照](https://market.ft.tech/gateway/doc/pages/xhywfnzt.md) |
| `stock-st-history` | 股票历史ST状态 | `/api/v1/market/data/stock-st-history` | 查询 A 股股票历史风险警示（ST/*ST/PT/退市整理期）状态区间。Use when user asks about 股票历史ST状态… | 免费版 | [股票历史ST状态](https://market.ft.tech/gateway/doc/pages/hs1q3li4.md) |
| `stock-tech-factor` | 股票技术面因子 | `/api/v2/market/data/stock-factor` | 查询单只沪深北 A 股在指定交易日的基础行情、估值、股本及技术面因子。用户问某只股票的技术面因子、技术指标（MACD、KDJ、RSI、BO… | 基础版 | [股票技术面因子](https://market.ft.tech/gateway/doc/pages/6dkil79o.md) |
| `stock-unlock` | 限售解禁 | `/api/v1/market/data/unlock/stock_unlock` | 按证券代码查询限售解禁批次及股东明细，或按解禁日期范围查询全市场批次，批次维度分页。接口：GET /api/v1/market/data/… | 免费版 | [限售解禁](https://market.ft.tech/gateway/doc/pages/a3qlyxpp.md) |
| `supply-chain-companies` | 供应链公司候选 | `/api/v3/market/data/supply-chain/company-supply-chain-companies` | 查询指定 A 股公司的上游或下游行业及其公司候选，并按相邻行业记录分页返回。可用参数：--trade_code、--direction、-… | 基础版 | [供应链公司候选](https://market.ft.tech/gateway/doc/pages/jhcd4x3y.md) |
| `supply-chain-industry-names` | 供应链行业名称 | `/api/v3/market/data/supply-chain/industry-names` | 查询供应链行业名称全集。接口：GET /api/v3/market/data/supply-chain/industry-names。 | 基础版 | [供应链行业名称](https://market.ft.tech/gateway/doc/pages/z5k1xvhk.md) |
| `supply-chain-one-hop` | 供应链一跳关系 | `/api/v3/market/data/supply-chain/subindustry-supply-chain` | 查询指定行业的上游或下游相邻行业名称。可用参数：--industry_name、--direction。接口：GET /api/v3/ma… | 基础版 | [供应链一跳关系](https://market.ft.tech/gateway/doc/pages/6q0txaos.md) |
| `supply-chain-parent-subindustries` | 供应链子子行业父行业反查 | `/api/v3/market/data/supply-chain/subsubindustry-parent-subindustries` | 查询指定子子行业对应的父行业名称列表。可用参数：--subindustry_name。接口：GET /api/v3/market/data… | 基础版 | [供应链子子行业父行业反查](https://market.ft.tech/gateway/doc/pages/hqh0pm6q.md) |
| `supply-chain-subsubindustries` | 供应链子行业层级展开 | `/api/v3/market/data/supply-chain/subindustry-subsubindustries` | 查询指定行业直接对应的子子行业名称列表。可用参数：--industry_name。接口：GET /api/v3/market/data/s… | 基础版 | [供应链子行业层级展开](https://market.ft.tech/gateway/doc/pages/j7xpe5zx.md) |
| `supply-chain-subsubindustry-companies` | 供应链子子行业公司映射 | `/api/v3/market/data/supply-chain/subsubindustry-companies` | 查询指定子子行业对应的父行业、指数成分公司及公司明细。可用参数：--subindustry_name。接口：GET /api/v3/mar… | 基础版 | [供应链子子行业公司映射](https://market.ft.tech/gateway/doc/pages/64iwxu5j.md) |
| `suspension-list` | 停牌列表 | `/api/v1/market/data/suspension-list` | 查询停牌股票列表。可选 --trade-date。接口：GET /api/v1/market/data/suspension-list。 | 免费版 | [停牌列表](https://market.ft.tech/gateway/doc/pages/e42u4fqk.md) |
| `tdx-board-daily` | 通达信板块日线 | `/api/v1/market/data/tdx-board-daily` | 按日期范围查询通达信板块日线，返回板块标识、板块类型、开高低收、成交量和成交额等原始字段。接口：GET /api/v1/market/da… | 免费版 | [通达信板块日线](https://market.ft.tech/gateway/doc/pages/otlferf5.md) |
| `tdx-board-index` | 通达信板块指数最新快照 | `/api/v1/market/data/tdx-board-index` | 查询最新一期通达信板块指数快照，返回板块指数价格、昨收、涨速及领涨证券信息，无需传入日期。接口：GET /api/v1/market/da… | 免费版 | [通达信板块指数最新快照](https://market.ft.tech/gateway/doc/pages/tuzgkfun.md) |
| `tdx-board-members` | 通达信板块成分股最新快照 | `/api/v1/market/data/tdx-board-members` | 查询最新一期通达信板块与成分证券的对应关系，无需传入日期。接口：GET /api/v1/market/data/tdx-board-mem… | 免费版 | [通达信板块成分股最新快照](https://market.ft.tech/gateway/doc/pages/ek1t8pco.md) |
| `ths-all-board-kline` | 同花顺全板块K线 | `/api/v1/market/data/ths-all-board-kline` | Get THS all boards K-line by date range (同花顺全板块 K 线). Use when user a… | 免费版 | [同花顺全板块K线](https://market.ft.tech/gateway/doc/pages/6ujul8nk.md) |
| `ths-board-constituents` | 同花顺板块成分股 | `/api/v1/market/data/ths-board-constituents` | 查询同花顺板块成分股。当用户需要查同花顺概念/行业/地域/证监会板块包含哪些股票，或按板块名称、代码、类型检索成分股时使用。 | 免费版 | [同花顺板块成分股](https://market.ft.tech/gateway/doc/pages/sbu6tt44.md) |
| `ths-board-kline` | 同花顺板块K线 | `/api/v1/market/data/ths-board-kline` | 获取单个同花顺板块的历史日 K 线（开高低收 + 成交量），全部数值按字符串返回。可用参数：--board_code、--page、--p… | 免费版 | [同花顺板块K线](https://market.ft.tech/gateway/doc/pages/ck1zehfw.md) |
| `ths-concept-daily-flow` | 同花顺概念板块资金流日度 | `/api/v1/market/data/ths-concept-daily-flow` | 查询同花顺概念板块资金流日度。用户问同花顺概念板块资金流、概念板块每日净流入、概念板块主力流入、龙头股涨跌幅时使用。 | 免费版 | [同花顺概念板块资金流日度](https://market.ft.tech/gateway/doc/pages/hgcm2rnm.md) |
| `ths-hot-list` | 同花顺热榜 | `/api/v1/market/data/ths-hot-list` | 查询同花顺股票、ETF、债券、港股、美股、公募基金和期货热榜，支持按交易日分页查询。可用参数：--list_type、--trade_da… | 免费版 | [同花顺热榜](https://market.ft.tech/gateway/doc/pages/fbvl8umv.md) |
| `ths-industry-constituents` | 同花顺行业成分股列表 | `/api/v1/market/data/ths-industry-constituents` | 查询同花顺行业成分股列表。当用户需要查询指定同花顺行业的全部成分股代码和名称，或按股票代码/名称反查所属同花顺行业时使用。Use when… | 免费版 | [同花顺行业成分股列表](https://market.ft.tech/gateway/doc/pages/b54yn3wh.md) |
| `ths-industry-daily-flow` | 同花顺行业板块资金流日度 | `/api/v1/market/data/ths-industry-daily-flow` | 查询同花顺行业板块资金流日度。用户问同花顺行业板块资金流、行业板块每日净流入、行业资金流向、领涨股涨跌幅时使用。 | 免费版 | [同花顺行业板块资金流日度](https://market.ft.tech/gateway/doc/pages/n7u0assf.md) |
| `ths-stock-daily-flow` | 同花顺个股资金流日度 | `/api/v1/market/data/ths-stock-daily-flow` | 按日期范围查询同花顺个股日度资金流，返回股票代码和名称、收盘价、涨跌幅、换手率、资金流入/流出/净额及成交额。接口：GET /api/v1… | 免费版 | [同花顺个股资金流日度](https://market.ft.tech/gateway/doc/pages/rxbypzx4.md) |
| `trading-calendar` | 交易日历 | `/api/v1/market/data/time/trading-calendar` | 查询中国内地（cn）或香港（hk）市场在指定闭区间内的交易日列表。用户提到「交易日历」「A 股交易日」「港股交易日」「某区间内的交易日」「… | 免费版 | [交易日历](https://market.ft.tech/gateway/doc/pages/uqsqvzyv.md) |
| `xueqiu-rank` | 雪球股票排名 | `/api/v1/market/data/xueqiu-rank` | 查询雪球股票排行榜最新一期快照，支持按榜单组（关注/讨论/交易）与周期（本周新增/最热门）组合查询，返回排名、代码、简称、核心指标值、最新… | 免费版 | [雪球股票排名](https://market.ft.tech/gateway/doc/pages/kwt0flpu.md) |
| `yzxdr-detail` | 一致行动人明细 | `/api/v1/market/data/yzxdr-detail` | 按年份/季度（且可按股票代码过滤）查询一致行动人持股明细，返回每组一致行动人的合计持股比例与股数，以及组内每位股东的排名、持股数与市值、可… | 免费版 | [一致行动人明细](https://market.ft.tech/gateway/doc/pages/zpyi79up.md) |

## ETF专题（17）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `etf-adjust-factor` | ETF复权因子 | `/api/v1/market/data/etf-adjust-factor` | 查询 ETF 复权因子。支持 --symbol、--trade-date 或带 symbol 的 --start-date/--end-d… | 免费版 | [ETF复权因子](https://market.ft.tech/gateway/doc/pages/wj8y3my9.md) |
| `etf-announcements` | ETF公告列表 | `/api/v2/market/data/announcements/etf-announcements` | 查询 ETF 公告列表（etf_announcements），或按 url_hash 下载公告正文 PDF。用户问 ETF 公告、基金公告… | 基础版 | [ETF公告列表](https://market.ft.tech/gateway/doc/pages/azfxn177.md) |
| `etf-candlesticks` | ETFK线 | `/api/v1/market/data/etf-candlesticks` | 单只 ETF 历史日/周/月/年 K 线 GET 接口（market.ft.tech，etf-candlesticks）。用户问某只 ET… | 免费版 | [ETFK线](https://market.ft.tech/gateway/doc/pages/c3s30whl.md) |
| `etf-candlesticks-batch` | 批量ETFK线 | `/api/v2/market/data/etf-candlesticks/batch` | 批量查询多只 ETF 的历史 K 线（etf_candlesticks_batch）。用户问多只 ETF 日/周/月/年 K 线、批量 E… | 基础版 | [批量ETFK线](https://market.ft.tech/gateway/doc/pages/kz0hn1mk.md) |
| `etf-component-details` | ETF成分证券明细 | `/api/v2/market/data/etf-component-details` | 查询 ETF 成分证券明细（etf_component_details）。用户问 ETF 成分股明细、申赎清单成分证券、成分数量、现金替代… | 基础版 | [ETF成分证券明细](https://market.ft.tech/gateway/doc/pages/4cmtk12o.md) |
| `etf-components-all` | ETF成份列表 | `/api/v2/market/data/etf-components-all` | 查询全部或单只 ETF 成份列表。可选 --symbol；不传返回全部 ETF。接口：GET /api/v2/market/data/et… | 基础版 | [ETF成份列表](https://market.ft.tech/gateway/doc/pages/cksew5iy.md) |
| `etf-description-all` | ETF基础信息 | `/api/v2/market/data/etf-description-all` | 查询全部 ETF 基础信息（market.ft.tech）。用户问 ETF 列表、全部 ETF、ETF 代码与名称映射、按名称找 ETF … | 基础版 | [ETF基础信息](https://market.ft.tech/gateway/doc/pages/r31kkjvb.md) |
| `etf-minutes` | ETF历史分钟行情 | `/api/v2/market/data/etf_minutes` | ETF历史分钟行情。必填 --symbol；可选日期和分页参数。 用户询问ETF历史分钟行情时使用。 | 基础版 | [ETF历史分钟行情](https://market.ft.tech/gateway/doc/pages/oj78iq7k.md) |
| `etf-minutes-batch` | 批量ETF历史分钟行情 | `/api/v2/market/data/etf_minutes/batch` | 批量查询多只 ETF 的历史分钟 K 线（1 分钟及 5/15/30/60/120 等任意正整数周期），含开高低收、成交量额与复权处理；必… | 基础版 | [批量ETF历史分钟行情](https://market.ft.tech/gateway/doc/pages/uy7ivb2h.md) |
| `etf-net-value` | ETF净值 | `/api/v2/market/data/etf-net-value` | 查询 ETF 历史净值（etf_net_value）。用户问 ETF 净值、单位净值、累计净值、净值增长率、复权净值、每万份收益、7 日年… | 基础版 | [ETF净值](https://market.ft.tech/gateway/doc/pages/00pn98cv.md) |
| `etf-pcf-infos` | ETF申赎清单 | `/api/v2/market/data/etf-pcf/etf-pcf-infos` | 查询 ETF 申赎清单（PCF 汇总信息，etf_pcf_infos）。用户问 ETF 申赎清单、PCF 汇总、申购赎回单位、现金替代金额… | 基础版 | [ETF申赎清单](https://market.ft.tech/gateway/doc/pages/beq3ulj3.md) |
| `etf-pcfs` | ETF-PCF清单列表 | `/api/v2/market/data/etf-pcf/etf-pcfs` | 指定日期 ETF PCF 列表（market.ft.tech）。用户问 ETF PCF、申购赎回清单、指定日期 PCF 列表时使用。 | 基础版 | [ETF-PCF清单列表](https://market.ft.tech/gateway/doc/pages/82ffwm3o.md) |
| `etf-pre-data` | ETF盘前数据 | `/api/v2/market/data/etf-pre-data` | 获取指定交易日的全部 ETF 盘前信息（申赎单位、净值、现金差额、是否公布 IOPV、申赎允许情况、预估现金部分等）。可用参数：--dat… | 基础版 | [ETF盘前数据](https://market.ft.tech/gateway/doc/pages/gzgewm9p.md) |
| `etf-pre-single` | 单只ETF盘前数据 | `/api/v2/market/data/etf-pre-single` | 查询单只 ETF 盘前数据。用户问某只 ETF 盘前、申购赎回单位、净值、现金差额、IOPV、510300 盘前时使用。 | 基础版 | [单只ETF盘前数据](https://market.ft.tech/gateway/doc/pages/v7xq6ura.md) |
| `etf-realtime-day-kline` | ETF实时日K线 | `/api/v4/market/data/etf-realtime-day-kline` | 查询 ETF 当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/etf… | 专业版 | [ETF实时日K线](https://market.ft.tech/gateway/doc/pages/36kkwzxp.md) |
| `etf-realtime-minute-kline` | ETF实时分钟K线 | `/api/v4/market/data/etf-realtime-minute-kline` | 查询 ETF 当前交易日实时 1 分钟 K 线。必填 --symbols，按空格分隔，单次最多 20 个。接口：GET /api/v4/m… | 专业版 | [ETF实时分钟K线](https://market.ft.tech/gateway/doc/pages/rytblp5v.md) |
| `etf-share` | ETF份额 | `/api/v2/market/data/etf-share` | 查询 ETF 份额变动（etf_share）。用户问 ETF 份额、期末份额、申购赎回份额、份额净变动、份额变动率、ETF 份额历史时使用。 | 基础版 | [ETF份额](https://market.ft.tech/gateway/doc/pages/1bwbos96.md) |

## 债券专题（9）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `cb-lists` | 可转债列表 | `/api/v1/market/data/cb/cb-lists` | 可转债全量列表（market.ft.tech）。用户问可转债列表、全部可转债、转债代码列表、有哪些可转债时使用。 | 免费版 | [可转债列表](https://market.ft.tech/gateway/doc/pages/fpj2vwor.md) |
| `convertible-bond-candlesticks` | 可转债历史K线 | `/api/v1/market/data/convertible-bond-candlesticks` | 单只可转债历史日/周/月/年 K 线（convertible_bond_candlesticks，GET /api/v1/market/d… | 免费版 | [可转债历史K线](https://market.ft.tech/gateway/doc/pages/g1c884ww.md) |
| `convertible-bond-candlesticks-batch` | 批量可转债历史K线 | `/api/v2/market/data/convertible-bond-candlesticks/batch` | 批量查询多只可转债历史日/周/月/年 K 线（convertible_bond_candlesticks_batch，GET /api/v… | 基础版 | [批量可转债历史K线](https://market.ft.tech/gateway/doc/pages/k8ytss8s.md) |
| `convertible-bond-minutes` | 可转债历史分钟K线 | `/api/v2/market/data/convertible-bond-minute-candlesticks` | 可转债历史分钟 K 线，单只或批量（convertible_bond_minute_candlesticks，GET /api/v2/ma… | 基础版 | [可转债历史分钟K线](https://market.ft.tech/gateway/doc/pages/lla0sp86.md) |
| `convertible-bond-realtime-day-kline` | 可转债实时日K线 | `/api/v4/market/data/convertible-bond-realtime-day-kline` | 查询单只或批量可转债当前交易日实时日 K 线（GET /api/v4/market/data/convertible-bond-realt… | 专业版 | [可转债实时日K线](https://market.ft.tech/gateway/doc/pages/uzwf1a2t.md) |
| `convertible-bond-realtime-minute-kline` | 可转债实时分钟K线 | `/api/v4/market/data/convertible-bond-realtime-minute-kline` | 查询单只或批量可转债当前交易日实时 1 分钟 K 线（GET /api/v4/market/data/convertible-bond-r… | 专业版 | [可转债实时分钟K线](https://market.ft.tech/gateway/doc/pages/igkrpa9d.md) |
| `convertible-bond-szse-directed-trades` | 深交所可转债定向成交 | `/api/v1/market/data/convertible-bond/szse/directed-trades` | 查询深交所可转债定向成交公开信息。可用参数：--security-code、--trade-date、--page、--page-size… | 免费版 | [深交所可转债定向成交](https://market.ft.tech/gateway/doc/pages/axi47i8h.md) |
| `convertible-bond-szse-matching-trades` | 深交所可转债匹配成交 | `/api/v1/market/data/convertible-bond/szse/matching-trades` | 查询深交所披露的可转债匹配成交公开信息。可用参数：--security-code、--trade-date、--page、--page-s… | 免费版 | [深交所可转债匹配成交](https://market.ft.tech/gateway/doc/pages/yww4hh2l.md) |
| `convertible-bond-szse-negotiated-trades` | 深交所可转债协议成交 | `/api/v1/market/data/convertible-bond/szse/negotiated-trades` | 查询深交所可转债协议成交公开信息。可用参数：--security-code、--trade-date、--page、--page-size… | 免费版 | [深交所可转债协议成交](https://market.ft.tech/gateway/doc/pages/s3qatfk2.md) |

## 公募基金（18）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `fund-asset-allocation-single-fund-paginated` | 基金资产配置 | `/api/v1/market/data/fund/fund-asset-allocation` | 按基金代码查报告期资产配置。当用户需要查询基金总资产/净资产及股票/债券/基金/货币资金/其他资产的市值与占比，通过 report_dat… | 免费版 | [基金资产配置](https://market.ft.tech/gateway/doc/pages/b5wgtw9m.md) |
| `fund-basicinfo-single-fund` | 基金基础信息 | `/api/v1/market/data/fund/fund-basicinfo` | Get basic information of funds by fund code with pagination. Use when… | 免费版 | [基金基础信息](https://market.ft.tech/gateway/doc/pages/givmend6.md) |
| `fund-cal-return-single-fund-specific-period` | 基金收益 | `/api/v1/market/data/fund/fund-cal-return` | Get cumulative return time series for a specific fund over a given pe… | 免费版 | [基金收益](https://market.ft.tech/gateway/doc/pages/y8y3hv34.md) |
| `fund-classification-single-fund` | 基金分类 | `/api/v1/market/data/fund/fund-classification` | 查询基金在多套分类标准下的分类。当用户需要查询基金按证监会/晨星/银河证券等标准的分类，可按 classify_std 过滤时使用。 | 免费版 | [基金分类](https://market.ft.tech/gateway/doc/pages/j00607zo.md) |
| `fund-company-list-paginated` | 基金公司 | `/api/v1/market/data/fund/fund-company` | 分页查询基金公司列表及名下基金数量。当用户需要查询基金公司名称与名下基金数量，可按公司名精确过滤时使用。 | 免费版 | [基金公司](https://market.ft.tech/gateway/doc/pages/iuy3vkyw.md) |
| `fund-fee-single-fund-paginated` | 基金费率 | `/api/v1/market/data/fund/fund-fee` | 查询基金费率（当前有效，分页）。当用户需要查询基金日常申购费/赎回费/认购费/管理费/托管费/销售服务费，可按 charge_type 费… | 免费版 | [基金费率](https://market.ft.tech/gateway/doc/pages/gnzc5tcq.md) |
| `fund-holder-structure-single-fund` | 基金持有人结构 | `/api/v1/market/data/fund/fund-holder-structure` | 查询基金持有人结构（按报告期）。当用户需要查询基金持有人户数、户均持有份额、机构/个人/前十大持有人份额与比例等，可按 report_ty… | 免费版 | [基金持有人结构](https://market.ft.tech/gateway/doc/pages/c8538o8n.md) |
| `fund-index-tracking-funds` | 指数跟踪基金 | `/api/v2/market/data/fund/index-fund` | 按指数代码查询跟踪该指数的基金。当用户需要查询跟踪某只指数（如沪深 300）的全部基金（场内 ETF + 场外联接基金），或仅场内 ETF… | 基础版 | [指数跟踪基金](https://market.ft.tech/gateway/doc/pages/vfl9rnr6.md) |
| `fund-list-paginated` | 基金列表 | `/api/v1/market/data/fund/fund-list` | 分页查询公募基金基础列表。当用户需要查询基金代码/名称/交易代码/基金公司/经理/托管人/运作方式/类型/成立日期/规模等基金基础档案，可… | 免费版 | [基金列表](https://market.ft.tech/gateway/doc/pages/vct97ek2.md) |
| `fund-manager-relationship` | 基金经理任职关系 | `/api/v1/market/data/fund/fund-manager` | 按基金代码查历任/现任基金经理，或按基金经理姓名查其管理过的任职关系。当用户需要查基金经理姓名、职务、任职/离任日期、是否在任等，按 fu… | 免费版 | [基金经理任职关系](https://market.ft.tech/gateway/doc/pages/xju0x2mx.md) |
| `fund-net-value-detail-single-fund` | 基金净值明细 | `/api/v1/market/data/fund/fund-net-value` | 按基金代码查询基金净值明细。当用户需要查询基金单位/累计/复权净值、净值增长率、每万份基金收益、7 日年化等明细，通过 nav_date … | 免费版 | [基金净值明细](https://market.ft.tech/gateway/doc/pages/6b5i2aid.md) |
| `fund-net-value-performance-single-fund` | 基金净值收益表现 | `/api/v1/market/data/fund/fund-net-value-performance` | 按基金代码查净值口径收益表现。当用户需要查询基金多区间收益率（日/周/月/近三月/六月/今年/近一至十年/成立以来及对应年化收益率），通过… | 免费版 | [基金净值收益表现](https://market.ft.tech/gateway/doc/pages/u3nr8qes.md) |
| `fund-new-found-paginated` | 基金新发 | `/api/v1/market/data/fund/fund-new-found` | 查询新发基金（按成立日范围 + 倒序，分页）。当用户需要查询新发基金代码/名称/管理人/托管人/运作方式/类型/成立日期/成立规模等，可按… | 免费版 | [基金新发](https://market.ft.tech/gateway/doc/pages/nfbnt3tz.md) |
| `fund-overview-all-funds-paginated` | 基金总览 | `/api/v1/market/data/fund/fund-overview` | Get paginated overview information for all funds. Use when user asks … | 免费版 | [基金总览](https://market.ft.tech/gateway/doc/pages/gt3vpuzr.md) |
| `fund-portfolio-single-fund-paginated` | 基金持仓明细 | `/api/v1/market/data/fund/fund-portfolio` | 按基金代码查报告期持仓明细。当用户需要查询基金持仓股票/债券/转债的代码、名称、数量、市值、占净值比等，通过 report_date 单期… | 免费版 | [基金持仓明细](https://market.ft.tech/gateway/doc/pages/u3ixazhq.md) |
| `fund-risk-level-single-fund` | 基金风险等级 | `/api/v1/market/data/fund/fund-risk-level` | 查询基金风险等级。当用户需要查询基金风险等级（低/中低/中/中高/高，对应适当性 R1-R5）及其变更历史，可按 history=true… | 免费版 | [基金风险等级](https://market.ft.tech/gateway/doc/pages/ws3whvws.md) |
| `fund-share-single-fund-paginated` | 基金份额 | `/api/v1/market/data/fund/fund-share` | 按基金代码分页查询基金份额变动。当用户需要查询基金份额变动（期末/期初份额、申购赎回、份额变动率），按 stati_perd 统计周期（日… | 免费版 | [基金份额](https://market.ft.tech/gateway/doc/pages/0vi7kat2.md) |
| `fund-support-symbols-all-funds-paginated` | 基金支持标的 | `/api/v1/market/data/fund/fund-support-symbols` | Get paginated list of all supported fund symbols with code and name. … | 免费版 | [基金支持标的](https://market.ft.tech/gateway/doc/pages/87xbi3pr.md) |

## 指数专题（16）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `global-index-daily-kline` | 全球指数日K线 | `/api/v1/market/data/global-index/daily-kline` | 获取全球指数（含部分 A 股/港股宽基）的历史日K线，返回 `{total, items}` 结构（非分页，按时间区间一次性返回）。可用参… | 免费版 | [全球指数日K线](https://market.ft.tech/gateway/doc/pages/j0twmp6x.md) |
| `index-candlesticks` | 指数K线 | `/api/v1/market/data/index-candlesticks` | 单只指数历史日/周/月/年 K 线 GET 接口（market.ft.tech，index-candlesticks）。用户问某只指数的日… | 免费版 | [指数K线](https://market.ft.tech/gateway/doc/pages/gr2q0bjx.md) |
| `index-candlesticks-batch` | 批量指数K线 | `/api/v2/market/data/index-candlesticks/batch` | 批量查询多个指数的历史 K 线（index_candlesticks_batch）。用户问多个指数日/周/月/年 K 线、批量指数开高低收… | 基础版 | [批量指数K线](https://market.ft.tech/gateway/doc/pages/mrsinfcz.md) |
| `index-description-all` | 指数基础信息 | `/api/v1/market/data/index-description-all` | 查询全部指数基础信息（market.ft.tech）。用户问全部指数列表、指数简称全称、指数 PB/PE TTM、支持的指数清单、有哪些指… | 免费版 | [指数基础信息](https://market.ft.tech/gateway/doc/pages/ekyhuwqu.md) |
| `index-description-paginated` | 中证指数描述列表 | `/api/v1/market/data/index/index_description` | 含指数代码（纯 6 位 `index_code`）、名称、简介及其他描述字段。用户问指数描述分页、指数简介列表、某只指数简介、有哪些指数描… | 免费版 | [中证指数描述列表](https://market.ft.tech/gateway/doc/pages/y648z1s3.md) |
| `index-minutes` | 指数历史分钟行情 | `/api/v2/market/data/index_minutes` | 指数历史分钟行情。必填 --symbol；可选日期和分页参数。 用户询问指数历史分钟行情时使用。 | 基础版 | [指数历史分钟行情](https://market.ft.tech/gateway/doc/pages/ls85mq5n.md) |
| `index-minutes-batch` | 批量指数历史分钟行情 | `/api/v2/market/data/index_minutes/batch` | 批量查询多只 A 股指数的历史分钟 K 线（1 分钟及多分钟周期），含开高低收点位、成交量额；必填 --symbols（逗号分隔）与起止毫… | 基础版 | [批量指数历史分钟行情](https://market.ft.tech/gateway/doc/pages/5gbiz72k.md) |
| `index-realtime-day-kline` | 指数实时日K线 | `/api/v4/market/data/index-realtime-day-kline` | 查询指数当前交易日实时日 K 线。必填 --symbols，按空格分隔。接口：GET /api/v4/market/data/index-… | 专业版 | [指数实时日K线](https://market.ft.tech/gateway/doc/pages/g4mvoo8c.md) |
| `index-realtime-minute-kline` | 指数实时分钟K线 | `/api/v4/market/data/index-realtime-minute-kline` | 查询指数当前交易日实时 1 分钟 K 线。必填 --symbols，按空格分隔，单次最多 20 个。接口：GET /api/v4/mark… | 专业版 | [指数实时分钟K线](https://market.ft.tech/gateway/doc/pages/bzo0v549.md) |
| `index-weight-list` | 指数权重列表 | `/api/v1/market/data/index/index_weight` | 分页查询指数成份权重明细（market.ft.tech）。必填 index_code；可选 date、分页。每条含成份代码、名称、权重及该… | 免费版 | [指数权重列表](https://market.ft.tech/gateway/doc/pages/xym4pwjo.md) |
| `index-weight-summary` | 指数权重汇总 | `/api/v1/market/data/index/index_weight_summary` | 分页查询指数权重汇总（market.ft.tech）。可按 index_code 查询指定指数各期权重的 date 与 url_hash。… | 免费版 | [指数权重汇总](https://market.ft.tech/gateway/doc/pages/vezscfb4.md) |
| `sw-index-daily-quotes` | 申万指数日行情 | `/api/v1/market/data/sw-index/daily-quotes` | 查询申万指数日行情（sw_index_daily_quotes，GET /api/v1/market/data/sw-index/dail… | 免费版 | [申万指数日行情](https://market.ft.tech/gateway/doc/pages/59aeqfx9.md) |
| `sw-index-history-minutes` | 申万指数历史分钟K线 | `/api/v1/market/data/sw-index/history-minutes` | 按指数代码与日期区间查询申万指数的一分钟 K 线历史行情，返回分页结构（指数代码/名称、交易时间、开高低收、成交量额），支持 --all … | 免费版 | [申万指数历史分钟K线](https://market.ft.tech/gateway/doc/pages/vltgbxfw.md) |
| `sw-industry-constituent-history` | 申万行业成份股历史 | `/api/v1/market/data/sw-industry/constituent-history` | 查询单个申万行业当前有效的成份股归属记录。可用参数：--industry_code。接口：GET /api/v1/market/data/… | 免费版 | [申万行业成份股历史](https://market.ft.tech/gateway/doc/pages/os0w8opk.md) |
| `sw-industry-daily-metrics` | 申万行业日度指标 | `/api/v1/market/data/sw-industry/daily-metrics` | 查询单个申万行业的日频估值/资金/量价指标时间序列，包含 PE（LYR/TTM 及分位/中位数）、PB、股息率、换手率、总市值、收盘价、破… | 免费版 | [申万行业日度指标](https://market.ft.tech/gateway/doc/pages/9p19gdz0.md) |
| `sw-industry-overview` | 申万行业总览 | `/api/v1/market/data/sw-industry/overview` | 按交易日查询申万行业全部层级（一、二、三级行业）的估值概况快照，含成份股数、PE（LYR/TTM）及历史分位、PB 及分位、股息率及分位。… | 免费版 | [申万行业总览](https://market.ft.tech/gateway/doc/pages/x1q1shn7.md) |

## 期货数据（19）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `eastmoney-futures-position` | 东方财富期货持仓 | `/api/v1/market/data/eastmoney-futures-position` | 获取东方财富期货每日成交持仓排行榜数据，按合约/会员维度给出成交量、多头、空头、净多头、净空头的排名与持仓量及变化，含多头增/减仓、空头增… | 免费版 | [东方财富期货持仓](https://market.ft.tech/gateway/doc/pages/7al9wvew.md) |
| `eastmoney-futures-strange` | 东方财富期货龙虎榜 | `/api/v1/market/data/eastmoney-futures-strange` | 查询东方财富期货龙虎榜面板（成交量/持仓量多空排名等）。用户提到「东财期货龙虎榜」「期货龙虎榜面板」「期货会员排名」「eastmoney … | 免费版 | [东方财富期货龙虎榜](https://market.ft.tech/gateway/doc/pages/h5s1a7oc.md) |
| `futures-base-data` | 中国期货基础数据 | `/api/v1/market/data/futures/futures-base-data` | 查询指定交易日的期货合约要素，包括交易单位、最小变动价位、保证金、合约乘数、上市日、最后交易日和交割信息。可用参数：--trade-dat… | 免费版 | [中国期货基础数据](https://market.ft.tech/gateway/doc/pages/qd32szq6.md) |
| `futures-daily-kline` | 期货官方日K与9999主连 | `/api/v1/market/data/futures/daily-kline` | 查询期货真实合约或 9999 主连的官方日 K（futures_daily_kline，GET /api/v1/market/data/f… | 免费版 | [期货官方日K与9999主连](https://market.ft.tech/gateway/doc/pages/g7x1q4wp.md) |
| `futures-kline` | 期货合约历史K线 | `/api/v1/market/data/futures/kline` | 查询期货合约历史 K 线（期货合约日/周/月/季 K 线，futures_kline）。用户问期货合约 K 线、期货日K/周K/月K、合约… | 免费版 | [期货合约历史K线](https://market.ft.tech/gateway/doc/pages/j3w50zz7.md) |
| `futures-kline-batch` | 批量期货合约历史K线 | `/api/v2/market/data/futures/kline/batch` | 批量查询多个期货合约的历史 K 线（futures_kline_batch，GET /api/v2/market/data/futures… | 基础版 | [批量期货合约历史K线](https://market.ft.tech/gateway/doc/pages/0ausz81h.md) |
| `futures-limit` | 期货合约涨跌停价 | `/api/v1/market/data/futures/ft-limit` | 查询期货合约每日涨停价、跌停价。接口：GET /api/v1/market/data/futures/ft-limit。 | 免费版 | [期货合约涨跌停价](https://market.ft.tech/gateway/doc/pages/5nbz5zdb.md) |
| `futures-lists` | 中国期货列表 | `/api/v1/market/data/futures/futures-lists` | 查询指定交易日的期货合约列表，包括合约代码、交易所、品种、中文名称和合约类型。可用参数：--trade-date。接口：GET /api/… | 免费版 | [中国期货列表](https://market.ft.tech/gateway/doc/pages/rffbd7ih.md) |
| `futures-minutes` | 期货历史分钟K线 | `/api/v2/market/data/futures_minutes` | 期货历史分钟 K 线，单合约或批量（futures_minutes，GET /api/v2/market/data/futures_min… | 基础版 | [期货历史分钟K线](https://market.ft.tech/gateway/doc/pages/6je0p1c6.md) |
| `futures-minutes-single` | 期货历史分钟K线单合约 | `/api/v2/market/data/futures_minutes/single` | 查询单个期货合约的历史分钟 K 线（futures_minutes_single，GET /api/v2/market/data/futu… | 基础版 | [期货历史分钟K线单合约](https://market.ft.tech/gateway/doc/pages/1r54drig.md) |
| `futures-realtime-day-kline` | 期货实时日K线 | `/api/v4/market/data/futures-realtime-day-kline` | 查询期货合约当前交易日的实时日 K 线（futures_realtime_day_kline，GET /api/v4/market/dat… | 专业版 | [期货实时日K线](https://market.ft.tech/gateway/doc/pages/ko4fup34.md) |
| `futures-realtime-minute-kline` | 期货实时分钟K线 | `/api/v4/market/data/futures_minutes/realtime` | 查询期货合约当前交易日的实时 1 分钟 K 线（futures_minutes_realtime，GET /api/v4/market/d… | 专业版 | [期货实时分钟K线](https://market.ft.tech/gateway/doc/pages/tvhg1858.md) |
| `futures-settle` | 期货每日结算参数 | `/api/v1/market/data/futures/fut-settle` | 查询期货合约每日结算价、手续费和保证金参数。接口：GET /api/v1/market/data/futures/fut-settle。 | 免费版 | [期货每日结算参数](https://market.ft.tech/gateway/doc/pages/hvux2jh0.md) |
| `futures-warehouse-receipt` | 期货仓单日报 | `/api/v1/market/data/futures/fut-wsr` | 查询商品期货交易所发布的仓单日报明细。接口：GET /api/v1/market/data/futures/fut-wsr。 | 免费版 | [期货仓单日报](https://market.ft.tech/gateway/doc/pages/btn0gr4b.md) |
| `futures-weekly-detail` | 期货主要品种交易周报 | `/api/v1/market/data/futures/fut-weekly-detail` | 查询期货主要品种的周成交量、成交额、持仓量和周度变化。接口：GET /api/v1/market/data/futures/fut-wee… | 免费版 | [期货主要品种交易周报](https://market.ft.tech/gateway/doc/pages/wao8q91z.md) |
| `index-fut-depth` | 股指期货与指数深度行情 | `/api/v1/market/data/index-fut/depth` | 查询股指期货合约深度快照、对应指数价格与仪器映射（index_fut_depth，GET /api/v1/market/data/inde… | 免费版 | [股指期货与指数深度行情](https://market.ft.tech/gateway/doc/pages/7am2phuz.md) |
| `member-build-process` | 会员建仓过程 | `/api/v2/market/data/member-build-process` | 查询单个期货会员在指定合约/日期区间的持仓变化，并结合合约行情估算每日及累计盈亏。用户提到「会员建仓过程」「期货会员持仓盈亏」「会员净持仓… | 基础版 | [会员建仓过程](https://market.ft.tech/gateway/doc/pages/h32opb6k.md) |
| `member-position-ranking` | 会员持仓排名 | `/api/v2/market/data/member-position-ranking` | 查询指定交易日/交易所/合约/方向的期货会员持仓排名（品种/合约/方向/会员/持仓量/持仓量变化/净持仓）。用户提到「会员持仓排名」「期货… | 基础版 | [会员持仓排名](https://market.ft.tech/gateway/doc/pages/aftwyj12.md) |
| `nanhua-index-kline` | 南华期货指数日K线 | `/api/v1/market/data/futures/nanhua-index-kline` | 查询南华期货指数日 K 线，覆盖南华系列商品指数（`AD_NH`、`AG_NH`、`AL_NH`、`AO_NH`、`AP_NH` 等）。接… | 免费版 | [南华期货指数日K线](https://market.ft.tech/gateway/doc/pages/45cmhmre.md) |

## 现货数据（2）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `bullion-price` | 贵金属价格 | `/api/v1/market/data/bullion/price` | 查询指定标的的贵金属行情（日期 + 值），按 `start_date`/`end_date` 区间分页返回。接口：GET /api/v1/… | 免费版 | [贵金属价格](https://market.ft.tech/gateway/doc/pages/sl79u72x.md) |
| `sge-spot-description-all` | 上金所现货品种 | `/api/v1/market/data/sge-spot-description-all` | 查询上海黄金交易所（SGE）现货/延期品种主档全量列表（sge_spot_description_all，GET /api/v1/mark… | 免费版 | [上金所现货品种](https://market.ft.tech/gateway/doc/pages/jzxudwbp.md) |

## 港股数据（2）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `hk-candlesticks` | 港股K线 | `/api/v2/market/data/hk/hk-candlesticks` | 按港股代码查询日/月/季/年 K 线。用户问港股 K 线、日 K / 月 K / 季 K / 年 K、00700 历史行情、港股开高低收、… | 基础版 | [港股K线](https://market.ft.tech/gateway/doc/pages/k4v3vd8x.md) |
| `hsi-daily-weight` | 恒生指数每日权重 | `/api/v1/market/data/hk/hsi-daily-weight` | 查询恒生系列指数成份股权重（HSI 恒生指数 / HSCEI 国企指数 / HSAIT 等）。按交易日 + 指数/股票过滤（交易日必填）。… | 免费版 | [恒生指数每日权重](https://market.ft.tech/gateway/doc/pages/99ty9ak0.md) |

## 美股数据（2）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `eastmoney-us-stock-daily-ohlc` | 东方财富美股日OHLC | `/api/v1/market/data/eastmoney-us-stock-daily-ohlc` | 查询东财美股历史日 K 线。当用户需要查询东财美股历史日 K 线；有日期范围时按 3 天窗口分批请求，无日期范围时全量拉取，或了解东财美股… | 免费版 | [东方财富美股日OHLC](https://market.ft.tech/gateway/doc/pages/q4fuvuxi.md) |
| `eastmoney-us-stock-list` | 东方财富美股列表 | `/api/v1/market/data/eastmoney-us-stock-list` | 查询东方财富美股列表。Use when user asks for 美股列表、东财美股股票清单或美股代码。 | 免费版 | [东方财富美股列表](https://market.ft.tech/gateway/doc/pages/h5azbbob.md) |

## 宏观经济（23）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `chinabond-yield-daily` | 中债收益率曲线日度 | `/api/v1/market/data/chinabond-yield-daily` | 按日期范围查询中债收益率曲线日度数据。接口：GET /api/v1/market/data/chinabond-yield-daily。 | 免费版 | [中债收益率曲线日度](https://market.ft.tech/gateway/doc/pages/fubopatp.md) |
| `economic-china-cpi-monthly` | CPI | `/api/v1/market/data/economic/china-cpi` | Get China CPI monthly data (居民消费价格指数 月度). Use when user asks about CP… | 免费版 | [CPI](https://market.ft.tech/gateway/doc/pages/0v982m8z.md) |
| `economic-china-credit-loans-monthly` | 社融信贷 | `/api/v1/market/data/economic/china-credit-loans` | Get China credit/loans monthly data (中国信贷数据 月度). Use when user asks a… | 免费版 | [社融信贷](https://market.ft.tech/gateway/doc/pages/89eo4u6b.md) |
| `economic-china-customs-trade-monthly` | 进出口 | `/api/v1/market/data/economic/china-customs-trade` | Get China customs import/export monthly data (海关进出口 月度). Use when use… | 免费版 | [进出口](https://market.ft.tech/gateway/doc/pages/n6bu5izh.md) |
| `economic-china-fiscal-revenue-monthly` | 财政收入 | `/api/v1/market/data/economic/china-fiscal-revenue` | Get China fiscal revenue monthly data (中国财政收入月度). Use when user asks … | 免费版 | [财政收入](https://market.ft.tech/gateway/doc/pages/w515ivba.md) |
| `economic-china-fixed-asset-investment-monthly` | 固定资产投资 | `/api/v1/market/data/economic/china-fixed-asset-investment` | Get China urban fixed asset investment monthly data (城镇固定资产投资 月度). Us… | 免费版 | [固定资产投资](https://market.ft.tech/gateway/doc/pages/vp2bmxs5.md) |
| `economic-china-gdp-quarterly` | GDP | `/api/v1/market/data/economic/china-gdp` | Get China GDP quarterly data (中国 GDP 季度数据). Use when user asks about … | 免费版 | [GDP](https://market.ft.tech/gateway/doc/pages/egodfcdg.md) |
| `economic-china-industrial-added-value-monthly` | 工业增加值 | `/api/v1/market/data/economic/china-industrial-added-value` | Get China industrial added value growth monthly data (工业增加值增长 月度). Us… | 免费版 | [工业增加值](https://market.ft.tech/gateway/doc/pages/2tsc1z6m.md) |
| `economic-china-lpr-monthly` | LPR | `/api/v1/market/data/economic/china-lpr` | Get China LPR (Loan Prime Rate) monthly data (LPR 贷款市场报价利率 月度). Use w… | 免费版 | [LPR](https://market.ft.tech/gateway/doc/pages/wg95club.md) |
| `economic-china-money-supply-monthly` | 货币供应 | `/api/v1/market/data/economic/china-money-supply` | Get China money supply monthly data (货币供应量 M0/M1/M2 月度). Use when use… | 免费版 | [货币供应](https://market.ft.tech/gateway/doc/pages/twl6t7h1.md) |
| `economic-china-pmi-monthly` | PMI | `/api/v1/market/data/economic/china-pmi` | Get China PMI monthly data (中国 PMI 月度). Use when user asks about PMI,… | 免费版 | [PMI](https://market.ft.tech/gateway/doc/pages/s4xvqnu0.md) |
| `economic-china-ppi-monthly` | PPI | `/api/v1/market/data/economic/china-ppi` | Get China PPI monthly data (中国 PPI 工业品出厂价格指数 月度). Use when user asks … | 免费版 | [PPI](https://market.ft.tech/gateway/doc/pages/n6lijleg.md) |
| `economic-china-reserve-ratio-monthly` | 存款准备金率 | `/api/v1/market/data/economic/china-reserve-ratio` | Get China reserve requirement ratio monthly data (存款准备金率 月度). Use whe… | 免费版 | [存款准备金率](https://market.ft.tech/gateway/doc/pages/cl9tjf4p.md) |
| `economic-china-retail-sales-monthly` | 社零 | `/api/v1/market/data/economic/china-retail-sales` | Get China retail sales of consumer goods monthly data (社会消费品零售总额 月度).… | 免费版 | [社零](https://market.ft.tech/gateway/doc/pages/hped3tpp.md) |
| `economic-china-tax-revenue-monthly` | 税收 | `/api/v1/market/data/economic/china-tax-revenue` | Get China tax revenue monthly data (全国税收收入 月度). Use when user asks ab… | 免费版 | [税收](https://market.ft.tech/gateway/doc/pages/ht6ox0mg.md) |
| `economic-us-economic-by-type` | 美国经济指标 | `/api/v1/market/data/economic/us-economic` | Get US economic indicator time series by type (美国经济指标按类型查询). Use when… | 免费版 | [美国经济指标](https://market.ft.tech/gateway/doc/pages/vatd7paf.md) |
| `financial-calendar` | 百度财经日历 | `/api/v1/market/data/finance/financial-calendar/baidu` | 按日期范围查询财经日历（market.ft.tech），含华尔街见闻与百度财经日历数据（宏观数据、IPO、财报时间、交易提醒等）。用户问财… | 免费版 | [百度财经日历](https://market.ft.tech/gateway/doc/pages/vlqbh6t9.md) |
| `hibor-daily` | HIBOR日度利率 | `/api/v1/market/data/hibor-daily` | 按日期范围查询香港银行同业拆借利率（HIBOR）日度数据。可用参数：--start_date、--end_date、--page、--pa… | 免费版 | [HIBOR日度利率](https://market.ft.tech/gateway/doc/pages/wcjgmvoj.md) |
| `libor-daily` | 国际基准利率日度 | `/api/v1/market/data/libor-daily` | 按日期范围查询国际基准利率日度数据。接口：GET /api/v1/market/data/libor-daily。 | 免费版 | [国际基准利率日度](https://market.ft.tech/gateway/doc/pages/pyj0csm9.md) |
| `shibor-daily` | SHIBOR日度利率 | `/api/v1/market/data/shibor-daily` | 按日期范围查询上海银行间同业拆放利率（Shibor）日度数据。可用参数：--start_date、--end_date、--page、--… | 免费版 | [SHIBOR日度利率](https://market.ft.tech/gateway/doc/pages/3jnxyzmy.md) |
| `shibor-quote-daily` | SHIBOR报价日度 | `/api/v1/market/data/shibor-quote-daily` | 按日期范围查询 Shibor 报价行日度报价。接口：GET /api/v1/market/data/shibor-quote-daily。 | 免费版 | [SHIBOR报价日度](https://market.ft.tech/gateway/doc/pages/optr82sd.md) |
| `wallstreetcn-financial-calendar` | 华尔街见闻财经日历 | `/api/v1/market/data/finance/financial-calendar/wallstreetcn` | 查询华尔街见闻（wallstreetcn）财经日历，按日期范围返回该区间内的经济事件。可用参数：--start_date、--end_da… | 免费版 | [华尔街见闻财经日历](https://market.ft.tech/gateway/doc/pages/jvg7kkmv.md) |
| `wz-index-daily` | 温州民间融资综合利率指数日度 | `/api/v1/market/data/wz-index-daily` | 按日期范围查询温州民间融资综合利率指数及分项利率。可用参数：--start_date、--end_date、--page、--page_s… | 免费版 | [温州民间融资综合利率指数日度](https://market.ft.tech/gateway/doc/pages/e4w9tgm2.md) |

## 大模型语料（7）

| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |
|---|---|---|---|---|---|
| `market-announcements` | 全市场公告列表 | `/api/v2/market/data/announcements/market-announcements` | 查询全市场上市公司公告列表，或按 url_hash 下载公告原文 PDF（market_v2_announcements_market_a… | 免费版 | [全市场公告列表](https://market.ft.tech/gateway/doc/pages/3eyc3hn0.md) |
| `periodic-reports` | 定期报告列表 | `/api/v2/market/data/announcements/periodic-reports` | 查询上市公司定期报告（年报/半年报/一季报/三季报）列表，或按 url_hash 下载报告原文 PDF（market_v2_announc… | 免费版 | [定期报告列表](https://market.ft.tech/gateway/doc/pages/6ktm9ygz.md) |
| `semantic-search-news` | 新闻语义搜索 | `/api/v3/market/data/semantic-search-news` | 语义搜索新闻（market.ft.tech）。用户问语义搜新闻、按关键词搜新闻、搜索相关新闻时使用。数据仅支持当年、最近半个月。 | 进阶版 | [新闻语义搜索](https://market.ft.tech/gateway/doc/pages/kwjie41c.md) |
| `shareholder-meeting` | 股东大会 | `/api/v1/market/data/corporate/meeting` | 查询A股上市公司股东大会信息（market.ft.tech）。用户问股东大会、股东会议、股权登记日、投票日期、会议提案时使用。 | 免费版 | [股东大会](https://market.ft.tech/gateway/doc/pages/df11taap.md) |
| `stock-announcements` | 公告列表 | `/api/v2/market/data/announcements/stock-announcements` | 查询 A 股公告列表，或按 url_hash 下载公告正文 PDF。用户问某只股票的公告、按日期查全市场公告、要公告原文 PDF 时使用。 | 基础版 | [公告列表](https://market.ft.tech/gateway/doc/pages/j61mozzt.md) |
| `stock-prospectuses` | 招股书列表 | `/api/v2/market/data/announcements/stock-prospectuses` | 查询 A 股招股书及相关发行公告列表（stock_prospectuses，GET /api/v2/market/data/announc… | 免费版 | [招股书列表](https://market.ft.tech/gateway/doc/pages/xppnfsz6.md) |
| `stock-reports` | 研报列表 | `/api/v2/market/data/report/stock-reports` | 查询 A 股研报列表。按 stock-code 查询个股历史，或按 type 与日期范围查询；page 和 page-size 必填。 | 基础版 | [研报列表](https://market.ft.tech/gateway/doc/pages/g7615auf.md) |
