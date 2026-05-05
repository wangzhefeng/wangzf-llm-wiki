#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = ROOT / "wiki"


LINE_MD_RE = re.compile(r"^\s*([^#\[\]\n].*?)\.md\s*$")


@dataclass(frozen=True)
class Change:
    path: Path
    changed_lines: int


def md_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*.md") if p.is_file()])


def should_process(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if not rel.startswith("wiki/sources/"):
        return False
    # 只处理“来源聚合/清单类”文件，避免误改正文内容
    name = path.name
    return name.endswith("专题来源.md") or name.endswith("本地笔记.md") or name == "README.md"


def rewrite(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    changed = 0
    for line in lines:
        m = LINE_MD_RE.match(line)
        if not m:
            out.append(line)
            continue
        raw = m.group(1).strip()
        if not raw or raw.startswith("- ") or raw.startswith("* "):
            out.append(line)
            continue
        stem = raw
        out.append(f"- [[{stem}]]\n")
        changed += 1
    return "".join(out), changed


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert plain *.md filename lists to wikilinks.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    changes: list[Change] = []
    for p in md_files(WIKI_ROOT):
        if not should_process(p):
            continue
        text = p.read_text(encoding="utf-8")
        new_text, n = rewrite(text)
        if n <= 0 or new_text == text:
            continue
        changes.append(Change(path=p, changed_lines=n))
        if args.apply:
            p.write_text(new_text, encoding="utf-8")

    if not changes:
        print("No changes needed.")
        return 0

    print(f"Files changed: {len(changes)}")
    for c in changes[:30]:
        rel = c.path.relative_to(ROOT).as_posix()
        print(f"- {rel}: {c.changed_lines} lines")
    if len(changes) > 30:
        print(f"... ({len(changes) - 30} more)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

