#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATT_ROOT = ROOT / "raw" / "assets" / "attachments"
WIKI_SOURCES = ROOT / "wiki" / "sources"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]*)?(?:\|[^\]]*)?\]\]")


DIR_TO_SOURCES_TOPIC = {
    "computer-vision": "computervision",
    "machine-learning": "machinelearning",
    "reinforcement-learning": "reinforcementlearning",
    "data-structure-algorithm": "data_structure_algorithm",
    "control-algorithms": "control_algorithms",
    "knowledge-base": "knowledge-base",
}


def md_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*.md") if p.is_file()])


def collect_refs() -> set[str]:
    refs: set[str] = set()
    for base in (ROOT / "raw", ROOT / "wiki", ROOT / "outputs"):
        for p in md_files(base):
            txt = p.read_text(encoding="utf-8", errors="ignore")
            for t in WIKILINK_RE.findall(txt):
                if t.startswith("raw/assets/attachments/"):
                    refs.add(t.strip())
    return refs


def list_attachment_files() -> list[Path]:
    if not ATT_ROOT.exists():
        return []
    return sorted([p for p in ATT_ROOT.rglob("*") if p.is_file()])


def topic_for_attachment(path: Path) -> str:
    rel = path.relative_to(ATT_ROOT).as_posix()
    if "/" not in rel:
        return "attachments-root"
    parts = rel.split("/", 1)
    top = parts[0]
    return DIR_TO_SOURCES_TOPIC.get(top, top)


def render_page(topic: str, label: str, files: list[Path]) -> str:
    lines: list[str] = []
    lines.append("---\n")
    lines.append(f"source_type: local_note\n")
    lines.append(f"title: {label} 附件入口清单\n")
    lines.append("created_at: 2026-04-11\n")
    lines.append("topics:\n")
    lines.append(f"  - {topic}\n")
    lines.append("  - assets\n")
    lines.append("status: linked\n")
    lines.append("---\n\n")
    lines.append(f"# 附件入口清单（{label}）\n\n")
    lines.append("> 目的：为 `raw/assets/attachments/` 中暂未被引用的附件提供可追溯入口，避免成为“暗资产”。\n\n")
    lines.append("## 清单\n\n")
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        # 以 wikilink 形式建立最小引用；图片可被 Obsidian 渲染
        lines.append(f"- [[{rel}]]\n")
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Create wiki/sources entry pages for unreferenced attachments.")
    ap.add_argument("--apply", action="store_true", help="Write pages to disk.")
    args = ap.parse_args()

    refs = collect_refs()
    unref: list[Path] = []
    for p in list_attachment_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel not in refs:
            unref.append(p)

    groups: dict[str, list[Path]] = defaultdict(list)
    for p in unref:
        groups[topic_for_attachment(p)].append(p)

    plans: list[tuple[Path, str, int]] = []
    for topic, items in sorted(groups.items()):
        if topic in {"_dups"}:
            continue
        label = topic

        # attachments 根目录的杂项统一归到 shared（label 保留）
        dest_topic = topic
        rel0 = items[0].relative_to(ATT_ROOT).as_posix()
        if topic == "attachments-root":
            dest_topic = "shared"

        out_dir = WIKI_SOURCES / dest_topic
        if not out_dir.exists():
            out_dir = WIKI_SOURCES / "shared"
            dest_topic = "shared"

        safe_label = label.replace("/", "-")
        out_path = out_dir / f"附件入口清单-{safe_label}.md"
        content = render_page(dest_topic, label, sorted(items))
        plans.append((out_path, content, len(items)))

    print(f"Unreferenced attachments: {len(unref)}")
    for out_path, _, n in plans:
        print(f"- {out_path.relative_to(ROOT)}: {n} assets")

    if args.apply:
        for out_path, content, _ in plans:
            out_path.write_text(content, encoding="utf-8")
        print("Applied.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
