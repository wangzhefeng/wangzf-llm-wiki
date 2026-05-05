#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES_ROOT = ROOT / "wiki" / "sources"

START = "<!-- AUTO-GENERATED: sources-dir-index:start -->"
END = "<!-- AUTO-GENERATED: sources-dir-index:end -->"


def md_files(base: Path) -> list[Path]:
    return sorted([p for p in base.glob("*.md") if p.is_file()])


def collect_dir_targets(dir_path: Path) -> list[str]:
    items: list[str] = []
    for p in md_files(dir_path):
        if p.name == "README.md":
            continue
        rel = p.relative_to(ROOT).with_suffix("").as_posix()
        items.append(rel)
    return sorted(items)


def upsert_block(text: str, block: str) -> str:
    if START in text and END in text:
        pre = text.split(START, 1)[0]
        post = text.split(END, 1)[1]
        # 保留 END 后原文
        return pre + block + post
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block


def render_block(title: str, stems: list[str]) -> str:
    lines: list[str] = []
    lines.append(START + "\n")
    lines.append(f"\n## {title}\n\n")
    lines.append("> 本区块由脚本生成：用于避免来源卡成为孤页（仅统计 wikilinks）。\n\n")
    for s in stems:
        lines.append(f"- [[{s}]]\n")
    lines.append("\n" + END + "\n")
    return "".join(lines)


def process_readme(readme: Path, apply: bool) -> bool:
    stems = collect_dir_targets(readme.parent)
    if not stems:
        return False
    text = readme.read_text(encoding="utf-8")
    block = render_block("本目录来源卡清单（自动生成）", stems)
    new_text = upsert_block(text, block)
    if new_text == text:
        return False
    if apply:
        readme.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill per-topic wiki/sources/*/README.md link indexes.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    if not SOURCES_ROOT.exists():
        print("wiki/sources not found.")
        return 0

    readmes = sorted([p for p in SOURCES_ROOT.rglob("README.md") if p.is_file() and p.parent != SOURCES_ROOT])
    changed = 0
    for r in readmes:
        if process_readme(r, args.apply):
            changed += 1

    if changed == 0:
        print("No changes needed.")
        return 0

    print(f"Topic READMEs updated: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
