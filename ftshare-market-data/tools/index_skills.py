#!/usr/bin/env python3
"""生成并校验子技能索引（INDEX.md / INDEX.json / manifest.tsv / README 能力总览表）。

用法：
    python3 tools/index_skills.py --write    # 重新生成索引文件与 README 表格
    python3 tools/index_skills.py --check    # 校验索引是否与仓库一致（CI 用）

数据来源全部在仓库内，不访问网络、不依赖外部仓库：
- route          ← sub-skills/<name>/scripts/handler.py 的公开路由字面量
- 文档标题/链接/套餐 ← sub-skills/doc-map.tsv（route → title / url / tier / category）
- description    ← 各子技能 SKILL.md 的 frontmatter
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUB_SKILLS = ROOT / "sub-skills"
DOC_MAP = SUB_SKILLS / "doc-map.tsv"
INDEX_MD = SUB_SKILLS / "INDEX.md"
INDEX_JSON = SUB_SKILLS / "INDEX.json"
MANIFEST = SUB_SKILLS / "manifest.tsv"
README = ROOT / "README.md"
README_BEGIN = "<!-- BEGIN: skills-table -->"
README_END = "<!-- END: skills-table -->"
CATEGORY_ORDER = [
    "股票数据", "ETF专题", "债券专题", "公募基金", "指数专题", "期货数据",
    "现货数据", "港股数据", "美股数据", "宏观经济", "大模型语料",
]


def handler_route(handler: Path) -> str | None:
    try:
        text = handler.read_text(encoding="utf-8")
    except OSError:
        return None
    found = re.findall(r"api/v[1-4]/market/[A-Za-z0-9_\-/{}.]+", text)
    return "/" + found[0].rstrip("?/") if found else None


def load_doc_map() -> dict[str, dict]:
    """route -> {title, url, md, tier, category}"""
    result: dict[str, dict] = {}
    if not DOC_MAP.is_file():
        return result
    with DOC_MAP.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            route = (row.get("route") or "").strip()
            if not route:
                continue
            url = (row.get("doc_url") or "").strip()
            slug = url.rsplit("/", 1)[-1] if url else ""
            result[route] = {
                "title": (row.get("doc_title") or "").strip(),
                "url": url,
                "md": f"https://market.ft.tech/gateway/doc/pages/{slug}.md" if slug else "",
                "tier": (row.get("tier") or "").strip(),
                "category": (row.get("category") or "").strip(),
            }
    return result


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    block = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not block:
        return {}
    out = {}
    for line in block.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def build_rows() -> list[dict]:
    doc_map = load_doc_map()
    rows: list[dict] = []
    for child in sorted(SUB_SKILLS.iterdir()):
        handler = child / "scripts" / "handler.py"
        if not handler.is_file():
            continue
        route = handler_route(handler) or ""
        doc = doc_map.get(route)
        if doc is None and route:
            for candidate, meta in doc_map.items():
                if candidate.startswith(route + "/") or route.startswith(candidate + "/"):
                    doc = meta
                    break
        doc = doc or {}
        skill_md = child / "SKILL.md"
        rows.append(
            {
                "skill": child.name,
                "route": route,
                "doc_title": doc.get("title", ""),
                "doc_url": doc.get("url", ""),
                "doc_md": doc.get("md", ""),
                "tier": doc.get("tier", ""),
                "category": doc.get("category", ""),
                "description": frontmatter(skill_md).get("description", "") if skill_md.is_file() else "",
            }
        )
    return rows


def _one_line(text: str, limit: int = 70) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_index(rows: list[dict]) -> str:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row["category"] or "未分类", []).append(row)
    keys = [k for k in CATEGORY_ORDER if k in groups] + sorted(k for k in groups if k not in CATEGORY_ORDER)

    out = [
        "# 子技能索引",
        "",
        "> 本文件由 `tools/index_skills.py --write` 生成，请勿手改。",
        f"> 共 {len(rows)} 个子技能；「在线文档」为可直接抓取的 markdown 链接。",
        "> 按需读取本文件做路由，日常对话不必加载；文件较大，建议按分组或关键词检索，",
        "> 精简清单用 `python run.py --index`（名称 + 触发场景）。",
        "",
    ]
    for key in keys:
        items = groups[key]
        out += [f"## {key}（{len(items)}）", "",
                "| 子技能 | 接口 | 路由 | 触发场景 | 套餐 | 在线文档 |",
                "|---|---|---|---|---|---|"]
        for row in sorted(items, key=lambda r: r["skill"]):
            doc_cell = f"[{row['doc_title']}]({row['doc_md']})" if row["doc_md"] else (
                row["doc_title"] or "—"
            )
            out.append(
                "| `{}` | {} | `{}` | {} | {} | {} |".format(
                    row["skill"],
                    row["doc_title"] or "—",
                    row["route"] or "—",
                    _one_line(row["description"]).replace("|", "\\|"),
                    row["tier"] or "—",
                    doc_cell,
                )
            )
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_manifest(rows: list[dict]) -> str:
    cols = ("skill", "route", "doc_title", "doc_url", "tier", "category", "description")
    lines = ["\t".join(cols)]
    for row in sorted(rows, key=lambda r: r["skill"]):
        lines.append("\t".join(row[c].replace("\t", " ").replace("\n", " ") for c in cols))
    return "\n".join(lines) + "\n"


def render_readme_table(rows: list[dict]) -> str:
    groups: dict[str, list[str]] = {}
    for row in rows:
        groups.setdefault(row["category"] or "未分类", []).append(row["skill"])
    keys = [k for k in CATEGORY_ORDER if k in groups] + sorted(k for k in groups if k not in CATEGORY_ORDER)
    lines = [README_BEGIN, "| 域 | 子技能数 | 代表子 skill |", "|---|---|---|"]
    for key in keys:
        names = sorted(groups[key])
        sample = names[:8]
        cell = "、".join(f"`{n}`" for n in sample)
        if len(names) > len(sample):
            cell += f" 等 {len(names)} 个"
        lines.append(f"| **{key}** | {len(names)} | {cell} |")
    lines.append(README_END)
    return "\n".join(lines)


def apply_readme_table(rows: list[dict], current: str) -> str:
    table = render_readme_table(rows)
    if README_BEGIN in current and README_END in current:
        start = current.index(README_BEGIN)
        end = current.index(README_END) + len(README_END)
        return current[:start] + table + current[end:]
    return current


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 / 校验子技能索引")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="重新生成索引文件与 README 表格")
    group.add_argument("--check", action="store_true", help="校验索引是否与仓库一致")
    args = parser.parse_args()

    rows = build_rows()
    payload = {
        "skills": [
            {k: r[k] for k in ("skill", "route", "doc_title", "doc_url", "doc_md", "tier", "category", "description")}
            for r in sorted(rows, key=lambda r: r["skill"])
        ]
    }
    readme_now = README.read_text(encoding="utf-8") if README.is_file() else ""
    files = {
        INDEX_MD: render_index(rows),
        INDEX_JSON: json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        MANIFEST: render_manifest(rows),
        README: apply_readme_table(rows, readme_now),
    }

    if args.write:
        for path, content in files.items():
            path.write_text(content, encoding="utf-8")
        missing = [r["skill"] for r in rows if not r["doc_title"]]
        print(f"写入 {len(files)} 个文件，{len(rows)} 个子技能；无文档映射：{missing or '无'}")
        return 0

    stale = [str(p.relative_to(ROOT)) for p, content in files.items()
             if not p.is_file() or p.read_text(encoding="utf-8") != content]
    if stale:
        print("索引已过期，请运行 python3 tools/index_skills.py --write", file=sys.stderr)
        for item in stale:
            print(f"  - {item}", file=sys.stderr)
        return 1

    errors = []
    seen: dict[str, str] = {}
    for row in rows:
        if not row["route"]:
            errors.append(f"{row['skill']}: 未解析到公开路由")
        elif row["route"] in seen:
            errors.append(f"{row['skill']}: 路由与 {seen[row['route']]} 重复（{row['route']}）")
        else:
            seen[row["route"]] = row["skill"]
        if not row["doc_title"]:
            errors.append(f"{row['skill']}: doc-map.tsv 中缺少对应文档")
    for item in errors:
        print(f"ERROR {item}", file=sys.stderr)
    if errors:
        return 1
    print(f"索引一致：{len(rows)} 个子技能，文档映射齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())