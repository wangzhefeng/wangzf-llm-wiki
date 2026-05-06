#!/usr/bin/env python3
"""
批量修复autofix清理后的断链引用

从清理记录文件中读取断链文件名和引用位置，检查是否有实际对应文件存在，
如果存在则更新链接，否则删除引用或记录未找到。
"""

import os
import re
import sys
import argparse
from pathlib import Path

# 仓库根目录
ROOT_DIR = Path(__file__).parent.parent


def parse_cleanup_record(file_path):
    """解析清理记录文件，返回断链映射"""
    broken_links = {}

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 查找表格开始
    table_started = False
    for i, line in enumerate(lines):
        line = line.strip()

        # 表格标题行，包含"文件名 | 引用数 | 引用位置"
        if "文件名" in line and "引用数" in line and "引用位置" in line:
            table_started = True
            continue

        if table_started and line.startswith("| `"):
            # 表格行，格式: | `filename` | count | reference locations |
            # 移除首尾的|，分割字段
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                filename = parts[1].strip("`")
                ref_locations = parts[3]

                # 解析引用位置，可能是多个文件
                ref_files = []

                # 处理引用位置字符串
                # 可能格式: "file1.md, file2.md" 或 "file1.md ... 等 1 个"
                ref_text = ref_locations

                # 处理"... 等 1 个"格式
                if "... 等" in ref_text:
                    # 提取前面的文件路径
                    ref_text = ref_text.split("...")[0].strip()

                # 分割多个文件
                for ref in ref_text.split(","):
                    ref = ref.strip()
                    # 清理可能的`.`前缀
                    if ref.startswith("`"):
                        ref = ref.strip("`")
                    if ref and ref.endswith(".md"):
                        # 确保路径正确
                        if not ref.startswith("wiki/"):
                            ref = f"wiki/{ref}"
                        ref_files.append(ref)

                if filename and ref_files:
                    broken_links[filename] = ref_files

    return broken_links


def find_actual_file(filename):
    """
    在wiki目录中查找实际文件
    返回实际文件名（带扩展名）或None
    """
    # 提取关键标识部分：去掉日期和通用后缀
    # 例如: "2026-04-06-datawhalechinaeasy-rl 强化学习中文教程（蘑菇书）"
    # 关键部分: "datawhalechinaeasy-rl" 或 "强化学习中文教程（蘑菇书）"

    # 移除日期前缀
    key_part = filename
    if re.match(r"\d{4}-\d{2}-\d{2}-", filename):
        key_part = filename[11:]  # 移除"YYYY-MM-DD-"

    # 进一步清理，保留核心标识
    # 移除常见标点变体
    key_clean = (
        key_part.replace("'", "")
        .replace("’", "")
        .replace("...", "")
        .replace("⨁", "")
        .replace("⚡️", "")
    )

    # 分割成单词列表
    words = re.findall(r"[\w\u4e00-\u9fff]+", key_clean.lower())

    # 搜索wiki目录
    wiki_dir = ROOT_DIR / "wiki"
    best_match = None
    best_score = 0

    for root, dirs, files in os.walk(wiki_dir):
        for file in files:
            if not file.endswith(".md"):
                continue

            file_lower = file.lower()

            # 计算匹配分数
            score = 0
            matched_words = 0

            for word in words:
                if len(word) > 2 and word in file_lower:
                    score += 1
                    matched_words += 1

            # 如果匹配了大部分单词，认为是正确文件
            if matched_words > 0 and matched_words >= len(words) * 0.5:
                # 优先选择匹配更多的
                if matched_words > best_score:
                    best_score = matched_words
                    best_match = file

    # 也检查raw目录
    if not best_match:
        raw_dir = ROOT_DIR / "raw"
        for root, dirs, files in os.walk(raw_dir):
            for file in files:
                if not file.endswith(".md"):
                    continue

                file_lower = file.lower()
                score = 0
                matched_words = 0

                for word in words:
                    if len(word) > 2 and word in file_lower:
                        score += 1
                        matched_words += 1

                if matched_words > 0 and matched_words >= len(words) * 0.5:
                    if matched_words > best_score:
                        best_score = matched_words
                        best_match = file

    return best_match


def fix_file_links(file_path, broken_to_actual_map, dry_run=True):
    """修复单个文件中的断链链接"""
    if not os.path.exists(file_path):
        print(f"警告: 文件不存在 {file_path}")
        return 0

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    changes = 0

    for broken, actual in broken_to_actual_map.items():
        if not actual:
            continue

        # 创建Wiki链接模式
        pattern = rf"\[\[\s*{re.escape(broken)}\s*\]\]"

        # 查找所有匹配
        matches = list(re.finditer(pattern, content))
        if matches:
            # 检查是否已经指向正确文件
            actual_filename = actual.rstrip(".md")
            actual_pattern = rf"\[\[\s*{re.escape(actual_filename)}\s*\]\]"

            # 如果已经指向正确文件，跳过
            if re.search(actual_pattern, content):
                print(f"  跳过: {file_path} 中的 '{broken}' 已经指向正确文件")
                continue

            print(f"  在 {file_path} 中找到 {len(matches)} 个 '{broken}' 引用")

            # 替换为实际文件名（不带.md扩展名，因为Wiki链接通常不带）
            actual_link_name = actual.rstrip(".md")
            actual_link = f"[[{actual_link_name}]]"
            content = re.sub(pattern, actual_link, content)
            changes += len(matches)

    if changes > 0 and not dry_run:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  已更新 {changes} 个链接")
    elif changes > 0 and dry_run:
        print(f"  （干运行）将更新 {changes} 个链接")

    return changes


