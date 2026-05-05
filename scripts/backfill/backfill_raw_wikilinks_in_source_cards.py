#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI_SOURCES = ROOT / "wiki" / "sources"


SOURCE_PATH_RE = re.compile(r"^source_path:\s*(.+?)\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]*)?(?:\|[^\]]*)?\]\]")


@dataclass(frozen=True)
class Change:
    path: Path
    added: bool


def md_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*.md") if p.is_file()])


def extract_source_path(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fm = text[4:end]
    m = SOURCE_PATH_RE.search(fm)
    if not m:
        return None
    raw = m.group(1).strip().strip('"').strip("'")
    if not raw:
        return None
    return raw


def normalize_wikilink_target(path_or_path_with_anchor: str) -> str:
    # `raw/.../x.md#anchor` -> `raw/.../x`
    p = path_or_path_with_anchor.split("#", 1)[0].strip()
    if p.endswith(".md"):
        p = p[:-3]
    return p


def has_raw_wikilink(text: str, target: str) -> bool:
    for t in WIKILINK_RE.findall(text):
        if t.strip() == target:
            return True
    return False


def insert_under_section(text: str, header: str, line_to_insert: str) -> tuple[str, bool]:
    # Insert the line right after the section header line, but after any blank line(s).
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip() == header.strip():
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            lines.insert(j, line_to_insert if line_to_insert.endswith("\n") else (line_to_insert + "\n"))
            return "".join(lines), True
    return text, False


def rewrite(text: str) -> tuple[str, bool]:
    sp = extract_source_path(text)
    if not sp or not sp.startswith("raw/"):
        return text, False
    target = normalize_wikilink_target(sp)
    if has_raw_wikilink(text, target):
        return text, False

    line = f"- 原文：[[{target}]]\n"

    # Preferred section
    new_text, ok = insert_under_section(text, "## 这份材料讲了什么", line)
    if ok:
        return new_text, True

    # Fallback: insert after first H1 title
    lines = text.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.startswith("# "):
            insert_at = i + 1
            while insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            lines.insert(insert_at, "\n" + line)
            return "".join(lines), True

    # Last resort: append
    return text + "\n" + line, True


def should_process(p: Path) -> bool:
    # Skip directory READMEs and collection files; only touch source cards.
    if p.name == "README.md":
        return False
    if p.name.endswith("专题来源.md") or p.name.endswith("本地笔记.md"):
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill explicit wikilinks to raw sources in wiki/sources cards.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    changes: list[Change] = []
    for p in md_files(WIKI_SOURCES):
        if not should_process(p):
            continue
        text = p.read_text(encoding="utf-8")
        new_text, changed = rewrite(text)
        if not changed or new_text == text:
            continue
        changes.append(Change(path=p, added=True))
        if args.apply:
            p.write_text(new_text, encoding="utf-8")

    print(f"Changed files: {len(changes)}")
    for c in changes[:30]:
        rel = c.path.relative_to(ROOT).as_posix()
        print(f"- {rel}")
    if len(changes) > 30:
        print(f"... ({len(changes) - 30} more)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

