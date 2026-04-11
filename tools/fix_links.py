#!/usr/bin/env python3
import re
from pathlib import Path
import os

ROOT = Path(__file__).parent
WIKI_ROOT = ROOT / "wiki"

# 映射表：错误的链接目标 -> 正确的目录名
LINK_MAPPINGS = {
    # concepts目录
    "wiki/concepts/analysis/": "wiki/concepts/data-analysis/",
    "wiki/concepts/computervision/": "wiki/concepts/computer-vision/",
    "wiki/concepts/deeplearning/": "wiki/concepts/deep-learning/",
    "wiki/concepts/machinelearning/": "wiki/concepts/machine-learning/",
    "wiki/concepts/operationsresearch/": "wiki/concepts/operations-research/",
    "wiki/concepts/reinforcementlearning/": "wiki/concepts/reinforcement-learning/",
    # sources目录
    "wiki/sources/analysis/": "wiki/sources/data-analysis/",
    "wiki/sources/computervision/": "wiki/sources/computer-vision/",
    "wiki/sources/deeplearning/": "wiki/sources/deep-learning/",
    "wiki/sources/machinelearning/": "wiki/sources/machine-learning/",
    "wiki/sources/operationsresearch/": "wiki/sources/operations-research/",
    "wiki/sources/reinforcementlearning/": "wiki/sources/reinforcement-learning/",
    # 处理不带wiki/前缀的链接
    "concepts/analysis/": "concepts/data-analysis/",
    "concepts/computervision/": "concepts/computer-vision/",
    "concepts/deeplearning/": "concepts/deep-learning/",
    "concepts/machinelearning/": "concepts/machine-learning/",
    "concepts/operationsresearch/": "concepts/operations-research/",
    "concepts/reinforcementlearning/": "concepts/reinforcement-learning/",
    "sources/analysis/": "sources/data-analysis/",
    "sources/computervision/": "sources/computer-vision/",
    "sources/deeplearning/": "sources/deep-learning/",
    "sources/machinelearning/": "sources/machine-learning/",
    "sources/operationsresearch/": "sources/operations-research/",
    "sources/reinforcementlearning/": "sources/reinforcement-learning/",
}

# 正则表达式匹配wikilink
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def fix_links_in_file(file_path):
    """修复单个文件中的错误链接"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        changed = False

        def replace_link(match):
            link_text = match.group(1)
            # 检查是否包含竖线分隔符
            if "|" in link_text:
                link, display = link_text.split("|", 1)
                link = link.strip()
                display = display.strip()
            else:
                link = link_text.strip()
                display = None

            # 检查是否需要替换
            for wrong, right in LINK_MAPPINGS.items():
                if link.startswith(wrong):
                    new_link = right + link[len(wrong) :]
                    if display:
                        return f"[[{new_link}|{display}]]"
                    else:
                        return f"[[{new_link}]]"

            # 不需要替换
            return match.group(0)

        new_content = WIKILINK_RE.sub(replace_link, content)

        if new_content != original:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    # 查找所有markdown文件
    md_files = list(WIKI_ROOT.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files in wiki/")

    fixed_count = 0
    for md_file in md_files:
        if fix_links_in_file(md_file):
            fixed_count += 1
            print(f"Fixed links in: {md_file.relative_to(ROOT)}")

    print(f"\nFixed {fixed_count} files")


if __name__ == "__main__":
    main()