def main():
    parser = argparse.ArgumentParser(description="批量修复autofix清理后的断链引用")
    parser.add_argument(
        "--dry-run", action="store_true", help="干运行模式，只显示更改不实际修改"
    )
    parser.add_argument("--execute", action="store_true", help="实际执行修改")
    parser.add_argument(
        "--record",
        default="outputs/logs/2026-04-12-autofix-剩余文件清理记录.md",
        help="清理记录文件路径",
    )
    args = parser.parse_args()

    # 默认干运行，除非指定--execute
    dry_run = not args.execute if args.execute else True
    if args.dry_run:
        dry_run = True

    cleanup_record = ROOT_DIR / args.record

    if not cleanup_record.exists():
        print(f"错误: 清理记录文件不存在 {cleanup_record}")
        return

    print("解析清理记录文件...")
    broken_links = parse_cleanup_record(cleanup_record)

    print(f"找到 {len(broken_links)} 个断链文件")

    # 显示前几个示例
    print("\n示例断链文件:")
    for i, (broken, refs) in enumerate(list(broken_links.items())[:5]):
        print(f"  {broken} -> {refs}")
    if len(broken_links) > 5:
        print(f"  ... 还有 {len(broken_links) - 5} 个")

    # 创建实际文件映射
    actual_files = {}
    for broken in broken_links.keys():
        actual = find_actual_file(broken)
        if actual:
            actual_files[broken] = actual
            print(f"✓ 找到实际文件: {broken} -> {actual}")
        else:
            actual_files[broken] = None
            print(f"✗ 未找到实际文件: {broken}")

    # 统计
    found = sum(1 for v in actual_files.values() if v)
    not_found = sum(1 for v in actual_files.values() if not v)
    print(f"\n文件查找结果: 找到 {found} 个, 未找到 {not_found} 个")

    # 按文件分组处理
    file_to_broken_map = {}
    for broken, ref_files in broken_links.items():
        for ref_file in ref_files:
            if ref_file not in file_to_broken_map:
                file_to_broken_map[ref_file] = {}
            file_to_broken_map[ref_file][broken] = actual_files.get(broken)

    print(f"\n开始处理 {len(file_to_broken_map)} 个引用文件...")

    total_changes = 0
    total_files = 0

    for ref_file, broken_map in file_to_broken_map.items():
        file_path = ROOT_DIR / ref_file
        if not file_path.exists():
            # 尝试其他可能路径
            possible_paths = [
                ROOT_DIR / ref_file,
                ROOT_DIR / "wiki" / ref_file,
                ROOT_DIR / "wiki" / ref_file.replace("../", ""),
            ]

            for path in possible_paths:
                if path.exists():
                    file_path = path
                    break

        if not file_path.exists():
            print(f"警告: 引用文件不存在 {ref_file}")
            continue

        print(f"\n处理: {ref_file}")
        changes = fix_file_links(file_path, broken_map, dry_run)
        if changes > 0:
            total_changes += changes
            total_files += 1

    mode = "干运行" if dry_run else "实际执行"
    print(f"\n{mode}完成:")
    print(f"- 处理了 {total_files} 个文件")
    print(f"- 更新了 {total_changes} 个链接")

    # 生成报告
    report_path = ROOT_DIR / "outputs" / "logs" / "2026-04-12-断链修复报告.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""---
created_at: 2026-04-12
topics: [autofix, 知识库维护, 断链修复]
related_concepts: [知识库运维总索引]
status: active
---

# 断链修复报告

## 统计信息

- 断链文件数: {len(broken_links)}
- 找到实际文件: {found}
- 未找到实际文件: {not_found}
- 处理的引用文件: {total_files}
- 更新的链接数: {total_changes}
- 执行模式: {mode}
- 执行时间: 2026-04-12

## 文件查找结果

### 找到的实际文件

""")

        for broken, actual in actual_files.items():
            if actual:
                f.write(f"- `{broken}` → `{actual}`\n")

        f.write("\n### 未找到的实际文件\n\n")

        for broken, actual in actual_files.items():
            if not actual:
                f.write(f"- `{broken}`\n")

        f.write(f"\n## 处理的文件\n\n")

        for ref_file in sorted(file_to_broken_map.keys()):
            f.write(f"- `{ref_file}`\n")

    print(f"\n报告已保存到: {report_path}")


if __name__ == "__main__":
    main()
