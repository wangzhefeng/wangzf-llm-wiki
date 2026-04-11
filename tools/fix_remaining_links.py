#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).parent
WIKI_ROOT = ROOT / "wiki"

# 映射表：错误的链接目标 -> 正确的路径
LINK_MAPPINGS = {
    # 修复 raw/localnotes/analysis/ -> raw/localnotes/data-analysis/
    "raw/localnotes/analysis/": "raw/localnotes/data-analysis/",
    # 修复其他可能的错误
    "raw/web/tools/": "raw/web/programming-tools/",  # 检查这个映射
    "raw/web/llm/": "raw/web/llm-pre-training/",  # llm可能指向llm-pre-training
    # 修复可能缺少的目录层级
}

# 正则表达式匹配wikilink
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def fix_remaining_links_in_file(file_path):
    """修复单个文件中的剩余链接"""
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

            original_link = link

            # 跳过 wiki/log.md 中的 [[raw/...]] 占位符
            if link == "raw/..." and file_path.name == "log.md":
                return match.group(0)

            # 应用映射
            for wrong, right in LINK_MAPPINGS.items():
                if link.startswith(wrong):
                    link = right + link[len(wrong) :]

            # 检查是否是raw/...链接且没有.md扩展名
            if (
                link.startswith("raw/")
                and not link.endswith(".md")
                and not link.endswith(".png")
                and not link.endswith(".jpg")
                and not link.endswith(".jpeg")
                and not link.endswith(".gif")
                and not link.endswith(".svg")
            ):
                # 检查是否存在对应的.md文件
                md_path = ROOT / (link + ".md")
                if md_path.exists():
                    link = link + ".md"
                else:
                    # 检查是否是目录索引（以index结尾）
                    if link.endswith("/index"):
                        md_path = ROOT / (link + ".md")
                        if md_path.exists():
                            link = link + ".md"
                    # 检查是否是其他扩展名
                    else:
                        # 尝试查找实际文件
                        parent_dir = ROOT / Path(link).parent
                        if parent_dir.exists():
                            stem = Path(link).name
                            # 查找匹配的文件
                            for f in parent_dir.iterdir():
                                if f.stem == stem and f.suffix in [
                                    ".md",
                                    ".png",
                                    ".jpg",
                                    ".jpeg",
                                    ".gif",
                                    ".svg",
                                ]:
                                    link = str(f.relative_to(ROOT))
                                    break

            # 如果链接被修改了
            if link != original_link:
                if display:
                    return f"[[{link}|{display}]]"
                else:
                    return f"[[{link}]]"
            else:
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
        if fix_remaining_links_in_file(md_file):
            fixed_count += 1
            print(f"Fixed remaining links in: {md_file.relative_to(ROOT)}")

    print(f"\nFixed {fixed_count} files")


if __name__ == "__main__":
    main()
