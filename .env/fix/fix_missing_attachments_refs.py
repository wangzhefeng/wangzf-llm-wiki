#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATT_ROOT = ROOT / "raw" / "assets" / "attachments"

# Match:
# - ![[raw/assets/attachments/...|alt]]
# - [![[raw/assets/attachments/...|alt]]](https://...)
EMBED_RE = re.compile(
    r"(?P<prefix>!?\[\[\s*(?P<path>raw/assets/attachments/[^\]|#]+)\s*(?:#[^\]]*)?(?:\|(?P<alt>[^\]]+))?\s*\]\])"
)
WRAPPED_LINK_RE = re.compile(
    r"\[\s*(?P<inner>!?\[\[\s*(?P<path>raw/assets/attachments/[^\]|#]+)\s*(?:#[^\]]*)?(?:\|(?P<alt>[^\]]+))?\s*\]\])\s*\]\((?P<url>https?://[^)]+)\)"
)


@dataclass(frozen=True)
class Fix:
    file: Path
    replacements: int


def md_files() -> list[Path]:
    bases = [ROOT / "raw", ROOT / "wiki", ROOT / "outputs"]
    out: list[Path] = []
    for b in bases:
        if not b.exists():
            continue
        out.extend([p for p in b.rglob("*.md") if p.is_file()])
    return sorted(out)


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def rewrite_text(text: str) -> tuple[str, int]:
    n = 0

    # 1) Prefer converting wrapped link embeds to standard markdown image if the local file is missing.
    def repl_wrapped(m: re.Match[str]) -> str:
        nonlocal n
        path = m.group("path").strip()
        alt = (m.group("alt") or "").strip()
        url = m.group("url").strip()
        if exists(path):
            return m.group(0)
        n += 1
        alt2 = alt if alt else Path(path).name
        return f"![{alt2}]({url})"

    text2 = WRAPPED_LINK_RE.sub(repl_wrapped, text)

    # 2) For bare embeds with missing files, replace with an HTML comment (non-rendering) to avoid broken assets.
    def repl_embed(m: re.Match[str]) -> str:
        nonlocal n
        path = m.group("path").strip()
        if exists(path):
            return m.group(0)
        n += 1
        # 不在注释里保留路径，避免后续“附件存在性扫描”误报
        return "<!-- missing attachment -->"

    text3 = EMBED_RE.sub(repl_embed, text2)
    return text3, n


def main() -> int:
    ap = argparse.ArgumentParser(description="Fix missing raw/assets/attachments references in markdown.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    fixes: list[Fix] = []
    for p in md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        new_text, n = rewrite_text(text)
        if n <= 0 or new_text == text:
            continue
        fixes.append(Fix(file=p, replacements=n))
        if args.apply:
            p.write_text(new_text, encoding="utf-8")

    if not fixes:
        print("No changes needed.")
        return 0

    print(f"Files to update: {len(fixes)}")
    for f in fixes[:40]:
        print(f"- {f.file.relative_to(ROOT)}: {f.replacements} replacements")
    if len(fixes) > 40:
        print(f"... ({len(fixes) - 40} more)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
