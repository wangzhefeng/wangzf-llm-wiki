#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "raw"
WIKI_SOURCES = ROOT / "wiki" / "sources"


SOURCE_PATH_LINE_RE = re.compile(r"^source_path:\s*(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Fix:
    path: Path
    old: str
    new: str


def md_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*.md") if p.is_file()])


def parse_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[: end + 5], text[end + 5 :]


def get_source_path(fm: str) -> str | None:
    m = SOURCE_PATH_LINE_RE.search(fm)
    if not m:
        return None
    raw = m.group(1).strip().strip('"').strip("'")
    return raw or None


def normalize_path(p: str) -> str:
    return p.split("#", 1)[0].strip()


def wikilink_target_from_source_path(sp: str) -> str:
    p = normalize_path(sp)
    if p.endswith(".md"):
        p = p[:-3]
    return p


def safe_exists(p: Path) -> bool:
    try:
        return p.exists()
    except OSError:
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Fix broken source_path in wiki/sources by matching raw filename uniquely.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    raw_by_name: dict[str, list[Path]] = {}
    for p in md_files(RAW_ROOT):
        raw_by_name.setdefault(p.name, []).append(p)

    fixes: list[Fix] = []
    for p in md_files(WIKI_SOURCES):
        if p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        fm, body = parse_frontmatter(text)
        sp = get_source_path(fm)
        if not sp or not sp.startswith("raw/"):
            continue
        sp_norm = normalize_path(sp)
        if safe_exists(ROOT / sp_norm):
            continue
        fname = Path(sp_norm).name
        cands = raw_by_name.get(fname, [])
        if len(cands) != 1:
            continue
        new_sp = cands[0].relative_to(ROOT).as_posix()
        if new_sp == sp_norm:
            continue
        # keep anchor if present
        if "#" in sp:
            new_sp = new_sp + "#" + sp.split("#", 1)[1]

        fixes.append(Fix(path=p, old=sp, new=new_sp))

        if args.apply:
            old_target = wikilink_target_from_source_path(sp)
            new_target = wikilink_target_from_source_path(new_sp)

            new_fm = fm.replace(f"source_path: {sp}", f"source_path: {new_sp}")
            # best-effort update common body patterns
            new_body = body
            new_body = new_body.replace(f"[[{old_target}]]", f"[[{new_target}]]")
            new_body = new_body.replace(f"`{sp_norm}`", f"`{normalize_path(new_sp)}`")
            (p).write_text(new_fm + new_body, encoding="utf-8")

    print(f"Fixable source_path entries: {len(fixes)}")
    for f in fixes[:30]:
        rel = f.path.relative_to(ROOT).as_posix()
        print(f"- {rel}: {f.old} -> {f.new}")
    if len(fixes) > 30:
        print(f"... ({len(fixes) - 30} more)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

