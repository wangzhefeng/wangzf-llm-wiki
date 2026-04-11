#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATT_ROOT = ROOT / "raw" / "assets" / "attachments"
UNCAT_DIR = ATT_ROOT / "uncategorized"

WIKILINK_RE = re.compile(
    r"\[\[\s*(?P<path>raw/assets/attachments/uncategorized/[^\]|#]+)\s*(?P<rest>(?:#[^\]]*)?(?:\|[^\]]*)?)\s*\]\]"
)


TOPIC_DIR_MAP = {
    "computer-vision": "computer-vision",
    "machinelearning": "machine-learning",
    "reinforcementlearning": "reinforcement-learning",
    "data-structure-algorithm": "data-structure-algorithm",
    "data-structure-algorithm": "data-structure-algorithm",
    "control_algorithms": "control-algorithms",
    "control-algorithms": "control-algorithms",
    "knowledge-base-building": "knowledge-base-building",
}


@dataclass(frozen=True)
class MovePlan:
    src_rel: str
    dst_rel: str
    topics: tuple[str, ...]


def md_files() -> list[Path]:
    bases = [ROOT / "raw", ROOT / "wiki", ROOT / "outputs"]
    out: list[Path] = []
    for b in bases:
        if not b.exists():
            continue
        out.extend([p for p in b.rglob("*.md") if p.is_file()])
    return sorted(out)


def detect_topic(md_path: Path) -> str:
    rel = md_path.relative_to(ROOT).as_posix()
    parts = Path(rel).parts
    if parts[:2] == ("raw", "web") and len(parts) >= 3:
        return parts[2]
    if parts[:2] == ("wiki", "concepts") and len(parts) >= 3:
        return parts[2]
    if parts[:2] == ("wiki", "sources") and len(parts) >= 3:
        return parts[2]
    return "misc"


def map_topic_dir(topic: str) -> str:
    if topic in TOPIC_DIR_MAP:
        return TOPIC_DIR_MAP[topic]
    return topic.replace("_", "-")


def collect_uncat_refs() -> dict[str, set[str]]:
    refs: dict[str, set[str]] = defaultdict(set)
    for p in md_files():
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for m in WIKILINK_RE.finditer(txt):
            rel_path = m.group("path").strip()
            refs[rel_path].add(detect_topic(p))
    return refs


def plan_moves(refs: dict[str, set[str]]) -> list[MovePlan]:
    plans: list[MovePlan] = []
    for src_rel, topics in sorted(refs.items()):
        if len(topics) != 1:
            continue
        topic = next(iter(topics))
        src_path = ROOT / src_rel
        if not src_path.exists():
            continue
        dst_dir = ATT_ROOT / map_topic_dir(topic)
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_rel = (dst_dir / src_path.name).relative_to(ROOT).as_posix()
        plans.append(MovePlan(src_rel=src_rel, dst_rel=dst_rel, topics=tuple(sorted(topics))))
    return plans


def apply_moves(plans: list[MovePlan], apply: bool) -> None:
    # 1) move files
    if apply:
        for it in plans:
            src = ROOT / it.src_rel
            dst = ROOT / it.dst_rel
            if not src.exists():
                continue
            if dst.exists():
                # 若目标已存在但内容可能一致，优先保留目标，备份源到 _dups
                dups = ATT_ROOT / "_dups"
                dups.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dups / src.name))
                continue
            shutil.move(str(src), str(dst))

    # 2) rewrite markdown references
    mapping = {it.src_rel: it.dst_rel for it in plans}
    if not mapping:
        return

    for p in md_files():
        txt = p.read_text(encoding="utf-8", errors="ignore")

        def repl(m: re.Match[str]) -> str:
            path = m.group("path").strip()
            rest = m.group("rest") or ""
            new_path = mapping.get(path)
            if not new_path:
                return m.group(0)
            return f"[[{new_path}{rest}]]"

        new_txt = WIKILINK_RE.sub(repl, txt)
        if apply and new_txt != txt:
            p.write_text(new_txt, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Migrate raw/assets/attachments/uncategorized/* into topic dirs.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk (move + rewrite).")
    args = ap.parse_args()

    if not UNCAT_DIR.exists():
        print("No uncategorized directory.")
        return 0

    refs = collect_uncat_refs()
    plans = plan_moves(refs)
    print(f"Planned moves: {len(plans)} (from {len(refs)} referenced assets)")
    for it in plans[:30]:
        print(f"- {it.src_rel} -> {it.dst_rel} (topic: {', '.join(it.topics)})")
    if len(plans) > 30:
        print(f"... ({len(plans) - 30} more)")

    apply_moves(plans, apply=args.apply)
    if args.apply:
        print("Applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
