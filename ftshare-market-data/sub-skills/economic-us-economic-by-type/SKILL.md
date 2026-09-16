---
name: economic-us-economic-by-type
description: Get US economic indicator time series by type (美国经济指标按类型查询). Use when user asks about 美国 ISM, 美国非农, 美国 CPI/PPI, 美国失业率, 美国贸易帐, 美国新屋开工, 美国成屋销售, 美国耐用品订单, 美国咨商会信心指数, 美国 GDP 年率, 美国联邦基金利率, US economic data.
---

# 美国经济指标 - 按类型查询

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 按类型查询美国经济指标（统一接口） |
| 外部接口 | GET /api/v1/market/data/economic/us-economic |
| 请求方式 | GET |
| 适用场景 | 通过参数 `type` 指定指标类型，获取对应美国经济指标的时间序列（时间、前值、现值、发布日期）；支持 16 类指标 |

## 2. 请求参数

说明：`type` 为必填项，指定要查询的指标类型。

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| type | string | 是 | 指标类型 | ism-manufacturing | 见下方「type 取值列表」 |

### type 取值列表

| type 值 | 说明 | 单位/备注 |
|---------|------|-----------|
| ism-manufacturing | 美国 ISM 制造业指数 | 百分比 |
| ism-non-manufacturing | 美国 ISM 非制造业指数 | 百分比 |
| nonfarm-payroll | 美国非农就业人数变化 | 万人（接口已换算） |
| trade-balance | 美国贸易帐 | 亿美元（接口已换算） |
| unemployment-rate | 美国失业率 | 百分比 |
| ppi-mom | 美国生产者物价指数月率 | 百分比 |
| cpi-mom | 美国消费者物价指数月率 | 百分比 |
| cpi-yoy | 美国消费者物价指数年率 | 百分比 |
| core-cpi-mom | 美国核心消费者物价指数月率 | 百分比 |
| core-cpi-yoy | 美国核心消费者物价指数年率 | 百分比 |
| housing-starts | 美国新屋开工 | 万户（接口已换算） |
| existing-home-sales | 美国成屋销售 | 万套 |
| durable-goods-orders-mom | 美国耐用品订单月率 | 百分比 |
| cb-consumer-confidence | 美国咨商会消费者信心指数 | 无单位 |
| gdp-yoy-preliminary | 美国 GDP 年率初值 | 百分比；季度数据，时间为「YYYY年第N季度」 |
| fed-funds-rate-upper | 美国央行公布利率决议（上限） | 百分比 |

## 3. 用法

从用户问题中识别要查的美国经济指标类型，对应到上表 `type` 值，执行：

```bash
python script/handler.py --type <type值>
```

示例：

```bash
python script/handler.py --type ism-manufacturing
python script/handler.py --type nonfarm-payroll
python script/handler.py --type cpi-mom
python script/handler.py --type fed-funds-rate-upper
```

脚本输出 JSON 数组，按时间倒序，每项含 `month`（或季度格式）、`prev_value`、`current_value`、`release_date`，以表格展示给用户。

## 4. 响应说明

返回值为该指标的时间序列数组，按时间倒序。

### 单条记录结构（UsEconomicItem）

| 字段名 | 类型 | 是否可为空 | 说明 | 单位 |
|--------|------|------------|------|------|
| month | String | 否 | 时间；月度为「YYYY年MM月」，季度（如 GDP）为「YYYY年第N季度」 | - |
| prev_value | Number/String | 是 | 上一期数值 | 见各 type 说明 |
| current_value | Number/String | 是 | 当期数值，最新期可能为 null | 见各 type 说明 |
| release_date | String | 否 | 发布日期，YYYY-MM-DD | - |

说明：部分指标为季度（如 gdp-yoy-preliminary），其余为月度。

## 5. 请求示例

```
GET /api/v1/market/data/economic/us-economic?type=ism-manufacturing
```

## 6. 注意事项

- 必须传入合法的 `type`，否则接口可能报错或返回空。
- 数组按时间倒序，最新在前；数值单位见各 type 说明。

## 调用示例

```bash
python <RUN_PY> economic-us-economic-by-type --type cpi-yoy
```
