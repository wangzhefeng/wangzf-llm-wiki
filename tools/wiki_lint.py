#!/usr/bin/env python3
"""
wiki_lint.py — LLM-Wiki wikilink 有效性 lint 工具

用法：
  python tools/wiki_lint.py                  # 扫描并打印报告到终端
  python tools/wiki_lint.py --report         # 同上，并写入 outputs/logs/wiki-lint-report.md
  python tools/wiki_lint.py --fix            # 将占位符 wikilink 改为纯文本（就地修改）
  python tools/wiki_lint.py --report --fix   # 同时生成报告并修复占位符

分类逻辑：
  VALID  — 目标文件存在（不报告）
  A1     — 文件存在但名称有差异（如空格 vs 连字符），建议修正链接名
  A2     — 占位符模板链接（如 [[某个概念页]]），--fix 时改为纯文本
  A3     — 历史文档清单类链接（以"历史文档清单"/"文档清单"结尾），不存在则删除
  A4     — 包含路径分隔符 / 但目标不存在，可能是旧路径
  B      — 合理概念名但文件尚未创建，内容缺口，不修复
  C      — raw/ 或 outputs/ 前缀路径，跨层路径，不修复

跳过：
  - wiki/log.md（历史记录文件，包含大量历史链接名）
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import date

# ─── 路径配置 ───────────────────────────────────────────────────────────────
REPO_ROOT  = Path(__file__).parent.parent
WIKI_ROOT  = REPO_ROOT / "wiki"
OUTPUT_DIR = REPO_ROOT / "outputs" / "logs"
REPORT_PATH = OUTPUT_DIR / "wiki-lint-report.md"
SKIP_FILES = {WIKI_ROOT / "log.md"}

# ─── 占位符模式（精确，不过于宽泛）────────────────────────────────────────────
# 只匹配明确是模板占位符的写法，不能用 .*总索引$ 等宽泛模式
PLACEHOLDER_PATTERNS = [
    r"^某",           # 以"某"开头：某总索引、某个概念页、某篇结果页...
    r"^xxx",          # 英文通用占位
    r"^TODO$",
    r"^TBD$",
    r"^概念页名$",     # 精确模板占位
    r"^相关概念名$",
    r"^主题名$",
    r"^文件名$",
    r"^标题$",
    r"^结果页$",       # 精确匹配
    r"^\[.*\]$",      # 模板变量 [xxx]
]

# 历史文档清单模式
HISTORY_DOC_PATTERNS = [
    r".*历史文档清单$",
    r".*文档清单$",
]


# ─── 文件收集 ────────────────────────────────────────────────────────────────

def collect_all_md_files():
    """收集 wiki/ 下所有 .md 文件，返回 (all_files, stem_map)"""
    all_files = []
    stem_map = defaultdict(list)

    for path in WIKI_ROOT.rglob("*.md"):
        if path in SKIP_FILES:
            continue
        all_files.append(path)
        # 建立多种 key 便于模糊匹配
        stem = path.stem
        for key in [stem, stem.lower(),
                    stem.replace("-", " "), stem.replace(" ", "-"),
                    stem.replace("-", " ").lower(), stem.replace(" ", "-").lower()]:
            stem_map[key].append(path)

    return all_files, stem_map


# ─── wikilink 提取 ───────────────────────────────────────────────────────────

def extract_wikilinks(content):
    """提取所有 [[wikilink]]，返回 [(原始文本, 处理后目标)]"""
    raw_links = re.findall(r'\[\[([^\[\]]+)\]\]', content)
    result = []
    for r in raw_links:
        # 去掉别名 [[target|alias]] 或 [[target\|alias]] -> target
        target = re.split(r'[\\]?\|', r)[0].strip()
        # 去掉锚点 [[target#section]] -> target
        target = target.split("#")[0].strip()
        if target:
            result.append((r, target))
    return result


# ─── 分类逻辑 ────────────────────────────────────────────────────────────────

def is_placeholder(target):
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, target):
            return True
    return False


def is_history_doc(target):
    for pat in HISTORY_DOC_PATTERNS:
        if re.search(pat, target):
            return True
    return False


def find_matching_file(target, stem_map):
    """在 stem_map 中查找匹配文件"""
    for key in [target, target.lower(),
                target.replace(" ", "-"), target.replace("-", " "),
                target.replace(" ", "-").lower(), target.replace("-", " ").lower()]:
        if key in stem_map:
            return stem_map[key]
    return None


def classify_link(target, raw_text, stem_map):
    """
    返回 (class_key, note)
    class_key: VALID / A1 / A2 / A3 / A4 / B / C
    """
    # C 类：跨层路径
    if target.startswith("raw/") or target.startswith("outputs/"):
        return "C", "跨层路径（raw/ 或 outputs/），不修复"

    # 合法的 repo 内路径式 wikilink
    path_prefixes = (
        "wiki/",
        "sources/",
        "indexes/",
        "concepts/",
        "entities/",
        "comparisons/",
        "queries/",
    )
    if "/" in target and target.startswith(path_prefixes):
        rel = target if target.startswith("wiki/") else f"wiki/{target}"
        candidate = REPO_ROOT / Path(rel if rel.endswith(".md") else f"{rel}.md")
        if candidate.exists():
            return "VALID", ""

    # A2：占位符
    if is_placeholder(target):
        return "A2", f"占位符模板链接，--fix 时改为纯文本"

    # A3：历史文档清单
    if is_history_doc(target):
        matched = find_matching_file(target, stem_map)
        if not matched:
            return "A3", "历史文档清单不存在，建议删除引用行或改为纯文本"
        return "VALID", ""

    # 尝试文件匹配
    matched = find_matching_file(target, stem_map)

    if matched:
        actual_stems = [p.stem for p in matched]
        if target in actual_stems:
            return "VALID", ""
        else:
            best = matched[0].stem
            return "A1", f"文件存在但名称不匹配，建议改为: [[{best}]]"
    else:
        # 文件不存在
        if "/" in target:
            return "A4", "包含路径分隔符但目标不存在，可能是旧路径引用"
        # B：合理概念名，内容缺口
        return "B", "尚未创建的概念页，内容缺口，不修复"


# ─── 扫描主逻辑 ──────────────────────────────────────────────────────────────

def scan(all_files, stem_map):
    """扫描所有文件，返回分类结果 dict"""
    results = {"A1": [], "A2": [], "A3": [], "A4": [], "B": [], "C": []}
    seen = set()

    for md_file in sorted(all_files):
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[WARNING] 无法读取 {md_file}: {e}", file=sys.stderr)
            continue

        for raw_text, target in extract_wikilinks(content):
            key = (str(md_file), raw_text)
            if key in seen:
                continue
            seen.add(key)

            cls, note = classify_link(target, raw_text, stem_map)
            if cls == "VALID":
                continue

            entry = {
                "source":   str(md_file.relative_to(REPO_ROOT)),
                "wikilink": f"[[{raw_text}]]",
                "target":   target,
                "note":     note,
                "_file":    md_file,   # 内部用，不输出
            }
            results[cls].append(entry)

    return results


# ─── 修复（--fix）────────────────────────────────────────────────────────────

def fix_placeholders(results):
    """将 A2 占位符链接改为纯文本（就地修改文件）"""
    # 按文件聚合 A2 条目
    by_file = defaultdict(list)
    for entry in results["A2"]:
        by_file[entry["_file"]].append(entry)

    fixed_files = 0
    fixed_links = 0

    for md_file, entries in by_file.items():
        try:
            content = md_file.read_text(encoding="utf-8")
            original = content
            for entry in entries:
                wikilink = entry["wikilink"]          # [[xxx]] 或 [[xxx|alias]]
                # 提取显示文本：有别名用别名，否则用链接目标
                inner = wikilink[2:-2]               # 去掉 [[ ]]
                alias_match = re.search(r'[\\]?\|(.+)$', inner)
                display = alias_match.group(1).strip() if alias_match else entry["target"]
                # 替换 wikilink -> 纯文本
                content = content.replace(wikilink, display)
            if content != original:
                md_file.write_text(content, encoding="utf-8")
                fixed_files += 1
                fixed_links += len(entries)
                print(f"  [FIX] {md_file.relative_to(REPO_ROOT)}  ({len(entries)} 处)")
        except Exception as e:
            print(f"  [ERROR] 无法修复 {md_file}: {e}", file=sys.stderr)

    print(f"\n修复完成：{fixed_files} 个文件，{fixed_links} 处占位符改为纯文本")
    return fixed_files, fixed_links


# ─── 报告生成（--report）────────────────────────────────────────────────────

def build_report(results, all_files):
    today = date.today().isoformat()
    total_a = sum(len(results[k]) for k in ["A1","A2","A3","A4"])
    b_targets = {e["target"] for e in results["B"]}

    lines = [
        "---",
        f"created_at: {today}",
        "topics:",
        "  - 知识库维护",
        "  - 健康检查",
        "status: linked",
        "---",
        "",
        "# wiki-lint 断链扫描报告",
        "",
        f"> 生成时间：{today}  ",
        f"> 扫描文件数：{len(all_files)}  ",
        f"> 真实断链（A 类）：{total_a} 条  ",
        f"> 内容缺口（B 类）：{len(results['B'])} 条（涉及 {len(b_targets)} 个概念）  ",
        "",
        "---",
        "",
    ]

    for cls, title, desc in [
        ("A1", "A1：文件名不匹配", "文件存在但 wikilink 名称与实际 stem 有差异，建议修正链接名"),
        ("A2", "A2：占位符模板链接", "明确是模板占位符，运行 `--fix` 可自动改为纯文本"),
        ("A3", "A3：历史文档清单", '以"历史文档清单"/"文档清单"结尾的链接，文件不存在'),
        ("A4", "A4：旧路径引用", "包含 / 分隔符但目标不存在，可能是已删除/重命名的旧路径"),
    ]:
        lines += [f"## {title}", "", f"> {desc}", ""]
        if results[cls]:
            lines += ["| 源文件 | 链接 | 建议 |", "|--------|------|------|"]
            for e in results[cls]:
                src = e["source"]
                lnk = e["wikilink"].replace("|", "\\|")
                note = e["note"].replace("|", "\\|")
                lines.append(f"| {src} | {lnk} | {note} |")
        else:
            lines.append("_无_")
        lines += ["", f"**小计：{len(results[cls])} 条**", "", "---", ""]

    # B 类聚合展示
    lines += [
        "## B：内容缺口（尚未创建的概念页）",
        "",
        "> 合理的概念名但文件不存在，属于待建内容，不修复。",
        "",
    ]
    if results["B"]:
        b_by_target = defaultdict(list)
        for e in results["B"]:
            b_by_target[e["target"]].append(e["source"])
        lines += ["| 概念名 | 引用处数 |", "|--------|---------|"]
        for target, sources in sorted(b_by_target.items()):
            lines.append(f"| [[{target}]] | {len(sources)} |")
    else:
        lines.append("_无_")
    lines += ["", f"**小计：{len(results['B'])} 条**", "", "---", ""]

    # C 类
    lines += [
        "## C：跨层路径（不修复）",
        "",
        "> raw/ 或 outputs/ 前缀的路径，属于跨层引用，不处理。",
        "",
        f"**小计：{len(results['C'])} 条**",
        "",
        "---",
        "",
        "## 汇总",
        "",
        "| 类别 | 数量 |",
        "|------|------|",
        f"| A1（文件名不匹配） | {len(results['A1'])} |",
        f"| A2（占位符） | {len(results['A2'])} |",
        f"| A3（历史文档清单） | {len(results['A3'])} |",
        f"| A4（旧路径引用） | {len(results['A4'])} |",
        f"| **A 合计（真实断链）** | **{total_a}** |",
        f"| B（内容缺口） | {len(results['B'])} |",
        f"| C（跨层路径） | {len(results['C'])} |",
        "",
        "> 目标：A 合计为 0。B 类和 C 类不需要修复。",
    ]

    return "\n".join(lines)


# ─── 终端输出 ────────────────────────────────────────────────────────────────

def print_results(results, all_files):
    total_a = sum(len(results[k]) for k in ["A1","A2","A3","A4"])
    b_targets = {e["target"] for e in results["B"]}

    print(f"\n扫描文件数：{len(all_files)}")
    print(f"真实断链（A 类）：{total_a} 条")
    print(f"内容缺口（B 类）：{len(results['B'])} 条（涉及 {len(b_targets)} 个概念）")

    for cls, title in [("A1","A1 文件名不匹配"), ("A2","A2 占位符"), ("A3","A3 历史文档清单"), ("A4","A4 旧路径引用")]:
        if not results[cls]:
            print(f"\n  [{cls}] {title}: 0 条 ✅")
            continue
        print(f"\n  [{cls}] {title}: {len(results[cls])} 条")
        for e in results[cls]:
            print(f"    {e['source']}")
            print(f"      {e['wikilink']}  →  {e['note']}")

    print(f"\n  [B]  内容缺口: {len(results['B'])} 条")
    print(f"  [C]  跨层路径: {len(results['C'])} 条（不修复）")


# ─── 入口 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LLM-Wiki wikilink lint 工具")
    parser.add_argument("--report", action="store_true", help="写入 outputs/logs/wiki-lint-report.md")
    parser.add_argument("--fix",    action="store_true", help="将 A2 占位符改为纯文本（就地修改）")
    args = parser.parse_args()

    print("=" * 60)
    print("wiki_lint.py — wikilink 有效性扫描")
    print("=" * 60)

    all_files, stem_map = collect_all_md_files()
    results = scan(all_files, stem_map)

    print_results(results, all_files)

    if args.report:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report = build_report(results, all_files)
        REPORT_PATH.write_text(report, encoding="utf-8")
        print(f"\n报告已写入：{REPORT_PATH.relative_to(REPO_ROOT)}")

    if args.fix:
        print("\n" + "=" * 60)
        print("--fix 模式：修复 A2 占位符链接")
        print("=" * 60)
        fix_placeholders(results)

    # 退出码：A 类断链 > 0 时返回非零
    total_a = sum(len(results[k]) for k in ["A1","A2","A3","A4"])
    sys.exit(0 if total_a == 0 else 1)


if __name__ == "__main__":
    main()
