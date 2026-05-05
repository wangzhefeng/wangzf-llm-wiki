#!/usr/bin/env python3
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
RAW_ROOT = ROOT / "raw"

# 需要修复的文件列表（从健康检查输出中获取）
FILES_TO_FIX = [
    "raw/local-notes/computer-vision/cnn/index.md",
    "raw/local-notes/computer-vision/index.md",
    "raw/local-notes/control-algorithms/index.md",
    "raw/local-notes/data-analysis/index.md",
    "raw/local-notes/data-structure-algorithm/index.md",
    "raw/local-notes/deep-learning/index.md",
    "raw/local-notes/llm/index.md",
    "raw/local-notes/machine-learning/index.md",
    "raw/local-notes/nlp/index.md",
    "raw/local-notes/operations-research/index.md",
    "raw/local-notes/timeseries/timeseries-books/index.md",
    "raw/local-notes/timeseries/timeseries-descriptive/index.md",
    "raw/local-notes/timeseries/timeseries-filter/index.md",
    "raw/local-notes/timeseries/timeseries-frequency-domain/index.md",
    "raw/local-notes/timeseries/timeseries-libs/index.md",
    "raw/local-notes/timeseries/timeseries-projects/index.md",
    "raw/local-notes/timeseries/timeseries-time-domain/index.md",
]


# 根据路径确定topic
def determine_topic(path_str):
    if "computer-vision" in path_str or "cv" in path_str:
        return ["computer-vision"]
    elif "control-algorithms" in path_str:
        return ["control-algorithms"]
    elif "data-analysis" in path_str:
        return ["data-analysis"]
    elif "data-structure-algorithm" in path_str:
        return ["data-structure-algorithm"]
    elif "deep-learning" in path_str:
        return ["deep-learning"]
    elif "llm" in path_str:
        return ["llm", "natural-language-processing"]
    elif "machine-learning" in path_str:
        return ["machine-learning"]
    elif "nlp" in path_str:
        return ["natural-language-processing"]
    elif "operations-research" in path_str:
        return ["operations-research"]
    elif "timeseries" in path_str:
        return ["timeseries"]
    else:
        return ["knowledge-base"]


def split_frontmatter(text):
    """分割frontmatter和正文"""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5 :]

    # 解析frontmatter
    fm = {}
    current_key = None
    for line in fm_raw.splitlines():
        line = line.rstrip()
        if not line:
            continue
        # 检查是否是键值对
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            value = m.group(2).strip()
            if value == "":
                fm[current_key] = []
            else:
                fm[current_key] = value
        # 检查是否是列表项（以-开头）
        elif (
            line.strip().startswith("- ")
            and current_key
            and isinstance(fm.get(current_key), list)
        ):
            fm[current_key].append(line.strip()[2:].strip())

    return fm, body


def create_frontmatter(fm_dict, path_str):
    """创建或更新frontmatter"""
    # 确保必需字段
    if "source_type" not in fm_dict:
        fm_dict["source_type"] = "local_note"

    if "created_at" not in fm_dict:
        fm_dict["created_at"] = "2026-04-11"  # 今天

    if "topics" not in fm_dict:
        fm_dict["topics"] = determine_topic(path_str)

    if "status" not in fm_dict:
        fm_dict["status"] = "linked"

    # 确保topics是列表
    if isinstance(fm_dict["topics"], str):
        fm_dict["topics"] = [fm_dict["topics"]]

    # 如果有title但没有title字段，添加title
    if "title" not in fm_dict:
        # 从路径推断标题
        path = Path(path_str)
        if path.name == "index.md":
            # 使用父目录名
            fm_dict["title"] = path.parent.name.replace("-", " ").title()
        else:
            fm_dict["title"] = path.stem.replace("-", " ").title()

    return fm_dict


def format_frontmatter(fm_dict):
    """格式化frontmatter为YAML"""
    lines = ["---"]
    for key, value in fm_dict.items():
        if isinstance(value, list):
            if value:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: []")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def fix_file(file_path):
    """修复单个文件的frontmatter"""
    path = ROOT / file_path
    if not path.exists():
        print(f"Warning: File not found: {file_path}")
        return False

    try:
        content = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(content)

        # 创建新的frontmatter
        new_fm = create_frontmatter(fm, file_path)
        new_frontmatter = format_frontmatter(new_fm)

        # 写入文件
        new_content = new_frontmatter + "\n" + body
        path.write_text(new_content, encoding="utf-8")
        print(f"Fixed: {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    print(f"Fixing {len(FILES_TO_FIX)} files...")
    fixed_count = 0
    for file_path in FILES_TO_FIX:
        if fix_file(file_path):
            fixed_count += 1

    print(f"\nFixed {fixed_count} out of {len(FILES_TO_FIX)} files")


if __name__ == "__main__":
    main()
