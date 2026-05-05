#!/usr/bin/env python3
"""
为 autofix 占位页查找实际文件位置的脚本

分析 wiki/sources/autofix/ 中的文件，在 wiki/sources/ 其他目录中查找同名文件，
建立自动映射关系用于批量清理。

使用方法：
python find_autofix_mappings.py
"""

import os
import re
import glob
import json
from pathlib import Path


def find_autofix_files(autofix_dir):
    """获取所有autofix文件"""
    autofix_files = {}
    for md_file in glob.glob(os.path.join(autofix_dir, "*.md")):
        if md_file.endswith("index.md"):
            continue
        filename = os.path.basename(md_file)
        name_without_ext = filename[:-3]  # 去掉 .md
        autofix_files[name_without_ext] = {"path": md_file, "filename": filename}
    return autofix_files


def find_actual_file(autofix_name, wiki_sources_root):
    """在 wiki/sources/ 目录中查找同名文件"""
    # 排除 autofix 目录本身
    search_patterns = [
        os.path.join(wiki_sources_root, "**", f"{autofix_name}.md"),
        os.path.join(wiki_sources_root, "**", f"*{autofix_name}*.md"),  # 宽松匹配
    ]

    actual_files = []
    for pattern in search_patterns:
        for match in glob.glob(pattern, recursive=True):
            # 排除 autofix 目录
            if "wiki/sources/autofix" in match:
                continue
            actual_files.append(match)

    # 优先选择完全匹配的文件名
    exact_matches = [
        f for f in actual_files if os.path.basename(f) == f"{autofix_name}.md"
    ]
    if exact_matches:
        return exact_matches[0]
    elif actual_files:
        # 返回第一个匹配（可能是部分匹配）
        return actual_files[0]
    return None


def analyze_mappings():
    """分析所有autofix文件并查找映射"""
    base_dir = "/Users/wangzf/wangzf-llm-wiki"
    autofix_dir = os.path.join(base_dir, "wiki/sources/autofix")
    wiki_sources_root = os.path.join(base_dir, "wiki/sources")

    print(f"分析目录: {autofix_dir}")
    print(f"搜索范围: {wiki_sources_root}")

    # 获取所有autofix文件
    autofix_files = find_autofix_files(autofix_dir)
    print(f"找到 {len(autofix_files)} 个 autofix 文件")

    # 分析每个文件
    mappings = {}
    found_count = 0
    not_found = []

    for i, (autofix_name, info) in enumerate(autofix_files.items()):
        if i % 20 == 0:
            print(f"  进度: {i}/{len(autofix_files)}")

        actual_file = find_actual_file(autofix_name, wiki_sources_root)

        if actual_file:
            # 计算相对路径（相对于 wiki 根目录）
            rel_path = os.path.relpath(actual_file, os.path.join(base_dir, "wiki"))
            # 去掉 .md 扩展名，得到 Wiki 链接格式
            wiki_link = rel_path[:-3]  # 去掉 .md

            mappings[autofix_name] = {
                "autofix_path": info["path"],
                "actual_path": actual_file,
                "wiki_link": wiki_link,
                "confidence": 1.0,  # 文件名完全匹配，置信度高
                "match_type": "exact"
                if os.path.basename(actual_file) == f"{autofix_name}.md"
                else "partial",
            }
            found_count += 1
        else:
            not_found.append(autofix_name)

    print(f"\n分析完成:")
    print(f"  找到映射: {found_count}")
    print(f"  未找到: {len(not_found)}")

    # 保存结果
    results = {
        "mappings": mappings,
        "not_found": not_found,
        "stats": {
            "total_autofix": len(autofix_files),
            "mapped": found_count,
            "not_mapped": len(not_found),
        },
    }

    output_file = os.path.join(
        base_dir, "outputs/answers/2026-04-12-autofix-自动映射表.md"
    )
    json_file = os.path.join(
        base_dir, "outputs/answers/2026-04-12-autofix-自动映射表.json"
    )

    # 保存为 Markdown 表格
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("created_at: 2026-04-12\n")
        f.write("topics: [autofix, 知识库维护]\n")
        f.write("related_concepts: [知识库运维总索引]\n")
        f.write("status: active\n")
        f.write("---\n\n")
        f.write("# Autofix 自动映射表\n\n")
        f.write("本表通过文件名匹配自动生成，用于批量清理 autofix 占位页。\n\n")
        f.write("| Autofix 文件名 | 实际文件路径 | Wiki链接 | 匹配类型 | 置信度 |\n")
        f.write("|---|---|---|---|---|\n")

        for autofix_name, mapping in sorted(mappings.items()):
            actual_rel = os.path.relpath(mapping["actual_path"], base_dir)
            f.write(
                f"| `{autofix_name}` | `{actual_rel}` | `{mapping['wiki_link']}` | {mapping['match_type']} | {mapping['confidence']:.2f} |\n"
            )

        if not_found:
            f.write("\n## 未找到映射的文件\n\n")
            for name in not_found:
                f.write(f"- `{name}`\n")

    # 保存为 JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存:")
    print(f"  Markdown 表格: {output_file}")
    print(f"  JSON 数据: {json_file}")

    # 显示一些示例
    if mappings:
        print("\n映射示例（前5个）:")
        for i, (name, mapping) in enumerate(list(mappings.items())[:5]):
            print(f"  {name} -> {os.path.basename(mapping['actual_path'])}")

    if not_found:
        print("\n未找到映射示例（前10个）:")
        for name in not_found[:10]:
            print(f"  {name}")

    return results


def main():
    print("开始分析 autofix 文件映射关系...")
    results = analyze_mappings()
    print("\n分析完成。")


if __name__ == "__main__":
    main()
