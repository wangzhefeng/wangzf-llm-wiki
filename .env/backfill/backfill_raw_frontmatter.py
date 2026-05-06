#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "raw"


DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
YAML_KEY_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")
RAW_TYPE_MAP: list[tuple[str, str]] = [
    ("raw/web/", "web"),
    ("raw/papers/", "paper"),
    ("raw/repos/", "repo"),
    ("raw/datasets/", "dataset"),
    ("raw/images/", "image"),
    ("raw/local-notes/", "local_note"),
    ("raw/codex_threads/", "local_note"),
]


@dataclass(frozen=True)
class PatchResult:
    path: Path
    added_keys: tuple[str, ...]


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


def parse_frontmatter_lines(lines: list[str]) -> dict[str, object]:
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


def infer_created_at(path: Path, fm: dict[str, object]) -> str | None:
    for k in ("created_at", "date", "created", "published_at", "updated"):
        v = fm.get(k)
        if isinstance(v, str):
            m = DATE_RE.search(v)
            if m:
                return m.group(1)
    # 从路径中提取（常见：raw/local-notes/<topic>/YYYY-MM-DD-xxx/index.md）
    m = DATE_RE.search(path.as_posix())
    return m.group(1) if m else None


def infer_topics(path: Path, fm: dict[str, object]) -> list[str] | None:
    v = fm.get("topics")
    if isinstance(v, list) and v:
        return [str(x).strip() for x in v if str(x).strip()][:3]
    # 兼容历史字段：categories/tags
    for k in ("categories", "category", "tags", "tag"):
        v2 = fm.get(k)
        if isinstance(v2, list) and v2:
            return [str(x).strip() for x in v2 if str(x).strip()][:3]
        if isinstance(v2, str) and v2.strip():
            return [v2.strip()]
    # 最后从 raw 子目录推断：
    # - raw/web/<topic>/... -> <topic>
    # - raw/local-notes/<topic>/... -> <topic>
    # - 其他 -> raw/<kind> 作为兜底
    try:
        rel = path.relative_to(RAW_ROOT).parts
    except ValueError:
        return None
    if rel:
        if rel[0] in {"web", "local-notes"} and len(rel) >= 2 and rel[1]:
            return [rel[1]]
        return [rel[0]]
    return None


def infer_source_type(path: Path, fm: dict[str, object]) -> str | None:
    v = fm.get("source_type")
    if isinstance(v, str) and v.strip():
        return v.strip()
    rel = path.relative_to(ROOT).as_posix()
    for prefix, st in RAW_TYPE_MAP:
        if rel.startswith(prefix):
            return st
    return None


def ensure_min_frontmatter(path: Path, text: str) -> tuple[str, tuple[str, ...]] | None:
    if path.name in {"README.md", "_index.md"}:
        return None

    fm_lines, body_lines = split_frontmatter(text)
    fm = parse_frontmatter_lines(fm_lines)

    missing: list[str] = []
    if "source_type" not in fm:
        missing.append("source_type")
    if "created_at" not in fm:
        missing.append("created_at")
    if "topics" not in fm:
        missing.append("topics")
    if "status" not in fm:
        missing.append("status")

    # 仅当 topics 已存在且 >3 时做截断（按仓库约定 topics 1~3 个）
    topics_truncated = False
    if "topics" in fm and isinstance(fm.get("topics"), list) and len(fm.get("topics", [])) > 3:
        fm["topics"] = list(fm.get("topics", []))[:3]
        topics_truncated = True
        if "topics_truncated" not in missing:
            missing.append("topics_truncated")

    if not missing:
        return None

    created_at = infer_created_at(path, fm)
    topics = infer_topics(path, fm)
    source_type = infer_source_type(path, fm)

    insert_lines: list[str] = []
    if "source_type" in missing:
        insert_lines.append(f"source_type: {source_type or 'local_note'}\n")
    if "created_at" in missing:
        if not created_at:
            # 不要瞎填时间戳：无法推断则交给人工处理
            return None
        insert_lines.append(f"created_at: {created_at}\n")
    if "topics" in missing:
        insert_lines.append("topics:\n")
        for t in (topics or ["local_note"])[:3]:
            insert_lines.append(f"  - {t}\n")
    if "status" in missing:
        insert_lines.append("status: inbox\n")

    # 若需要截断 topics，则在 frontmatter 内原地替换 topics block（保持其它字段不动）
    if topics_truncated and fm_lines:
        new_fm_lines: list[str] = []
        i = 0
        while i < len(fm_lines):
            line = fm_lines[i]
            m = YAML_KEY_RE.match(line.rstrip("\n"))
            if m and m.group(1) == "topics":
                # consume existing topics block
                new_fm_lines.append("topics:\n")
                for t in fm.get("topics", []):
                    new_fm_lines.append(f"  - {t}\n")
                i += 1
                while i < len(fm_lines) and fm_lines[i].lstrip().startswith("- "):
                    i += 1
                continue
            new_fm_lines.append(line if line.endswith("\n") else (line + "\n"))
            i += 1
        fm_lines = new_fm_lines
        # 标记只是为了报告，不实际写入这个 key
        missing = [k for k in missing if k != "topics_truncated"]

    # 若已有 frontmatter，则在末尾追加缺失字段；否则创建新的 frontmatter。
    if fm_lines:
        new_fm_lines = [*fm_lines]
        if not new_fm_lines[-1].endswith("\n"):
            new_fm_lines[-1] = new_fm_lines[-1] + "\n"
        new_fm_lines.extend(insert_lines)
        new_text = "".join(["---\n", *new_fm_lines, "---\n", *body_lines])
        return new_text, tuple([k for k in missing if k != "topics_truncated"])

    new_text = "".join(["---\n", *insert_lines, "---\n", *body_lines])
    return new_text, tuple([k for k in missing if k != "topics_truncated"])


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill minimal raw frontmatter fields.")
    ap.add_argument("--apply", action="store_true", help="Write changes to disk.")
    ap.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max files to modify (0 = no limit).",
    )
    args = ap.parse_args()

    results: list[PatchResult] = []
    for p in md_files(RAW_ROOT):
        text = p.read_text(encoding="utf-8")
        out = ensure_min_frontmatter(p, text)
        if out is None:
            continue
        new_text, added = out
        results.append(PatchResult(path=p, added_keys=added))
        if args.limit and len(results) >= args.limit:
            break

    if not results:
        print("No changes needed.")
        return 0

    print(f"Candidates: {len(results)}")
    for r in results[:20]:
        rel = r.path.relative_to(ROOT).as_posix()
        print(f"- {rel} add: {', '.join(r.added_keys)}")
    if len(results) > 20:
        print(f"... ({len(results) - 20} more)")

    if args.apply:
        for r in results:
            p = r.path
            text = p.read_text(encoding="utf-8")
            out = ensure_min_frontmatter(p, text)
            if out is None:
                continue
            new_text, _ = out
            p.write_text(new_text, encoding="utf-8")
        print("Applied.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
