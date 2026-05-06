#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "raw"
WIKI_SOURCES = ROOT / "wiki" / "sources"


SOURCE_PATH_RE = re.compile(r"^source_path:\s*(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class NewCard:
    raw_path: Path
    card_path: Path


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
    return raw or None


def normalize_raw_path(p: str) -> str:
    return p.split("#", 1)[0].strip()


def infer_topic_dir(raw_rel: str) -> str:
    parts = Path(raw_rel).parts
    # raw/<type>/<topic>/file.md
    if len(parts) >= 3 and parts[0] == "raw":
        # local-notes has hyphen already, keep it
        if parts[1] in {"web", "papers", "repos", "datasets", "images", "local-notes"}:
            return parts[2]
    return "shared"


def card_filename_from_raw(raw_path: Path) -> str:
    # keep same filename for traceability
    return raw_path.name


def safe_title_from_filename(name: str) -> str:
    return name[:-3] if name.endswith(".md") else name


def build_card(raw_rel: str, title: str, topic_dir: str) -> str:
    # link target without .md
    raw_link = raw_rel[:-3] if raw_rel.endswith(".md") else raw_rel
    return (
        "---\n"
        "created_at: 2026-04-11\n"
        "topics:\n"
        f"  - {topic_dir}\n"
        "status: inbox\n"
        f"source_path: {raw_rel}\n"
        "---\n\n"
        f"# 来源卡：{title}\n\n"
        "## 这份材料讲了什么\n\n"
        f"- 原文：[[{raw_link}]]\n"
        f"- 来源路径：`{raw_rel}`\n\n"
        "## 价值是什么\n\n"
        "- （待补）一句话说明这份材料能解决什么问题/提供什么证据。\n\n"
        "## 连到哪些概念\n\n"
        "- （待补）[[对应主题总索引]] / [[相关概念页]]\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Create missing wiki/sources cards for raw/*.md files without source cards.")
    ap.add_argument("--apply", action="store_true", help="Write new cards to disk.")
    args = ap.parse_args()

    # collect existing referenced raw paths
    referenced: set[str] = set()
    for p in md_files(WIKI_SOURCES):
        text = p.read_text(encoding="utf-8", errors="ignore")
        sp = extract_source_path(text)
        if sp and sp.startswith("raw/"):
            referenced.add(normalize_raw_path(sp))

    new_cards: list[NewCard] = []
    for raw in md_files(RAW_ROOT):
        raw_rel = raw.relative_to(ROOT).as_posix()
        # only ingest primary source types; skip local note trees and thread archives
        if not raw_rel.startswith(("raw/web/", "raw/papers/", "raw/datasets/", "raw/images/", "raw/repos/")):
            continue
        # skip READMEs and templates / directory indexes
        if raw.name in {"README.md", "线程总结模板.md", "_index.md"}:
            continue
        if raw_rel in referenced:
            continue
        topic_dir = infer_topic_dir(raw_rel)
        dst_dir = WIKI_SOURCES / topic_dir
        if not dst_dir.exists():
            dst_dir = WIKI_SOURCES / "shared"
        dst = dst_dir / card_filename_from_raw(raw)
        if dst.exists():
            # don't overwrite
            continue
        new_cards.append(NewCard(raw_path=raw, card_path=dst))

    print(f"New cards to create: {len(new_cards)}")
    for c in new_cards[:30]:
        print(f"- {c.card_path.relative_to(ROOT).as_posix()} <- {c.raw_path.relative_to(ROOT).as_posix()}")
    if len(new_cards) > 30:
        print(f"... ({len(new_cards) - 30} more)")

    if not args.apply or not new_cards:
        return 0

    for c in new_cards:
        raw_rel = c.raw_path.relative_to(ROOT).as_posix()
        title = safe_title_from_filename(c.raw_path.name)
        topic_dir = c.card_path.parent.name
        c.card_path.write_text(build_card(raw_rel, title, topic_dir), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
