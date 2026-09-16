---
name: fund-classification-single-fund
description: "查询基金在多套分类标准下的分类。当用户需要查询基金按证监会/晨星/银河证券等标准的分类，可按 classify_std 过滤时使用。"
---

# 基金分类

## 接口说明

| 项目     | 说明                                                              |
|----------|-------------------------------------------------------------------|
| 接口名称 | 基金分类                                                   |
| 外部接口 | `/api/v1/market/data/fund/fund-classification`                                  |
| 请求方式 | GET                                                                |

## 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `--fund_code` | string | 是 | 基金代码（trade_code 形式，如 000001 或 000001.OF） |
| `--classify_std` | string | 否 | 分类标准：证监会基金分类/晨星基金分类/银河证券分类2017版，缺省全部 |

## 执行方式

通过根目录的 `run.py` 调用（推荐）：

```bash
python <RUN_PY> fund-classification-single-fund --fund_code 000001 --classify_std 晨星基金分类
```

> `<RUN_PY>` 为主 `SKILL.md` 同级的 `run.py` 绝对路径。

## 响应结构

JSON 对象或数组，结构请参考 [ftshare-doc](../..) 接口文档。

## 注意事项

- 必填参数必须提供。
- 响应以 JSON 格式输出至 stdout，诊断信息输出至 stderr。
