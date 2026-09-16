---
name: stk-managers
description: "查询上市公司管理层人员信息。用户问上市公司管理层、高管、董事、独立董事、董事长、总经理、任职区间、候选日期、董监高、平安银行管理层、600848 高管时使用。参数 trade_code 必填且需带 .SZ/.SH 后缀，支持逗号分隔多个代码。"
---

# 查询上市公司管理层信息

## 接口说明

| 项目     | 说明                                                    |
|----------|---------------------------------------------------------|
| 接口名称 | 查询上市公司管理层人员信息                                |
| 外部接口 | `/api/v1/market/data/stk-managers`                      |
| 请求方式 | GET                                                     |
| 适用场景 | 查询上市公司管理层人员，含姓名、岗位类别、职位、任职区间等 |

## 请求参数

| 参数名      | 类型   | 是否必填 | 描述                                                | 取值示例     | 备注                                                                  |
|-------------|--------|----------|-----------------------------------------------------|--------------|-----------------------------------------------------------------------|
| trade_code  | string | 是       | 股票代码                                            | 600848.SH    | 带 .SZ/.SH 后缀，支持逗号分隔多个，如 `600848.SH,000001.SZ`            |
| candi_date  | string | 否       | 候选日期，精确匹配                                  | 20251128     | `YYYYMMDD` 格式                                                       |
| begin_date  | string | 否       | 任职起始日过滤                                      | 20200101     | `YYYYMMDD` 格式                                                       |
| end_date    | string | 否       | 任职截止日过滤                                      | 20241231     | `YYYYMMDD` 格式；与 `begin_date` 同时提供时须 `begin_date` ≤ `end_date` |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> stk-managers --trade_code 600848.SH
python <RUN_PY> stk-managers --trade_code 600848.SH --begin_date 20200101 --end_date 20241231
python <RUN_PY> stk-managers --trade_code 600848.SH,000001.SZ
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

```json
[
    {
        "trade_code": "000001.SZ",
        "security_name": "平安银行",
        "name": "杨运杰",
        "s_type": "董事",
        "position": "独立董事",
        "birth": "19660101",
        "candi_date": "20251128",
        "begin_date": "20260326",
        "end_date": "20281215",
        "is_job": "在任",
        "change_reason": ""
    }
]
```

### 字段说明

| 字段名          | 类型   | 是否可为空 | 说明                                            |
|-----------------|--------|------------|-------------------------------------------------|
| trade_code      | string | 否         | 股票代码（带 .SZ/.SH 后缀）                      |
| security_name   | string | 否         | 股票名称                                        |
| name            | string | 否         | 管理人员姓名                                    |
| s_type          | string | 否         | 岗位类别（如「高管」「董事」等）                 |
| position        | string | 否         | 职位                                            |
| birth           | string | 否         | 出生年月（`YYYYMMDD`）                          |
| candi_date      | string | 否         | 候选日期（`YYYYMMDD`）                          |
| begin_date      | string | 否         | 任职起始日（`YYYYMMDD`；空字符串表示无确切起始日）|
| end_date        | string | 否         | 任职截止日（`YYYYMMDD`；空字符串表示在职）       |
| is_job          | string | 否         | 是否在职                                        |
| change_reason   | string | 否         | 变动原因                                        |

## 注意事项

- `trade_code` 必填，为空时接口返回 400。
- 不分页，单只股票一次性返回全部管理层记录；多 `trade_code`（逗号分隔）时合并返回。
- 日期参数格式为 `YYYYMMDD`，非时间戳。
