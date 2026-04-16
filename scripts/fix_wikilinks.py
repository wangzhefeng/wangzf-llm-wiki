#!/usr/bin/env python3
"""
修复 A1、A2、A3 类 [[wikilink]] 断链。
A4 仅列出清单，不自动修复。

运行方式：
  python3 fix_wikilinks.py          # dry-run 模式（只打印变更，不写文件）
  python3 fix_wikilinks.py --apply  # 实际写入文件
"""

import re
import sys
import json
from pathlib import Path
from collections import defaultdict

WIKI_ROOT = Path("/Users/wangzf/wangzf-llm-wiki/wiki")
SKIP_FILES = {WIKI_ROOT / "log.md"}
DRY_RUN = "--apply" not in sys.argv

# ─── 占位符模式（A2）───────────────────────────────────────────────────────────
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

# ─── 历史文档清单模式（A3）────────────────────────────────────────────────────
HISTORY_DOC_PATTERNS = [
    r".*历史文档清单$",
    r".*文档清单$",
]


def collect_stem_map():
    """建立 stem -> [Path] 映射，支持多种变体匹配"""
    stem_map = defaultdict(list)
    for path in WIKI_ROOT.rglob("*.md"):
        if path in SKIP_FILES:
            continue
        stem = path.stem
        for key in [stem, stem.lower(),
                    stem.replace("-", " "), stem.replace(" ", "-"),
                    stem.replace("-", " ").lower(), stem.replace(" ", "-").lower()]:
            if path not in stem_map[key]:
                stem_map[key].append(path)
    return stem_map


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


def find_matching_stem(target, stem_map):
    """返回匹配的实际 stem（或 None）"""
    for key in [target, target.lower(),
                target.replace(" ", "-"), target.replace("-", " "),
                target.replace(" ", "-").lower(), target.replace("-", " ").lower()]:
        if key in stem_map:
            actual_stems = [p.stem for p in stem_map[key]]
            # 精确匹配优先
            if target in actual_stems:
                return target
            # 返回第一个匹配结果
            return actual_stems[0]
    return None


def fix_line_a1(line, stem_map):
    """A1：把空格版链接替换为连字符版（文件存在但 stem 不匹配）"""
    changed = False

    def replacer(m):
        nonlocal changed
        inner = m.group(1)
        raw = inner.split("|")[0].strip()
        anchor_part = ""
        alias_part = ""
        if "|" in inner:
            alias_part = "|" + inner.split("|", 1)[1]
        if "#" in raw:
            parts = raw.split("#", 1)
            raw_target = parts[0].strip()
            anchor_part = "#" + parts[1]
        else:
            raw_target = raw

        # 跳过 raw/ outputs/ 开头
        if raw_target.startswith("raw/") or raw_target.startswith("outputs/"):
            return m.group(0)
        # 只处理含空格的（空格->连字符不匹配）
        if " " not in raw_target:
            return m.group(0)

        actual = find_matching_stem(raw_target, stem_map)
        if actual and actual != raw_target:
            changed = True
            return f"[[{actual}{anchor_part}{alias_part}]]"
        return m.group(0)

    new_line = re.sub(r'\[\[([^\[\]]+)\]\]', replacer, line)
    return new_line, changed


def fix_line_a2(line):
    """A2：把占位符 [[xxx]] 改为纯文本"""
    changed = False

    def replacer(m):
        nonlocal changed
        inner = m.group(1)
        raw = inner.split("|")[0].strip().split("#")[0].strip()
        if is_placeholder(raw):
            changed = True
            # 有别名时保留别名文本，否则保留目标文本
            if "|" in inner:
                return inner.split("|", 1)[1]
            return raw
        return m.group(0)

    new_line = re.sub(r'\[\[([^\[\]]+)\]\]', replacer, line)
    return new_line, changed


def fix_line_a3(line):
    """A3：把历史文档清单链接改为纯文本"""
    changed = False

    def replacer(m):
        nonlocal changed
        inner = m.group(1)
        raw = inner.split("|")[0].strip().split("#")[0].strip()
        if is_history_doc(raw):
            changed = True
            return raw  # 改为纯文本
        return m.group(0)

    new_line = re.sub(r'\[\[([^\[\]]+)\]\]', replacer, line)
    return new_line, changed


def process_file(md_file, stem_map, fix_log):
    try:
        original = md_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] 读取失败: {md_file}: {e}")
        return

    lines = original.splitlines(keepends=True)
    new_lines = []
    file_changed = False
    file_changes = []

    for i, line in enumerate(lines, 1):
        new_line = line

        # A1 修复
        new_line, c1 = fix_line_a1(new_line, stem_map)
        if c1:
            file_changes.append(f"  行{i} A1: {line.rstrip()!r} -> {new_line.rstrip()!r}")
            file_changed = True

        # A2 修复
        new_line, c2 = fix_line_a2(new_line)
        if c2:
            file_changes.append(f"  行{i} A2: {new_line.rstrip()!r}")
            file_changed = True

        # A3 修复
        new_line, c3 = fix_line_a3(new_line)
        if c3:
            file_changes.append(f"  行{i} A3: {new_line.rstrip()!r}")
            file_changed = True

        new_lines.append(new_line)

    if file_changed:
        rel = md_file.relative_to(WIKI_ROOT.parent)
        fix_log.append({"file": str(rel), "changes": file_changes})
        print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}修改: {rel}")
        for c in file_changes:
            print(c)

        if not DRY_RUN:
            new_content = "".join(new_lines)
            md_file.write_text(new_content, encoding="utf-8")


def main():
    print("=" * 70)
    mode = "DRY-RUN（预览模式，不写文件）" if DRY_RUN else "APPLY（实际修复）"
    print(f"断链修复脚本  [{mode}]")
    print("=" * 70)

    stem_map = collect_stem_map()
    all_files = sorted([p for p in WIKI_ROOT.rglob("*.md") if p not in SKIP_FILES])

    fix_log = []
    for md_file in all_files:
        process_file(md_file, stem_map, fix_log)

    print("\n" + "=" * 70)
    print(f"修复完成。共修改 {len(fix_log)} 个文件。")
    if DRY_RUN:
        print("使用 --apply 参数实际写入文件。")

    # 统计
    a1_count = sum(1 for f in fix_log for c in f["changes"] if " A1:" in c)
    a2_count = sum(1 for f in fix_log for c in f["changes"] if " A2:" in c)
    a3_count = sum(1 for f in fix_log for c in f["changes"] if " A3:" in c)
    print(f"  A1 修复行数: {a1_count}")
    print(f"  A2 修复行数: {a2_count}")
    print(f"  A3 修复行数: {a3_count}")

    # 保存修复日志
    log_path = Path("/Users/wangzf/wangzf-llm-wiki/scripts/fix_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(fix_log, f, ensure_ascii=False, indent=2)
    print(f"\n修复日志已保存到: {log_path}")


if __name__ == "__main__":
    main()
