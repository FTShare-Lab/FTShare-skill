#!/usr/bin/env python3
"""
ftshare-market-data 统一调度入口。

用法：
    python run.py <subskill名> [handler参数...]
    python run.py --index            # 列出全部子技能（名称 / 路由 / 触发场景），用于路由
    python run.py --index --json     # 同上，JSON 输出（程序化匹配）

示例：
    python run.py stock-list-all-stocks
    python run.py stock-quotes-list --order_by "change_rate desc" --page_no 1 --page_size 30
    python run.py stock-ipos --page 1 --page_size 20
    python run.py block-trades
    python run.py margin-trading-details --page 1 --page_size 20
    python run.py semantic-search-news --query 人工智能
    python run.py cb-lists
    python run.py etf-pcfs --date 20260309
    python run.py fund-basicinfo-single-fund --fund-code 000001
    python run.py hk-candlesticks --trade-code 00700.HK --interval-unit day --until-date 2026-03-24 --since-date 2026-03-01 --limit 20
    python run.py index-weight-summary --page 1 --page-size 20
    python run.py index-weight-list --index-code 000300 --page 1 --page-size 20

"""
import json
import os
import re
import runpy
import sys

SKILL_ROOT = os.path.dirname(os.path.abspath(__file__))
SUB_SKILLS_DIR = os.path.join(SKILL_ROOT, "sub-skills")
INDEX_JSON = os.path.join(SUB_SKILLS_DIR, "INDEX.json")


def _allowed_subskills():
    """仅允许 sub-skills 目录下存在 scripts/handler.py 的名称，防止路径遍历。"""
    allowed = set()
    if not os.path.isdir(SUB_SKILLS_DIR):
        return allowed
    for name in os.listdir(SUB_SKILLS_DIR):
        if os.path.isfile(os.path.join(SUB_SKILLS_DIR, name, "scripts", "handler.py")):
            allowed.add(name)
    return allowed


def _load_index():
    """读取 tools/index_skills.py 生成的索引；缺失或损坏时返回空列表。"""
    try:
        with open(INDEX_JSON, encoding="utf-8") as handle:
            payload = json.load(handle)
        rows = payload.get("skills")
        return rows if isinstance(rows, list) else []
    except (OSError, ValueError):
        return []


def _frontmatter_description(name):
    path = os.path.join(SUB_SKILLS_DIR, name, "SKILL.md")
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return ""
    match = re.search(r"^description:\s*(.+)$", text, re.M)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def _summary(text, limit=88):
    text = " ".join(text.split())
    if not text:
        return ""
    first = re.split(r"(?<=。)|(?<=\.)\s", text)[0]
    return first if len(first) <= limit else first[: limit - 1] + "…"


def _print_index(as_json=False):
    rows = _load_index()
    if not rows:
        allowed = _allowed_subskills()
        rows = [{"skill": n, "route": "", "description": _frontmatter_description(n),
                 "doc_title": "", "doc_url": "", "category": ""} for n in sorted(allowed)]
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    width = max((len(r["skill"]) for r in rows), default=10)
    for row in rows:
        line = f"  {row['skill']:<{width}}  {_summary(row.get('description', ''))}".rstrip()
        print(line)
    print(f"\n共 {len(rows)} 个子技能。调用：python run.py <subskill名> [参数...]", file=sys.stderr)
    return 0


def _execute_handler(handler, handler_args):
    """在当前进程执行 handler.py，避免 subprocess 告警。

    不改变进程工作目录：handler 路径已是绝对路径，而下载类 handler 需要
    以调用方的工作目录为落盘根目录。
    """
    old_argv = sys.argv[:]
    try:
        sys.argv = [handler] + handler_args
        runpy.run_path(handler, run_name="__main__")
        return 0
    except SystemExit as e:
        code = e.code
        if isinstance(code, int):
            return code
        return 1 if code else 0
    finally:
        sys.argv = old_argv


def main():
    allowed = _allowed_subskills()

    if len(sys.argv) < 2:
        print("用法: python run.py <subskill名> [参数...]", file=sys.stderr)
        print("      python run.py --index [--json]   # 按描述列出全部子技能", file=sys.stderr)
        print("\n可用 subskill（名称 + 触发场景）：")
        sys.exit(_print_index() or 1)

    if sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)

    if sys.argv[1] == "--index":
        sys.exit(_print_index(as_json="--json" in sys.argv[2:]))

    subskill = sys.argv[1]
    if subskill not in allowed:
        print(f"错误：未找到 subskill '{subskill}'，或名称不合法。", file=sys.stderr)
        print("提示：python run.py --index 可列出全部子技能及其触发场景。", file=sys.stderr)
        sys.exit(1)

    handler = os.path.join(SUB_SKILLS_DIR, subskill, "scripts", "handler.py")
    sys.exit(_execute_handler(handler, sys.argv[2:]))


if __name__ == "__main__":
    main()
