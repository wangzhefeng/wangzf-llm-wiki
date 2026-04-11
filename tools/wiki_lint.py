#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ALLOWED_STATUS = {"summarized", "inbox", "linked", "archived"}
EXPECTED_SOURCES = {
    "analysis",
    "autofix",
    "computervision",
    "control-algorithms",
    "data-structure-algorithm",
    "deeplearning",
    "knowledge-base",
    "llm",
    "machinelearning",
    "operationsresearch",
    "reinforcementlearning",
    "shared",
    "timeseries",
}
EXPECTED_CONCEPTS = {
    "analysis",
    "autofix",
    "computervision",
    "control-algorithms",
    "data-structure-algorithm",
    "deeplearning",
    "knowledge-base",
    "llm",
    "machinelearning",
    "operationsresearch",
    "reinforcementlearning",
    "timeseries",
}
REQUIRED_INDEXES = {
    "knowledge-base-building",
    "knowledge-base-operations",
    "knowledge-base-usage",
}


def md_files(base: Path) -> list[Path]:
    return sorted(base.rglob("*.md"))


def check_dirs(root: Path) -> list[str]:
    errors: list[str] = []
    sources = {p.name for p in (root / "wiki" / "sources").iterdir() if p.is_dir()}
    concepts = {p.name for p in (root / "wiki" / "concepts").iterdir() if p.is_dir()}
    indexes = {p.name for p in (root / "wiki" / "indexes").iterdir() if p.is_dir()}

    if sources != EXPECTED_SOURCES:
        errors.append(f"sources 顶层目录不一致: {sorted(sources)}")
    if concepts != EXPECTED_CONCEPTS:
        errors.append(f"concepts 顶层目录不一致: {sorted(concepts)}")

    missing_idx = REQUIRED_INDEXES - indexes
    if missing_idx:
        errors.append(f"indexes 缺少目录: {sorted(missing_idx)}")
    if "knowledge-base" in indexes:
        errors.append("indexes 不应出现 knowledge-base 目录")

    return errors


def check_source_path(root: Path) -> list[str]:
    errors: list[str] = []
    for p in md_files(root / "wiki" / "sources"):
        for line_no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.startswith("source_path:"):
                continue
            val = line.split(":", 1)[1].strip()
            if not val.startswith("raw/"):
                errors.append(f"{p}:{line_no} source_path 非 raw/ 相对路径 -> {val}")
    return errors


def check_status(root: Path) -> list[str]:
    errors: list[str] = []
    for p in md_files(root / "wiki"):
        for line_no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.startswith("status:"):
                continue
            val = line.split(":", 1)[1].strip()
            if val not in ALLOWED_STATUS:
                errors.append(f"{p}:{line_no} status 非法 -> {val}")
    return errors


def check_relative_links(root: Path) -> list[str]:
    errors: list[str] = []
    pat = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")
    for p in md_files(root / "wiki"):
        text = p.read_text(encoding="utf-8")
        for rel in pat.findall(text):
            link = rel.strip()
            if link.startswith(("http://", "https://", "/", "#", "mailto:")):
                continue
            target = (p.parent / link).resolve()
            if not target.exists():
                errors.append(f"{p} -> {link} (不存在)")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    checks = [
        ("目录映射", check_dirs),
        ("source_path", check_source_path),
        ("status", check_status),
        ("相对链接", check_relative_links),
    ]

    all_errors: list[str] = []
    for name, fn in checks:
        errs = fn(root)
        if errs:
            all_errors.extend([f"[{name}] {e}" for e in errs])

    print("Wiki Lint Summary")
    print(f"- wiki/sources md: {len(md_files(root / 'wiki' / 'sources'))}")
    print(f"- wiki/indexes md: {len(md_files(root / 'wiki' / 'indexes'))}")
    print(f"- wiki/concepts md: {len(md_files(root / 'wiki' / 'concepts'))}")

    if all_errors:
        print(f"\n发现问题: {len(all_errors)}")
        for e in all_errors[:200]:
            print(f"- {e}")
        if len(all_errors) > 200:
            print(f"- ... 其余 {len(all_errors) - 200} 条省略")
        return 1

    print("\n未发现结构/字段/链接一致性问题。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
