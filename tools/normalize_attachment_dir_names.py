#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATT = ROOT / "raw" / "assets" / "attachments"


DIR_RENAMES = {
    "computer-vision": "computervision",
    "machine-learning": "machinelearning",
    "reinforcement-learning": "reinforcementlearning",
    "data_structure_algorithm": "data-structure-algorithm",
    "data-structure-algorithm": "data-structure-algorithm",
    "control_algorithms": "control-algorithms",
    "control-algorithms": "control-algorithms",
}


@dataclass(frozen=True)
class Change:
    src: Path
    dst: Path


def md_files() -> list[Path]:
    bases = [ROOT / "raw", ROOT / "wiki", ROOT / "outputs"]
    out: list[Path] = []
    for b in bases:
        if not b.exists():
            continue
        out.extend([p for p in b.rglob("*.md") if p.is_file()])
    return sorted(out)


def build_changes() -> list[Change]:
    changes: list[Change] = []
    for src_name, dst_name in DIR_RENAMES.items():
        src = ATT / src_name
        dst = ATT / dst_name
        if src.exists():
            changes.append(Change(src=src, dst=dst))
    return changes


def apply_dir_moves(changes: list[Change], apply: bool) -> None:
    for ch in changes:
        if ch.dst.exists():
            # 合并：dst 已存在则把 src 下文件并入 dst/_merge
            merge = ch.dst / "_merge"
            merge.mkdir(parents=True, exist_ok=True)
            for p in sorted([x for x in ch.src.rglob("*") if x.is_file()]):
                rel = p.relative_to(ch.src)
                target = merge / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if apply:
                    shutil.move(str(p), str(target))
            if apply:
                # 清理空目录
                for d in sorted([x for x in ch.src.rglob("*") if x.is_dir()], reverse=True):
                    try:
                        d.rmdir()
                    except OSError:
                        pass
                try:
                    ch.src.rmdir()
                except OSError:
                    pass
            continue

        if apply:
            shutil.move(str(ch.src), str(ch.dst))


def rewrite_markdown(changes: list[Change], apply: bool) -> int:
    if not changes:
        return 0
    mapping: dict[str, str] = {}
    for ch in changes:
        mapping[ch.src.relative_to(ROOT).as_posix() + "/"] = ch.dst.relative_to(ROOT).as_posix() + "/"

    touched = 0
    for p in md_files():
        txt = p.read_text(encoding="utf-8", errors="ignore")
        new = txt
        for a, b in mapping.items():
            new = new.replace(a, b)
        if new != txt:
            touched += 1
            if apply:
                p.write_text(new, encoding="utf-8")
    return touched


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize raw/assets/attachments topic directory names to wiki topic slugs.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    changes = build_changes()
    if not changes:
        print("No directories to rename.")
        return 0

    print("Planned renames:")
    for ch in changes:
        print(f"- {ch.src.relative_to(ROOT)} -> {ch.dst.relative_to(ROOT)}")

    files = rewrite_markdown(changes, apply=False)
    print(f"Markdown files to rewrite: {files}")

    if args.apply:
        apply_dir_moves(changes, apply=True)
        rewritten = rewrite_markdown(changes, apply=True)
        print(f"Rewritten: {rewritten}")
        print("Applied.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
