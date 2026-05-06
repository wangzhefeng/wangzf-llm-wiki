#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_WEB_ROOT = ROOT / "raw" / "web"

YAML_KEY_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")


@dataclass(frozen=True)
class PatchResult:
    path: Path
    actions: tuple[str, ...]


def md_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*.md") if p.is_file()])


def split_frontmatter(text: str) -> tuple[list[str], list[str]]:
    if not text.startswith("---\n"):
        return [], text.splitlines(keepends=True)
    end = text.find("\n---\n", 4)
    if end == -1:
        return [], text.splitlines(keepends=True)
    fm_raw = text[4:end]
    body = text[end + 5 :]
    return fm_raw.splitlines(keepends=True), body.splitlines(keepends=True)


def parse_frontmatter(lines: list[str]) -> dict[str, object]:
    fm: dict[str, object] = {}
    key: str | None = None
    for line in lines:
        m = YAML_KEY_RE.match(line.rstrip("\n"))
        if m:
            key = m.group(1)
            v = m.group(2).strip()
            fm[key] = [] if v == "" else v
            continue
        if line.strip().startswith("- ") and key and isinstance(fm.get(key), list):
            fm[key] = [*fm.get(key, []), line.strip()[2:].strip()]
    return fm


def remove_key_block(fm_lines: list[str], key: str) -> tuple[list[str], bool]:
    out: list[str] = []
    removed = False
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        m = YAML_KEY_RE.match(line.rstrip("\n"))
        if m and m.group(1) == key:
            removed = True
            i += 1
            while i < len(fm_lines) and fm_lines[i].lstrip().startswith("- "):
                i += 1
            continue
        out.append(line if line.endswith("\n") else (line + "\n"))
        i += 1
    return out, removed


def ensure_raw_web_frontmatter(path: Path, text: str) -> tuple[str, tuple[str, ...]] | None:
    fm_lines, body_lines = split_frontmatter(text)
    if not fm_lines:
        # raw/web 应该总有 frontmatter；没有就不做“无损归一”，避免猜测结构
        return None

    fm = parse_frontmatter(fm_lines)
    actions: list[str] = []

    # key migrations (structure-only)
    if "source_url" not in fm and isinstance(fm.get("source"), str) and fm.get("source", "").strip():
        val = str(fm["source"]).strip()
        fm_lines, _ = remove_key_block(fm_lines, "source")
        fm_lines.append(f"source_url: {val}\n")
        actions.append("migrate: source -> source_url")

    if "published_at" not in fm and isinstance(fm.get("published"), str) and fm.get("published", "").strip():
        val = str(fm["published"]).strip()
        fm_lines, _ = remove_key_block(fm_lines, "published")
        fm_lines.append(f"published_at: {val}\n")
        actions.append("migrate: published -> published_at")

    # fill missing keys (allow null/empty list; do not infer)
    if "source_url" not in parse_frontmatter(fm_lines):
        fm_lines.append("source_url: null\n")
        actions.append("add: source_url")
    if "published_at" not in parse_frontmatter(fm_lines):
        fm_lines.append("published_at: null\n")
        actions.append("add: published_at")
    if "author" not in parse_frontmatter(fm_lines):
        fm_lines.append("author: null\n")
        actions.append("add: author")
    if "title" not in parse_frontmatter(fm_lines):
        fm_lines.append("title: null\n")
        actions.append("add: title")
    if "related_concepts" not in parse_frontmatter(fm_lines):
        fm_lines.append("related_concepts: []\n")
        actions.append("add: related_concepts")

    if not actions:
        return None

    new_text = "".join(["---\n", *fm_lines, "---\n", *body_lines])
    return new_text, tuple(actions)


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize raw/web frontmatter keys and fill missing metadata keys.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    ap.add_argument("--limit", type=int, default=0, help="Max files to modify (0 = no limit).")
    args = ap.parse_args()

    results: list[PatchResult] = []
    for p in md_files(RAW_WEB_ROOT):
        out = ensure_raw_web_frontmatter(p, p.read_text(encoding="utf-8"))
        if out is None:
            continue
        _, actions = out
        results.append(PatchResult(path=p, actions=actions))
        if args.limit and len(results) >= args.limit:
            break

    if not results:
        print("No changes needed.")
        return 0

    print(f"Candidates: {len(results)}")
    for r in results[:20]:
        rel = r.path.relative_to(ROOT).as_posix()
        print(f"- {rel} -> {', '.join(r.actions)}")
    if len(results) > 20:
        print(f"... ({len(results) - 20} more)")

    if args.apply:
        for r in results:
            p = r.path
            out = ensure_raw_web_frontmatter(p, p.read_text(encoding="utf-8"))
            if out is None:
                continue
            new_text, _ = out
            p.write_text(new_text, encoding="utf-8")
        print("Applied.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

