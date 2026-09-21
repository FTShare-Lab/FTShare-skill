---
name: kline-archives
description: 查询和下载 FTShare 年度分K归档包（kline_archives / kline_archives_download）。用户要下载历史分钟K线全量数据、按年份拉取分钟行情归档、问有哪些年份的分钟数据包可下载时使用。
---

# 年度分K归档包

## 1. 接口描述

| 项目 | 说明 |
|------|------|
| 接口名称 | 年度分K归档包（kline_archives / kline_archives_download） |
| 外部接口 | `GET /api/v2/market/data/kline-archives`（清单）<br>`GET /api/v2/market/data/kline-archives/{year}/download`（下载） |
| 请求方式 | GET（清单无参数；下载为路径参数） |
| 适用场景 | 需要某个年份全市场分钟K线全量数据时，先查清单确认年份，再下载对应归档包 |

同一个子 skill 两种模式：

1. **清单模式**（不带 `--year`）：列出可下载的年份、包大小与 sha256。
2. **下载模式**（带 `--year`）：下载该年份的归档包到本地。

## 2. 请求参数

清单模式无参数。下载模式：

| 参数名 | 类型 | 是否必填 | 描述 | 取值示例 | 备注 |
|--------|------|----------|------|----------|------|
| year | int | 是 | 年份 | 2023 | 4 位数字，且必须出现在清单里 |
| --output | string | 否 | 落盘路径 | ./archives/2023.zst | 默认 `ftshare_1m_<year>.tar.zst`；必须在当前工作目录内 |
| --retries | int | 否 | 额外重试次数 | 3 | 默认 3（即最多尝试 4 次） |
| --timeout | int | 否 | 单次网络读超时秒数 | 60 | 默认 60 |
| --force | - | 否 | 目标已存在也强制重下 | - | 不带时，已存在且 sha256 与清单一致就直接返回 |

## 3. 响应说明

清单模式返回外层 `code` / `message` / `data`，`data` 为数组：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| year | int | 归档包对应年份 |
| size_bytes | int | 归档包字节数 |
| last_modified | string | 归档包生成时间（ISO 8601，UTC） |
| sha256 | string | 归档包 sha256，下载完成后据此校验完整性 |

下载模式不打印 JSON，只向 stdout 输出落盘后的文件路径。

归档包为 zstd 压缩 tar，解包后是按标的拆分的分钟K线（如 `1m/002142.XSHE.csv.gz`）。单包体积在 4–5 GB 量级，下载耗时以十分钟计。

## 4. 调用方式

```bash
# 清单：列出可下载的年份
python <RUN_PY> kline-archives

# 下载指定年份（默认落到当前目录的 ftshare_1m_2023.tar.zst）
python <RUN_PY> kline-archives --year 2023

# 指定落盘路径与重试次数
python <RUN_PY> kline-archives --year 2023 --output ./archives/2023.zst --retries 5
```

`<RUN_PY>` 为主 SKILL.md 同级 `run.py` 的绝对路径。

## 5. 注意事项

- 下载前会用清单校验年份；年份不在清单内直接报错退出，不会发起下载。
- 支持断点续传：半成品写在 `<目标文件>.part`，旁边 `./<目标文件>.part.meta` 记录来源 URL 与服务端 ETag。中断后重新执行同一条命令即可从断点继续。
- 续传带 `If-Range`：归档包在服务端被重新生成过（ETag 变化）时会自动丢弃半成品、整包重下，不会把新旧数据拼成坏包。
- 网络异常、`429`、`5xx` 与 `416` 会按 `--retries` 重试；其它 HTTP 错误立即失败。
- 下载完成后按清单的 `size_bytes` 与 `sha256` 校验，不一致会删除半成品并以非零状态退出。
- 目标文件已存在且 sha256 与清单一致时直接返回路径，不重新下载；需要强制重下用 `--force`。
- 落盘路径必须在当前工作目录及其子目录内，否则以非零状态退出。
