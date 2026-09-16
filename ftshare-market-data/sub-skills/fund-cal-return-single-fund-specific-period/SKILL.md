---
name: fund-cal-return-single-fund-specific-period
description: Get cumulative return time series for a specific fund over a given period. Use when user asks about 基金累计收益率, 近1年/近3个月收益, YTD收益, 基金收益曲线.
---

# 查询指定基金在指定区间的累计收益率

## 参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--fund-code` | string | 是 | 6 位数字基金代码 | `159619` |
| `--cal-type` | string | 是 | 区间类型：`1M` / `3M` / `6M` / `1Y` / `3Y` / `5Y` / `YTD` | `1Y` |

## 用法

通过主目录 `run.py` 调用（必填 `--fund-code`、`--cal-type`）：

```bash
python <RUN_PY> fund-cal-return-single-fund-specific-period --fund-code 159619 --cal-type 1Y
```

`<RUN_PY>` 为主 SKILL.md 同级的 `run.py` 绝对路径。脚本输出 JSON 数组，每项含 `date`（YYYYMMDD 整型）和 `return`（小数形式累计收益率），按时间序列展示。

## 注意

- 响应为数组，不是分页结构
- `return` 为小数（如 0.0234 表示 2.34%），展示时可乘以 100 转为百分比
- 区间选项：`1M`（近1月）、`3M`（近3月）、`6M`（近6月）、`1Y`（近1年）、`3Y`（近3年）、`5Y`（近5年）、`YTD`（今年来）
- 若用户只给基金名称，建议先用 `fund-support-symbols-all-funds-paginated` 或 `fund-overview-all-funds-paginated` 查到对应 6 位 `fund-code` 再查询收益。
