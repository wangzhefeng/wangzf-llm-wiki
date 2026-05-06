#!/usr/bin/env python3
"""
清理剩余 autofix 文件的脚本

删除所有剩余 autofix 文件，更新 index.md，并记录清理操作。
"""

import os
import re
import glob
import json
import shutil
from pathlib import Path


def get_all_autofix_files(autofix_dir):
    """获取所有autofix文件（不包括index.md）"""
    files = []
    for md_file in glob.glob(os.path.join(autofix_dir, "*.md")):
        if md_file.endswith("index.md"):
            continue
        files.append(
            {
                "path": md_file,
                "filename": os.path.basename(md_file),
                "name_without_ext": os.path.basename(md_file)[:-3],
            }
        )
    return files


def find_references(root_dir, target):
    """查找引用"""
    references = []
    wiki_link_pattern1 = re.compile(r"\[\[\s*" + re.escape(target) + r"\s*(?:\||\]\])")
    wiki_link_pattern2 = re.compile(
        r"\[\[\s*(?:[^|\]]*/\s*)?" + re.escape(target) + r"\s*(?:\||\]\])"
    )

    for md_file in glob.glob(os.path.join(root_dir, "**/*.md"), recursive=True):
        if "wiki/sources/autofix" in md_file:
            continue

        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                if wiki_link_pattern1.search(content) or wiki_link_pattern2.search(
                    content
                ):
                    references.append(os.path.relpath(md_file, root_dir))
        except Exception:
            continue

    return references


def update_autofix_index(index_file, files_to_remove):
    """从index.md中移除多个条目"""
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 为每个文件构建移除模式
    new_content = content
    for file_info in files_to_remove:
        name = file_info["name_without_ext"]
        # 模式1: [[wiki/sources/autofix/filename]]
        pattern1 = r"\[\[\s*wiki/sources/autofix/" + re.escape(name) + r"\s*\]\]"
        # 模式2: [[filename]]（简写形式）
        pattern2 = r"\[\[\s*" + re.escape(name) + r"\s*\]\]"

        new_content = re.sub(pattern1, "", new_content)
        new_content = re.sub(pattern2, "", new_content)

    # 清理空行和多余空白
    lines = new_content.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if (
            stripped == ""
            or stripped == "-"
            or stripped.startswith("- ")
            and len(stripped) <= 3
        ):
            # 跳过空行或只有"-"的行
            continue
        cleaned_lines.append(line)

    new_content = "\n".join(cleaned_lines)

    # 确保文件末尾有换行
    if new_content and not new_content.endswith("\n"):
        new_content += "\n"

    return new_content if new_content != content else None


def main():
    parser = argparse.ArgumentParser(description="清理剩余 autofix 文件")
    parser.add_argument(
        "--execute", action="store_true", help="执行实际操作（默认只显示计划）"
    )
    parser.add_argument("--backup", action="store_true", help="备份 autofix 目录")
    args = parser.parse_args()

    base_dir = "/Users/wangzf/wangzf-llm-wiki"
    autofix_dir = os.path.join(base_dir, "wiki/sources/autofix")
    autofix_index = os.path.join(autofix_dir, "index.md")
    wiki_root = os.path.join(base_dir, "wiki")

    print(f"工作目录: {base_dir}")
    print(f"Autofix 目录: {autofix_dir}")
    print(f"执行模式: {'是' if args.execute else '否（dry run）'}")
    print("=" * 80)

    # 获取所有剩余文件
    files = get_all_autofix_files(autofix_dir)
    print(f"找到 {len(files)} 个待清理的 autofix 文件")

    # 分析引用
    all_references = {}
    print("分析引用情况...")
    for i, file_info in enumerate(files):
        if i % 20 == 0:
            print(f"  进度: {i}/{len(files)}")

        name = file_info["name_without_ext"]
        refs = find_references(wiki_root, name)
        all_references[name] = refs

    # 统计
    total_refs = sum(len(refs) for refs in all_references.values())
    files_with_refs = sum(1 for refs in all_references.values() if refs)

    print(f"\n引用统计:")
    print(f"  总引用数: {total_refs}")
    print(f"  有引用的文件: {files_with_refs}")
    print(f"  无引用的文件: {len(files) - files_with_refs}")

    # 备份
    if args.execute and args.backup:
        backup_dir = os.path.join(
            base_dir, f"autofix_backup_{time.strftime('%Y%m%d_%H%M%S')}"
        )
        shutil.copytree(autofix_dir, backup_dir)
        print(f"\n已备份到: {backup_dir}")

    # 执行清理
    if args.execute:
        # 1. 更新 index.md
        new_index_content = update_autofix_index(autofix_index, files)
        if new_index_content:
            with open(autofix_index, "w", encoding="utf-8") as f:
                f.write(new_index_content)
            print(f"更新了 index.md")

        # 2. 删除文件
        deleted_count = 0
        for file_info in files:
            try:
                os.remove(file_info["path"])
                deleted_count += 1
            except OSError as e:
                print(f"错误：无法删除文件 {file_info['filename']}: {e}")

        print(f"删除了 {deleted_count} 个文件")
    else:
        # Dry run
        print(f"\n[dry run] 将删除 {len(files)} 个文件")
        print(f"[dry run] 将更新 index.md")
        print(f"[dry run] 总引用将断开: {total_refs}")

    # 保存清理记录
    record_file = os.path.join(
        base_dir, "outputs/logs/2026-04-12-autofix-剩余文件清理记录.md"
    )
    record_data = {
        "files": [f["name_without_ext"] for f in files],
        "references": all_references,
        "stats": {
            "total_files": len(files),
            "files_with_references": files_with_refs,
            "total_references": total_refs,
        },
    }

    # 创建 Markdown 记录
    with open(record_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("created_at: 2026-04-12\n")
        f.write("topics: [autofix, 知识库维护]\n")
        f.write("related_concepts: [知识库运维总索引]\n")
        f.write("status: active\n")
        f.write("---\n\n")
        f.write("# Autofix 剩余文件清理记录\n\n")
        f.write(f"本记录包含 {len(files)} 个被清理的 autofix 占位页。\n\n")

        f.write("## 统计信息\n\n")
        f.write(f"- 总文件数: {len(files)}\n")
        f.write(f"- 有引用的文件: {files_with_refs}\n")
        f.write(f"- 总引用数: {total_refs}\n")
        f.write(f"- 执行时间: 2026-04-12\n")

        f.write("\n## 文件清单与引用\n\n")
        f.write("| 文件名 | 引用数 | 引用位置 |\n")
        f.write("|---|---|---|\n")

        for file_info in sorted(
            files,
            key=lambda x: len(all_references[x["name_without_ext"]]),
            reverse=True,
        ):
            name = file_info["name_without_ext"]
            refs = all_references[name]
            ref_count = len(refs)
            ref_list = ", ".join([f"`{r}`" for r in refs[:3]])
            if len(refs) > 3:
                ref_list += f" ... 等 {len(refs) - 3} 个"

            f.write(f"| `{name}` | {ref_count} | {ref_list} |\n")

        f.write("\n## 后续建议\n\n")
        f.write("1. 检查引用文件中的断链，更新为实际资源链接\n")
        f.write("2. 对于重要资源，考虑收录到 `raw/web/` 并创建来源卡\n")
        f.write("3. 定期检查知识库健康状态，避免创建空占位页\n")

    print(f"\n清理记录已保存到: {record_file}")

    if not args.execute:
        print("\n注意：以上为 dry run 模式，未实际修改任何文件")
        print("如需执行，请添加 --execute 参数")

    return len(files)


if __name__ == "__main__":
    import argparse
    import time

    main()
