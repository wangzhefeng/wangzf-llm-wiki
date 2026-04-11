#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_LOCAL_NOTES = ROOT / "raw" / "local-notes"


THEME_TO_WIKI_INDEX = {
    "analysis": "wiki/indexes/analysis/数据分析总索引.md",
    "timeseries": "wiki/indexes/timeseries/时间序列预测总索引.md",
    "control-algorithms": "wiki/indexes/control-algorithms/控制算法总索引.md",
    "control_algorithms": "wiki/indexes/control-algorithms/控制算法总索引.md",
    "data-structure-algorithm": "wiki/indexes/data_structure_algorithm/数据结构与算法总索引.md",
    "data_structure_algorithm": "wiki/indexes/data_structure_algorithm/数据结构与算法总索引.md",
    "machinelearning": "wiki/indexes/machinelearning/机器学习总索引.md",
    "deeplearning": "wiki/indexes/deeplearning/深度学习总索引.md",
    "operationsresearch": "wiki/indexes/operationsresearch/运筹优化算法总索引.md",
    "llm": "wiki/indexes/llm/大语言模型总索引.md",
    "nlp": "wiki/indexes/llm/大语言模型总索引.md",
    "cv": "wiki/indexes/computervision/计算机视觉总索引.md",
    "post": "wiki/indexes/knowledge-base-operations/知识库工作台.md",
    "knowledge-base": "wiki/indexes/knowledge-base-building/知识库建设方法总索引.md",
}


@dataclass(frozen=True)
class Change:
    path: Path


def md_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("_index.md") if p.is_file()])


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[: end + 5], text[end + 5 :]


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill wikilinks from raw/local-notes/**/_index.md to wiki theme indexes.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = ap.parse_args()

    changes: list[Change] = []
    for p in md_files(RAW_LOCAL_NOTES):
        rel = p.relative_to(ROOT).as_posix()
        parts = p.relative_to(RAW_LOCAL_NOTES).parts
        if not parts:
            continue
        theme = parts[0]
        wiki_index = THEME_TO_WIKI_INDEX.get(theme)
        if not wiki_index:
            continue
        target = wiki_index[:-3] if wiki_index.endswith(".md") else wiki_index
        text = p.read_text(encoding="utf-8", errors="ignore")
        fm, body = split_frontmatter(text)
        if f"[[{target}]]" in text:
            continue
        insert = f"\n\n- Wiki 入口：[[{target}]]\n"
        new_text = fm + body.rstrip() + insert
        changes.append(Change(path=p))
        if args.apply:
            p.write_text(new_text, encoding="utf-8")

    print(f"Changed files: {len(changes)}")
    for c in changes[:30]:
        print(f"- {c.path.relative_to(ROOT).as_posix()}")
    if len(changes) > 30:
        print(f"... ({len(changes) - 30} more)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
