#!/usr/bin/env python3
"""
基于自动映射表的批量清理脚本

根据 outputs/answers/2026-04-12-autofix-自动映射表.md，
自动更新引用并删除 autofix 占位页。

使用方法：
1. 先运行 dry run（默认）：python cleanup_autofix_batch.py
2. 确认无误后：python cleanup_autofix_batch.py --execute

注意：请确保已备份，脚本会修改文件并删除文件。
"""

import os
import re
import sys
import glob
import json
import argparse
from pathlib import Path


def parse_auto_mapping_table(mapping_file):
    """解析自动生成的映射表，返回旧目标->新目标的字典"""
    mappings = {}

    with open(mapping_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 找到表格开始的行
    in_table = False
    for line in lines:
        line = line.strip()
        # 表格开始标记
        if line.startswith("| Autofix 文件名 |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            continue
        if line.startswith("|---"):
            continue

        # 解析表格行
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 6:
            continue

        autofix_name = parts[1].strip("` ")
        wiki_link = parts[3].strip("` ")

        if not autofix_name or not wiki_link:
            continue

        mappings[autofix_name] = {
            "wiki_link": wiki_link,
            "confidence": float(parts[5]) if parts[5].strip() else 1.0,
            "match_type": parts[4].strip(),
        }

    return mappings


def find_autofix_files(autofix_dir):
    """查找 autofix 目录下的所有 md 文件"""
    autofix_files = {}
    for md_file in glob.glob(os.path.join(autofix_dir, "*.md")):
        if md_file.endswith("index.md"):
            continue
        filename = os.path.basename(md_file)
        name_without_ext = filename[:-3]  # 去掉 .md
        autofix_files[name_without_ext] = md_file
    return autofix_files


def find_references(root_dir, target):
    """在 wiki 目录中查找所有引用 target 的文件"""
    references = []

    # Wiki 链接可能的形式：
    # 1. [[target]]
    # 2. [[target|alias]]
    # 3. [[path/to/target]]
    wiki_link_pattern1 = re.compile(r"\[\[\s*" + re.escape(target) + r"\s*(?:\||\]\])")
    wiki_link_pattern2 = re.compile(
        r"\[\[\s*(?:[^|\]]*/\s*)?" + re.escape(target) + r"\s*(?:\||\]\])"
    )

    # 搜索所有 .md 文件
    for md_file in glob.glob(os.path.join(root_dir, "**/*.md"), recursive=True):
        # 跳过 autofix 目录本身
        if "wiki/sources/autofix" in md_file:
            continue

        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                if wiki_link_pattern1.search(content) or wiki_link_pattern2.search(
                    content
                ):
                    references.append(md_file)
        except (UnicodeDecodeError, IOError) as e:
            print(f"警告：无法读取文件 {md_file}: {e}")

    return references


def update_references(file_path, old_target, new_wiki_link):
    """更新文件中的 Wiki 链接引用"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    old_content = content

    # 模式1: [[old_target]]
    pattern1 = r"\[\[\s*" + re.escape(old_target) + r"\s*\]\]"
    replacement1 = f"[[{new_wiki_link}]]"
    content = re.sub(pattern1, replacement1, content)

    # 模式2: [[old_target|alias]]
    pattern2 = r"\[\[\s*" + re.escape(old_target) + r"\s*\|\s*([^\]]+)\s*\]\]"
    replacement2 = f"[[{new_wiki_link}|\\1]]"
    content = re.sub(pattern2, replacement2, content)

    # 模式3: 更通用的匹配，处理路径情况
    # [[wiki/sources/autofix/old_target]]
    pattern3 = r"\[\[\s*wiki/sources/autofix/" + re.escape(old_target) + r"\s*\]\]"
    replacement3 = f"[[{new_wiki_link}]]"
    content = re.sub(pattern3, replacement3, content)

    # [[wiki/sources/autofix/old_target|alias]]
    pattern4 = (
        r"\[\[\s*wiki/sources/autofix/"
        + re.escape(old_target)
        + r"\s*\|\s*([^\]]+)\s*\]\]"
    )
    replacement4 = f"[[{new_wiki_link}|\\1]]"
    content = re.sub(pattern4, replacement4, content)

    if old_content != content:
        return content
    return None


def update_autofix_index(index_file, old_target_name):
    """从 autofix/index.md 中移除对应的条目"""
    with open(index_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    pattern1 = re.compile(
        r"\[\[\s*wiki/sources/autofix/" + re.escape(old_target_name) + r"\s*\]\]"
    )
    pattern2 = re.compile(r"\[\[\s*" + re.escape(old_target_name) + r"\s*\]\]")

    for line in lines:
        if not (pattern1.search(line) or pattern2.search(line)):
            new_lines.append(line)

    return "".join(new_lines) if new_lines != lines else None


def main():
    parser = argparse.ArgumentParser(
        description="批量清理 autofix 占位页（基于自动映射）"
    )
    parser.add_argument(
        "--execute", action="store_true", help="执行实际操作（默认只显示计划）"
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.0,
        help="最小置信度阈值（默认处理所有）",
    )
    parser.add_argument(
        "--mapping-file",
        type=str,
        default="outputs/answers/2026-04-12-autofix-自动映射表.md",
        help="映射表文件路径（默认: outputs/answers/2026-04-12-autofix-自动映射表.md）",
    )
    args = parser.parse_args()

    # 获取仓库根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # 上一级目录是仓库根目录
    mapping_file = os.path.join(base_dir, args.mapping_file)
    autofix_dir = os.path.join(base_dir, "wiki/sources/autofix")
    autofix_index = os.path.join(autofix_dir, "index.md")
    wiki_root = os.path.join(base_dir, "wiki")

    print(f"工作目录: {base_dir}")
    print(f"映射文件: {mapping_file}")
    print(f"Autofix 目录: {autofix_dir}")
    print(f"Wiki 根目录: {wiki_root}")
    print(f"执行模式: {'是' if args.execute else '否（dry run）'}")
    print(f"最小置信度: {args.min_confidence}")
    print("=" * 80)

    # 解析映射表
    mappings = parse_auto_mapping_table(mapping_file)
    print(f"解析到 {len(mappings)} 个映射项")

    # 查找 autofix 文件
    autofix_files = find_autofix_files(autofix_dir)
    print(f"找到 {len(autofix_files)} 个 autofix 文件")

    # 统计
    total_updates = 0
    total_deletions = 0
    processed = 0

    # 按置信度排序处理
    sorted_items = sorted(
        mappings.items(), key=lambda x: x[1]["confidence"], reverse=True
    )

    for autofix_name, mapping_info in sorted_items:
        confidence = mapping_info["confidence"]
        wiki_link = mapping_info["wiki_link"]

        # 过滤置信度
        if confidence < args.min_confidence:
            continue

        processed += 1

        print(
            f"\n[{processed}] 处理: {autofix_name} -> {wiki_link} (置信度: {confidence}, 匹配类型: {mapping_info['match_type']})"
        )

        # 检查是否为 autofix 占位页
        is_autofix = autofix_name in autofix_files
        print(f"  Autofix 文件: {'是' if is_autofix else '否'}")

        if not is_autofix:
            print(f"  跳过：不是 autofix 文件")
            continue

        # 查找引用
        references = find_references(wiki_root, autofix_name)
        print(f"  找到 {len(references)} 个引用文件")

        # 如果执行模式
        if args.execute:
            # 1. 更新引用
            updated_files = []
            for ref_file in references:
                new_content = update_references(ref_file, autofix_name, wiki_link)
                if new_content:
                    with open(ref_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    updated_files.append(ref_file)
                    total_updates += 1

            if updated_files:
                print(f"  更新了 {len(updated_files)} 个文件")
                for f in updated_files[:5]:  # 只显示前5个
                    print(f"    - {os.path.relpath(f, base_dir)}")
                if len(updated_files) > 5:
                    print(f"    ... 还有 {len(updated_files) - 5} 个文件")

            # 2. 删除 autofix 文件
            autofix_file_path = autofix_files[autofix_name]
            try:
                os.remove(autofix_file_path)
                print(f"  删除文件: {os.path.relpath(autofix_file_path, base_dir)}")
                total_deletions += 1
            except OSError as e:
                print(f"  错误：无法删除文件: {e}")

            # 3. 更新 index.md
            new_index_content = update_autofix_index(autofix_index, autofix_name)
            if new_index_content:
                with open(autofix_index, "w", encoding="utf-8") as f:
                    f.write(new_index_content)
                print(f"  更新了 index.md")
        else:
            # Dry run 模式
            print(f"  [dry run] 将更新 {len(references)} 个引用文件")
            print(f"  [dry run] 将删除文件: {autofix_files[autofix_name]}")
            print(f"  [dry run] 将更新 index.md")
            total_updates += len(references)
            total_deletions += 1

    print("\n" + "=" * 80)
    print(f"处理完成")
    print(f"总处理项: {processed}")
    print(f"总更新文件数: {total_updates}")
    print(f"总删除文件数: {total_deletions}")

    if not args.execute:
        print("\n注意：以上为 dry run 模式，未实际修改任何文件")
        print("如需执行，请添加 --execute 参数")

    return total_deletions


if __name__ == "__main__":
    main()
