#!/usr/bin/env python3
"""Fix wikilinks after space→hyphen rename: [[Chapter 1 Basics]] → [[Chapter-1-Basics]].
Only rewrites links where the target filename (with hyphens) actually exists on disk."""

import re
from pathlib import Path

WIKI_ROOT = Path("/Users/wangzf/wangzf-llm-wiki/wiki")


def find_files(root: Path) -> set[str]:
    """Return set of all .md filenames (without .md) in wiki/."""
    return {f.stem for f in root.rglob("*.md")}


def main():
    existing = find_files(WIKI_ROOT)
    print(f"Total files in wiki/: {len(existing)}\n")

    # Scan all wikilinks containing spaces → build rename map
    rename_map: dict[str, str] = {}
    unknown: set[str] = set()

    for fpath in WIKI_ROOT.rglob("*.md"):
        content = fpath.read_text(encoding="utf-8")
        for m in re.finditer(r"\[\[([^]\]]* [^]\]]*)(?:\|[^\]]*)?\]\]", content):
            target = m.group(1)
            new_name = target.replace(" ", "-")
            if new_name == target:
                continue  # no spaces
            if new_name in existing:
                rename_map[target] = new_name
            else:
                unknown.add(target)

    print(f"Wikilinks to update:  {len(rename_map)} unique")
    print(f"Unknown targets:     {len(unknown)} (no matching file on disk)\n")

    if unknown:
        print("Unknown targets (will NOT be changed):")
        for t in sorted(unknown)[:20]:
            print(f"  [[{t}]]")
        print(f"  ... ({len(unknown)} total)\n")

    if not rename_map:
        print("Nothing to update.")
        return

    # Show sample
    print("Sample updates:")
    for i, (old, new) in enumerate(list(rename_map.items())[:10]):
        print(f"  [[{old}]] → [[{new}]]")
    print()

    # Update all files (sorted by key length descending to avoid partial matches)
    sorted_keys = sorted(rename_map.keys(), key=len, reverse=True)
    stats = {"scanned": 0, "updated": 0, "modified": 0}

    for fpath in WIKI_ROOT.rglob("*.md"):
        stats["scanned"] += 1
        content = fpath.read_text(encoding="utf-8")
        modified = False

        for old_name in sorted_keys:
            new_name = rename_map[old_name]
            escaped = re.escape(old_name)
            pattern = re.compile(rf"\[\[{escaped}(?:\|[^\]]*)?\]\]")
            new_content, count = pattern.subn(
                lambda m: "[[{}]]".format(new_name) if "|" not in m.group()
                else "[[{}|{}]]".format(new_name, m.group().split("|", 1)[1][:-2]),
                content,
            )
            if count > 0:
                content = new_content
                stats["updated"] += count
                modified = True

        if modified:
            fpath.write_text(content, encoding="utf-8")
            stats["modified"] += 1

    print(f"=== Done ===")
    print(f"  Files scanned:   {stats['scanned']}")
    print(f"  Links updated:   {stats['updated']}")
    print(f"  Files modified:  {stats['modified']}")


if __name__ == "__main__":
    main()
