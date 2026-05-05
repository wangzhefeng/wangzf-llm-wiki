#!/usr/bin/env python3
"""Rename files in wiki/ with spaces → hyphens, and update all [[wikilinks]]."""

import os
import re
from pathlib import Path

WIKI_ROOT = Path("/Users/wangzf/wangzf-llm-wiki/wiki")


def find_files_with_spaces(root: Path) -> list[tuple[Path, Path]]:
    """Find all .md files with spaces. Returns [(old_path, new_path)]."""
    plan = []
    for fpath in root.rglob("*.md"):
        if " " in fpath.name:
            new_name = fpath.name.replace(" ", "-")
            new_path = fpath.parent / new_name
            plan.append((fpath, new_path))
    return plan


def wikilink_pattern(filename: str) -> re.Pattern:
    """Build a regex that matches [[filename]] or [[filename|alias]]."""
    # Escape regex special chars
    escaped = re.escape(filename)
    return re.compile(rf"\[\[{escaped}(?:\|[^\]]*)?\]\]")


def update_references(plan: list[tuple[Path, Path]], root: Path) -> dict:
    """Update all wikilinks in all wiki/ .md files. Returns stats."""
    stats = {"files_scanned": 0, "links_updated": 0, "files_modified": 0}

    # Build lookup: old_name → new_name (just the filename, not full path)
    rename_map = {}
    for old_path, new_path in plan:
        rename_map[old_path.name] = new_path.name

    # Scan all wiki files
    for fpath in root.rglob("*.md"):
        stats["files_scanned"] += 1
        content = fpath.read_text(encoding="utf-8")
        modified = False

        for old_name, new_name in rename_map.items():
            pattern = wikilink_pattern(old_name)
            new_content, count = pattern.subn(
                lambda m: m.group(0).replace(old_name, new_name), content
            )
            if count > 0:
                content = new_content
                stats["links_updated"] += count
                modified = True

        if modified:
            fpath.write_text(content, encoding="utf-8")
            stats["files_modified"] += 1

    return stats


def execute_renames(plan: list[tuple[Path, Path]]) -> int:
    """Execute the file renames. Returns number of renames."""
    count = 0
    for old_path, new_path in plan:
        if new_path.exists():
            print(f"  SKIP (target exists): {old_path.name}")
            continue
        old_path.rename(new_path)
        print(f"  RENAME: {old_path.name} → {new_path.name}")
        count += 1
    return count


def main():
    print("=== Phase 1: Find files with spaces ===")
    plan = find_files_with_spaces(WIKI_ROOT)
    print(f"Found {len(plan)} files to rename\n")

    if not plan:
        print("Nothing to do.")
        return

    # Show affected directories
    dirs = set()
    for old, _ in plan:
        dirs.add(old.parent.relative_to(WIKI_ROOT))
    print("Affected directories:")
    for d in sorted(dirs):
        print(f"  wiki/{d}/")
    print()

    # Show first 10 renames as sample
    print("Sample renames:")
    for old, new in plan[:10]:
        print(f"  {old.name} → {new.name}")
    print(f"  ... and {len(plan) - 10} more\n")

    # Phase 2: Update wikilinks FIRST (before renaming files)
    print("=== Phase 2: Update [[wikilinks]] ===")
    stats = update_references(plan, WIKI_ROOT)
    print(f"  Scanned: {stats['files_scanned']} files")
    print(f"  Links updated: {stats['links_updated']}")
    print(f"  Files modified: {stats['files_modified']}\n")

    # Phase 3: Rename files
    print("=== Phase 3: Rename files ===")
    count = execute_renames(plan)
    print(f"\n  Renamed: {count} files\n")

    # Summary
    print("=== Done ===")
    print(f"  Files renamed:  {count}")
    print(f"  Links updated:  {stats['links_updated']}")
    print(f"  Files touched:  {stats['files_modified']}")
    if count != len(plan):
        print(f"  WARNING: {len(plan) - count} files could not be renamed")


if __name__ == "__main__":
    main()
