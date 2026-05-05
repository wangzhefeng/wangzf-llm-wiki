#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATT = ROOT / "raw" / "assets" / "attachments"


def move_dir(src: Path, dst: Path, apply: bool) -> int:
    if not src.exists():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    moved = 0
    for p in sorted([x for x in src.iterdir() if x.is_file()]):
        target = dst / p.name
        if target.exists():
            # 若重名，保留目标，源放入 _dups
            dups = dst / "_dups"
            dups.mkdir(parents=True, exist_ok=True)
            target = dups / p.name
        if apply:
            shutil.move(str(p), str(target))
        moved += 1
    return moved


def move_files(src_files: list[Path], dst_dir: Path, apply: bool) -> int:
    dst_dir.mkdir(parents=True, exist_ok=True)
    moved = 0
    for p in src_files:
        if not p.exists() or not p.is_file():
            continue
        target = dst_dir / p.name
        if target.exists():
            dups = dst_dir / "_dups"
            dups.mkdir(parents=True, exist_ok=True)
            target = dups / p.name
        if apply:
            shutil.move(str(p), str(target))
        moved += 1
    return moved


def main() -> int:
    ap = argparse.ArgumentParser(description="Organize leftover assets under raw/assets/attachments.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    # 1) uncategorized leftovers (unreferenced)
    uncat = ATT / "uncategorized"
    dst_uncat = ATT / "shared" / "uncategorized"
    moved_uncat = move_dir(uncat, dst_uncat, apply=args.apply)

    # 2) latex leftovers in attachments root
    latex_files = [ATT / "gif 1.latex", ATT / "gif 2.latex", ATT / "gif.latex"]
    dst_latex = ATT / "shared" / "latex"
    moved_latex = move_files(latex_files, dst_latex, apply=args.apply)

    print(f"uncategorized moved: {moved_uncat}")
    print(f"latex moved: {moved_latex}")
    if args.apply:
        print("Applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

