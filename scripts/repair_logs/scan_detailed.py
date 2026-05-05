#!/usr/bin/env python3
"""
详细扫描并结构化输出 A1/A2/A3/A4 断链，用于修复脚本消费。
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

WIKI_ROOT = Path("/Users/wangzf/wangzf-llm-wiki/wiki")
SKIP_FILES = {WIKI_ROOT / "log.md"}

PLACEHOLDER_PATTERNS = [
    r"^某",
    r"^概念页名$",
    r"^相关概念名$",
    r"^主题名$",
    r"^文件名$",
    r"^标题$",
    r"^xxx",
    r"^TODO",
    r"^TBD",
    r".*结果页$",
    r".*总索引$",
    r".*概念页$",
    r".*索引页$",
    r".*入口页$",
]

HISTORY_DOC_PATTERNS = [
    r".*历史文档清单$",
    r".*文档清单$",
]


def collect_all_md_files():
    all_files = []
    stem_map = defaultdict(list)
    for path in WIKI_ROOT.rglob("*.md"):
        if path in SKIP_FILES:
            continue
        all_files.append(path)
        stem = path.stem
        for key in [stem, stem.lower(), stem.replace("-"," "), stem.replace(" ","-"),
                    stem.replace("-"," ").lower(), stem.replace(" ","-").lower()]:
            if path not in stem_map[key]:
                stem_map[key].append(path)
    return all_files, stem_map


def extract_wikilinks_with_lines(content):
    results = []
    for lineno, line in enumerate(content.splitlines(), 1):
        for m in re.finditer(r'\[\[([^\[\]]+)\]\]', line):
            raw = m.group(1)
            target = raw.split("|")[0].strip().split("#")[0].strip()
            if target:
                results.append((lineno, line.rstrip(), raw, target))
    return results


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
    for key in [target, target.lower(),
                target.replace(" ","-"), target.replace("-"," "),
                target.replace(" ","-").lower(), target.replace("-"," ").lower()]:
        if key in stem_map:
            return stem_map[key]
    return None


def classify_link(target, stem_map):
    if target.startswith("raw/") or target.startswith("outputs/"):
        return "C", None, "范围外路径"
    if is_placeholder(target):
        return "A", "A2", f"占位符"
    if is_history_doc(target):
        return "A", "A3", f"历史文档清单"
    matched = find_matching_file(target, stem_map)
    if matched:
        actual_stems = [p.stem for p in matched]
        if target not in actual_stems:
            best = matched[0].stem
            return "A", "A1", best
        return "VALID", None, ""
    if "/" in target or "\\" in target:
        return "A", "A4", "包含路径分隔符但目标不存在"
    return "B", None, "尚未创建的概念页"


def main():
    all_files, stem_map = collect_all_md_files()

    results = {"A1": [], "A2": [], "A3": [], "A4": [], "B": [], "C": []}
    seen = set()

    for md_file in sorted(all_files):
        try:
            content = md_file.read_text(encoding="utf-8")
        except:
            continue
        links = extract_wikilinks_with_lines(content)
        for lineno, line_text, raw, target in links:
            key = (str(md_file), raw)
            if key in seen:
                continue
            seen.add(key)
            cls, sub, note = classify_link(target, stem_map)
            if cls == "VALID":
                continue
            entry = {
                "file": str(md_file),
                "rel": str(md_file.relative_to(WIKI_ROOT.parent)),
                "lineno": lineno,
                "line": line_text,
                "raw": raw,
                "target": target,
                "wikilink": f"[[{raw}]]",
                "note": note,
            }
            if cls == "A":
                results[sub].append(entry)
            else:
                results[cls].append(entry)

    # 打印 A1
    print("\n=== A1 类：文件名不匹配（文件存在，名称有差异）===")
    for e in results["A1"]:
        print(f"  {e['rel']}:{e['lineno']}")
        print(f"    原链接: {e['wikilink']}")
        print(f"    建议:   [[{e['note']}]]")

    # 打印 A2（按文件分组）
    print("\n=== A2 类：占位符模板链接 ===")
    a2_by_file = defaultdict(list)
    for e in results["A2"]:
        a2_by_file[e["rel"]].append(e)
    for f, items in sorted(a2_by_file.items()):
        print(f"  {f}:")
        for e in items:
            print(f"    行{e['lineno']}: {e['wikilink']}")

    # 打印 A3
    print("\n=== A3 类：历史文档清单不存在 ===")
    for e in results["A3"]:
        print(f"  {e['rel']}:{e['lineno']}: {e['wikilink']}")

    # 打印 A4（仅含路径分隔符，即旧路径引用）
    print("\n=== A4 类：旧名/已删除引用（含路径分隔符，需人工判断）===")
    a4_by_file = defaultdict(list)
    for e in results["A4"]:
        a4_by_file[e["rel"]].append(e)
    for f, items in sorted(a4_by_file.items()):
        print(f"  {f}:")
        for e in items:
            print(f"    行{e['lineno']}: {e['wikilink']}")

    print(f"\n汇总: A1={len(results['A1'])} A2={len(results['A2'])} A3={len(results['A3'])} A4={len(results['A4'])} B={len(results['B'])} C={len(results['C'])}")

    # 保存 JSON 供修复脚本使用
    out = Path("/Users/wangzf/wangzf-llm-wiki/scripts/broken_links.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n已保存详细数据到: {out}")


if __name__ == "__main__":
    main()
