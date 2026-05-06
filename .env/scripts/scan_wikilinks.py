#!/usr/bin/env python3
"""
扫描 wiki/ 下所有 .md 文件中的 [[wikilink]] 断链，按 A/B/C 类分类。
跳过 wiki/log.md。
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

WIKI_ROOT = Path("/Users/wangzf/wangzf-llm-wiki/wiki")
SKIP_FILES = {WIKI_ROOT / "log.md"}

# 占位符模式（只匹配明确是模板占位符的写法，不能过于宽泛）
# 原则：精确匹配已知占位符，不用 .*总索引$ 等宽泛模式（会误匹配真实页面名）
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
    r"^结果页$",       # 精确匹配（不是 .*结果页$）
    r"^\[.*\]$",      # 模板变量 [xxx]、[概念名]
]

# 历史文档清单模式
HISTORY_DOC_PATTERNS = [
    r".*历史文档清单$",
    r".*文档清单$",
]


def collect_all_md_files():
    """收集 wiki/ 下所有 .md 文件，返回 {stem_lower: [Path, ...]} 和完整路径集合"""
    all_files = []
    stem_map = defaultdict(list)  # stem (不含扩展名) -> [Path]

    for path in WIKI_ROOT.rglob("*.md"):
        if path in SKIP_FILES:
            continue
        all_files.append(path)
        # 建立多种 key 便于模糊匹配
        stem = path.stem
        stem_map[stem].append(path)
        stem_map[stem.lower()].append(path)
        stem_map[stem.replace("-", " ")].append(path)
        stem_map[stem.replace(" ", "-")].append(path)
        stem_map[stem.replace("-", " ").lower()].append(path)
        stem_map[stem.replace(" ", "-").lower()].append(path)

    return all_files, stem_map


def extract_wikilinks(content):
    """提取所有 [[wikilink]] 和 [[wikilink|alias]]，返回链接目标列表（去掉锚点和别名）"""
    raw = re.findall(r'\[\[([^\[\]]+)\]\]', content)
    targets = []
    for r in raw:
        # 去掉别名 [[target|alias]] -> target
        target = r.split("|")[0].strip()
        # 去掉锚点 [[target#section]] -> target
        target = target.split("#")[0].strip()
        if target:
            targets.append((r, target))  # (原始文本, 处理后目标)
    return targets


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
    """尝试在 stem_map 中找到匹配的文件"""
    # 精确匹配
    if target in stem_map:
        return stem_map[target]
    # 大小写不敏感
    if target.lower() in stem_map:
        return stem_map[target.lower()]
    # 空格 <-> 连字符
    alt1 = target.replace(" ", "-")
    alt2 = target.replace("-", " ")
    if alt1 in stem_map:
        return stem_map[alt1]
    if alt2 in stem_map:
        return stem_map[alt2]
    if alt1.lower() in stem_map:
        return stem_map[alt1.lower()]
    if alt2.lower() in stem_map:
        return stem_map[alt2.lower()]
    return None


def classify_link(target, raw_text, stem_map, source_file):
    """
    返回 (class, subclass, note)
    class: A / B / C
    subclass: A1/A2/A3/A4 or None
    note: 建议修复方式
    """
    # C 类：路径前缀
    if target.startswith("raw/") or target.startswith("outputs/"):
        return "C", None, "范围外路径，不修复"

    # A2：占位符
    if is_placeholder(target):
        return "A", "A2", f"占位符，改为纯文本: {target}"

    # A3：历史文档清单
    if is_history_doc(target):
        return "A", "A3", f"历史文档清单不存在，删除引用行或改为纯文本"

    # 尝试找匹配文件（精确 stem 匹配）
    matched = find_matching_file(target, stem_map)

    if matched:
        # A1：文件存在但名称不一致（如空格 vs 连字符）
        actual_stems = [p.stem for p in matched]
        if target not in actual_stems:
            # 名称不一致，A1
            best_match = matched[0].stem
            return "A", "A1", f"文件存在但名称不匹配，建议改为: [[{best_match}]]"
        else:
            # 名称完全匹配，链接有效（不应出现在断链列表）
            return "VALID", None, ""
    else:
        # 文件不存在
        # 判断是否为 B 类（合理概念名）
        # B 类特征：中文概念名、英文学术术语，且不是占位符/历史清单
        # A4：其他明确旧名引用（已知被删/重命名的文件名模式）
        # 这里做一个粗略判断：如果链接名看起来像合理的概念/术语，归 B 类
        # 如果包含特殊模式（如路径分隔符、已知被删前缀），归 A4

        # A4 检测：包含路径分隔符（不是 raw/ outputs/）
        if "/" in target or "\\" in target:
            return "A", "A4", f"包含路径分隔符但目标不存在，可能是旧路径引用"

        # B 类：合理的概念名（中文/英文术语）
        return "B", None, "尚未创建的概念页，内容缺口，不修复"


def main():
    print("=" * 70)
    print("扫描 wiki/ 下所有 [[wikilink]] 断链")
    print("=" * 70)

    all_files, stem_map = collect_all_md_files()
    print(f"\n共扫描 {len(all_files)} 个 .md 文件\n")

    # 结果收集
    results = {
        "A1": [],  # 文件名不匹配
        "A2": [],  # 占位符
        "A3": [],  # 历史文档清单
        "A4": [],  # 旧名/已删除引用
        "B":  [],  # 内容缺口
        "C":  [],  # 范围外路径
    }

    # 记录已见过的断链（去重用于 B 类统计）
    seen_broken = set()

    for md_file in sorted(all_files):
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[WARNING] 无法读取 {md_file}: {e}")
            continue

        links = extract_wikilinks(content)

        for raw_text, target in links:
            cls, sub, note = classify_link(target, raw_text, stem_map, md_file)

            if cls == "VALID":
                continue

            entry = {
                "source": str(md_file.relative_to(WIKI_ROOT.parent)),
                "wikilink": f"[[{raw_text}]]",
                "target": target,
                "note": note,
            }

            key = (str(md_file), raw_text)
            if key in seen_broken:
                continue
            seen_broken.add(key)

            if cls == "A":
                results[sub].append(entry)
            elif cls == "B":
                results["B"].append(entry)
            elif cls == "C":
                results["C"].append(entry)

    # 输出报告
    print("\n" + "=" * 70)
    print("A1 类：文件名不匹配（文件存在，名称有差异）")
    print("=" * 70)
    for e in results["A1"]:
        print(f"  源文件: {e['source']}")
        print(f"  链接:   {e['wikilink']}")
        print(f"  修复:   {e['note']}")
        print()
    print(f"  A1 小计: {len(results['A1'])} 条")

    print("\n" + "=" * 70)
    print("A2 类：占位符模板链接")
    print("=" * 70)
    for e in results["A2"]:
        print(f"  源文件: {e['source']}")
        print(f"  链接:   {e['wikilink']}")
        print(f"  修复:   {e['note']}")
        print()
    print(f"  A2 小计: {len(results['A2'])} 条")

    print("\n" + "=" * 70)
    print("A3 类：历史文档清单不存在")
    print("=" * 70)
    for e in results["A3"]:
        print(f"  源文件: {e['source']}")
        print(f"  链接:   {e['wikilink']}")
        print(f"  修复:   {e['note']}")
        print()
    print(f"  A3 小计: {len(results['A3'])} 条")

    print("\n" + "=" * 70)
    print("A4 类：旧名/已删除引用（需人工判断）")
    print("=" * 70)
    for e in results["A4"]:
        print(f"  源文件: {e['source']}")
        print(f"  链接:   {e['wikilink']}")
        print(f"  修复:   {e['note']}")
        print()
    print(f"  A4 小计: {len(results['A4'])} 条")

    print("\n" + "=" * 70)
    print("B 类：尚未创建的概念页（内容缺口，不修复）")
    print("=" * 70)
    # B 类按主题聚合，避免过长
    b_targets = defaultdict(list)
    for e in results["B"]:
        b_targets[e["target"]].append(e["source"])
    for target, sources in sorted(b_targets.items()):
        print(f"  [[{target}]]  (引用于 {len(sources)} 处)")
        for s in sources[:3]:  # 最多显示3处引用
            print(f"    <- {s}")
        if len(sources) > 3:
            print(f"    ... 还有 {len(sources)-3} 处")
    print(f"\n  B 小计: {len(results['B'])} 条 (涉及 {len(b_targets)} 个不同概念)")

    print("\n" + "=" * 70)
    print("C 类：范围外路径（raw/ 或 outputs/，不修复）")
    print("=" * 70)
    for e in results["C"]:
        print(f"  源文件: {e['source']}")
        print(f"  链接:   {e['wikilink']}")
        print()
    print(f"  C 小计: {len(results['C'])} 条")

    print("\n" + "=" * 70)
    print("汇总")
    print("=" * 70)
    total_a = sum(len(results[k]) for k in ["A1","A2","A3","A4"])
    print(f"  A1（文件名不匹配）: {len(results['A1'])} 条")
    print(f"  A2（占位符）:       {len(results['A2'])} 条")
    print(f"  A3（历史文档清单）: {len(results['A3'])} 条")
    print(f"  A4（旧名引用）:     {len(results['A4'])} 条")
    print(f"  A 合计:             {total_a} 条")
    print(f"  B（内容缺口）:      {len(results['B'])} 条")
    print(f"  C（范围外路径）:    {len(results['C'])} 条")

    # 返回结果供修复脚本使用
    return results


if __name__ == "__main__":
    main()
