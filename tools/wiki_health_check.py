#!/usr/bin/env python3
"""
wiki_health_check.py — LLM-Wiki 统一健康检查脚本

覆盖维度：
  - wiki 内 A 类真实断链数量
  - raw/wiki/outputs frontmatter 契约
  - 非标准 status/source_type
  - 重复来源卡
  - source_path 失效与 legacy 路径残留
  - 缺失附件引用
  - raw -> wiki/sources 覆盖率

用法：
  python3 tools/wiki_health_check.py
  python3 tools/wiki_health_check.py --json
  python3 tools/wiki_health_check.py --report
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_RAW_SOURCE_TYPES = {
    "web",
    "paper",
    "repo",
    "dataset",
    "image",
    "notes",
    "internal",
}
ALLOWED_RAW_STATUS = {"inbox", "summarized", "linked", "archived"}
ALLOWED_WIKI_STATUS = {"inbox", "summarized", "linked", "archived"}
ALLOWED_OUTPUT_STATUS = {"linked", "archived"}
LEGACY_PATH_PATTERNS = [
    "raw/web/deep-learning-theory",
    "raw/notes/deep-learning-theory",
    "raw/web/computer-vision",
    "raw/notes/computer-vision",
    "raw/web/tools",
    "raw/web/programming-tools",
    "wiki/sources/data-analysis",
]
ASSET_PATTERNS = [
    re.compile(r"!\[[^\]]*\]\(([^)]+)\)"),
    re.compile(r"\[\[(raw/assets/attachments/[^\]|#]+)"),
]
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)
RAW_REF_RE = re.compile(
    r"(raw/(?:web|papers|repos|datasets|images|notes|codex_threads|assets)/[^\s`)\]]+\.md)"
)

def normalize_name(value: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", value.lower())


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    block = match.group(1)
    data: dict[str, object] = {}
    current_key: str | None = None

    for line in block.splitlines():
        if re.match(r"^[A-Za-z0-9_\-]+:\s*", line):
            key, raw_value = line.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            if raw_value == "":
                data[key] = []
                current_key = key
            else:
                data[key] = raw_value.strip('"')
                current_key = None
            continue

        if current_key and re.match(r"^\s*-\s*", line):
            data.setdefault(current_key, []).append(
                re.sub(r"^\s*-\s*", "", line).strip().strip('"')
            )
            continue

        current_key = None

    return data


def extract_wikilinks(text: str) -> Iterable[tuple[str, str]]:
    for raw in WIKILINK_RE.findall(text):
        target = re.split(r"[\\]?\|", raw)[0].strip()
        target = target.split("#")[0].strip()
        if target:
            yield raw, target


def build_stem_map(wiki_root: Path) -> defaultdict[str, list[Path]]:
    stem_map: defaultdict[str, list[Path]] = defaultdict(list)
    for path in wiki_root.rglob("*.md"):
        if path.name == "log.md":
            continue
        stem = path.stem
        for key in {
            stem,
            stem.lower(),
            stem.replace("-", " "),
            stem.replace(" ", "-"),
            stem.replace("-", " ").lower(),
            stem.replace(" ", "-").lower(),
        }:
            stem_map[key].append(path)
    return stem_map


def classify_wikilink(
    repo_root: Path, target: str, stem_map: defaultdict[str, list[Path]]
) -> tuple[str, str]:
    if target.startswith("raw/") or target.startswith("outputs/"):
        return "C", "跨层路径"

    path_prefixes = (
        "wiki/",
        "sources/",
        "indexes/",
        "concepts/",
        "entities/",
        "comparisons/",
        "queries/",
    )
    if "/" in target and target.startswith(path_prefixes):
        rel = target if target.startswith("wiki/") else f"wiki/{target}"
        candidate = Path(rel if rel.endswith(".md") else f"{rel}.md")
        if (repo_root / candidate).exists():
            return "VALID", ""
        return "A4", "旧路径引用或路径式 wikilink"

    matches: list[Path] = []
    for key in {
        target,
        target.lower(),
        target.replace(" ", "-"),
        target.replace("-", " "),
        target.replace(" ", "-").lower(),
        target.replace("-", " ").lower(),
    }:
        matches.extend(stem_map.get(key, []))
    if matches:
        if any(path.stem == target for path in matches):
            return "VALID", ""
        return "A1", "文件存在但名称不匹配"
    if "/" in target:
        return "A4", "旧路径引用或路径式 wikilink"
    return "B", "内容缺口"


def scan_wiki_links(repo_root: Path) -> dict:
    wiki_root = repo_root / "wiki"
    if not wiki_root.exists():
        return {"counts": {"A": 0}, "issues": []}

    stem_map = build_stem_map(wiki_root)
    issues: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for path in sorted(wiki_root.rglob("*.md")):
        if path.name == "log.md":
            continue
        rel = path.relative_to(repo_root).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for raw, target in extract_wikilinks(text):
            key = (rel, raw)
            if key in seen:
                continue
            seen.add(key)
            class_key, note = classify_wikilink(repo_root, target, stem_map)
            if class_key in {"VALID", "B", "C"}:
                continue
            issues.append(
                {
                    "source": rel,
                    "target": target,
                    "wikilink": f"[[{raw}]]",
                    "class_key": class_key,
                    "note": note,
                }
            )

    return {
        "counts": {
            "A": sum(1 for issue in issues if issue["class_key"].startswith("A")),
            "A1": sum(1 for issue in issues if issue["class_key"] == "A1"),
            "A4": sum(1 for issue in issues if issue["class_key"] == "A4"),
        },
        "issues": issues,
    }


def should_check_raw_file(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    rel = path.as_posix()
    parts = path.parts
    if rel in {"raw/README.md", "raw/assets/README.md"}:
        return False
    if rel.startswith("raw/repos/") and len(parts) > 4:
        return False
    return True


def count_exempt_raw_repo_mirrors(repo_root: Path) -> int:
    count = 0
    raw_repos = repo_root / "raw" / "repos"
    if not raw_repos.exists():
        return 0
    for path in raw_repos.rglob("*.md"):
        rel = path.relative_to(repo_root)
        if not should_check_raw_file(rel):
            count += 1
    return count


def scan_frontmatter(repo_root: Path) -> dict:
    summary = {
        "raw_missing_frontmatter": 0,
        "raw_exempt_repo_mirror_files": count_exempt_raw_repo_mirrors(repo_root),
        "raw_missing_source_type": 0,
        "raw_missing_created_at": 0,
        "raw_missing_topics": 0,
        "wiki_missing_created_at": 0,
        "wiki_missing_topics": 0,
        "wiki_missing_status": 0,
        "output_missing_frontmatter": 0,
        "nonstandard_raw_source_type": 0,
        "nonstandard_raw_status": 0,
        "nonstandard_wiki_status": 0,
        "nonstandard_output_status": 0,
    }
    examples: defaultdict[str, list[str]] = defaultdict(list)

    for area in ("raw", "wiki", "outputs"):
        base = repo_root / area
        if not base.exists():
            continue

        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(repo_root).as_posix()
            if area == "raw" and not should_check_raw_file(Path(rel)):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            fm = parse_frontmatter(text)
            if not fm:
                if area == "raw":
                    summary["raw_missing_frontmatter"] += 1
                    summary["raw_missing_source_type"] += 1
                    summary["raw_missing_created_at"] += 1
                    summary["raw_missing_topics"] += 1
                    if len(examples["raw_missing_frontmatter"]) < 10:
                        examples["raw_missing_frontmatter"].append(rel)
                    for key in (
                        "raw_missing_source_type",
                        "raw_missing_created_at",
                        "raw_missing_topics",
                    ):
                        if len(examples[key]) < 10:
                            examples[key].append(rel)
                if area == "outputs":
                    summary["output_missing_frontmatter"] += 1
                    if len(examples["output_missing_frontmatter"]) < 10:
                        examples["output_missing_frontmatter"].append(rel)
                continue

            def is_missing(key: str) -> bool:
                value = fm.get(key)
                return key not in fm or value in ("", None) or (
                    isinstance(value, list) and not value
                )

            if area == "raw":
                for key, summary_key in {
                    "source_type": "raw_missing_source_type",
                    "created_at": "raw_missing_created_at",
                    "topics": "raw_missing_topics",
                }.items():
                    if is_missing(key):
                        summary[summary_key] += 1
                        if len(examples[summary_key]) < 10:
                            examples[summary_key].append(rel)

                source_type = fm.get("source_type")
                if isinstance(source_type, list):
                    source_type = "|".join(source_type)
                if source_type and source_type not in ALLOWED_RAW_SOURCE_TYPES:
                    summary["nonstandard_raw_source_type"] += 1
                    if len(examples["nonstandard_raw_source_type"]) < 10:
                        examples["nonstandard_raw_source_type"].append(rel)

                status = fm.get("status")
                if isinstance(status, list):
                    status = "|".join(status)
                if status and status not in ALLOWED_RAW_STATUS:
                    summary["nonstandard_raw_status"] += 1
                    if len(examples["nonstandard_raw_status"]) < 10:
                        examples["nonstandard_raw_status"].append(rel)

            elif area == "wiki":
                if is_missing("created_at") and is_missing("created"):
                    summary["wiki_missing_created_at"] += 1
                    if len(examples["wiki_missing_created_at"]) < 10:
                        examples["wiki_missing_created_at"].append(rel)

                if is_missing("topics") and is_missing("tags"):
                    summary["wiki_missing_topics"] += 1
                    if len(examples["wiki_missing_topics"]) < 10:
                        examples["wiki_missing_topics"].append(rel)

                if is_missing("status") and is_missing("type"):
                    summary["wiki_missing_status"] += 1
                    if len(examples["wiki_missing_status"]) < 10:
                        examples["wiki_missing_status"].append(rel)

                status = fm.get("status")
                if isinstance(status, list):
                    status = "|".join(status)
                if status and status not in ALLOWED_WIKI_STATUS:
                    summary["nonstandard_wiki_status"] += 1
                    if len(examples["nonstandard_wiki_status"]) < 10:
                        examples["nonstandard_wiki_status"].append(rel)

            else:
                status = fm.get("status")
                if isinstance(status, list):
                    status = "|".join(status)
                if status and status not in ALLOWED_OUTPUT_STATUS:
                    summary["nonstandard_output_status"] += 1
                    if len(examples["nonstandard_output_status"]) < 10:
                        examples["nonstandard_output_status"].append(rel)

    return {"summary": summary, "examples": dict(examples)}


def scan_duplicate_source_cards(repo_root: Path) -> dict:
    source_root = repo_root / "wiki" / "sources"
    same_dir_groups: list[list[str]] = []
    cross_topic_groups: list[list[str]] = []
    normalized_groups: defaultdict[str, list[str]] = defaultdict(list)

    if source_root.exists():
        for path in source_root.rglob("*.md"):
            if path.name == "index.md":
                continue
            normalized_groups[normalize_name(path.stem)].append(
                path.relative_to(repo_root).as_posix()
            )

    for paths in normalized_groups.values():
        if len(paths) > 1:
            sorted_paths = sorted(paths)
            dirs = {str(Path(rel).parent) for rel in sorted_paths}
            if len(dirs) == 1:
                same_dir_groups.append(sorted_paths)
            else:
                cross_topic_groups.append(sorted_paths)

    return {
        "group_count": len(same_dir_groups),
        "file_count": sum(len(group) for group in same_dir_groups),
        "groups": same_dir_groups,
        "cross_topic_group_count": len(cross_topic_groups),
        "cross_topic_groups": cross_topic_groups,
    }


def scan_source_paths_and_coverage(repo_root: Path) -> dict:
    raw_root = repo_root / "raw"
    source_root = repo_root / "wiki" / "sources"
    raw_files: list[str] = []
    raw_to_card: defaultdict[str, list[str]] = defaultdict(list)
    invalid_source_path: list[dict] = []
    missing_raw_reference: list[str] = []

    if raw_root.exists():
        for path in raw_root.rglob("*.md"):
            rel = path.relative_to(repo_root).as_posix()
            if not should_check_raw_file(Path(rel)):
                continue
            raw_files.append(rel)

    if source_root.exists():
        for path in source_root.rglob("*.md"):
            rel = path.relative_to(repo_root).as_posix()
            text = path.read_text(encoding="utf-8", errors="ignore")
            fm = parse_frontmatter(text)
            refs: list[str] = []

            raw_source_path = fm.get("source_path")
            if isinstance(raw_source_path, str) and raw_source_path.startswith("raw/"):
                refs.append(raw_source_path)

            raw_sources = fm.get("sources", [])
            if isinstance(raw_sources, str):
                raw_sources = [raw_sources]
            refs.extend(ref for ref in raw_sources if isinstance(ref, str) and ref.startswith("raw/"))
            refs.extend(RAW_REF_RE.findall(text))

            deduped_refs = sorted(set(refs))
            thematic_page = (
                "专题来源" in path.name
                or "附件入口清单" in path.name
                or path.name in {"NLP本地笔记.md", "大语言模型本地笔记.md"}
            )
            if not deduped_refs and path.name != "index.md" and not thematic_page:
                missing_raw_reference.append(rel)

            valid_refs = []
            for ref in deduped_refs:
                target = repo_root / ref
                if target.exists():
                    valid_refs.append(ref)
                    raw_to_card[ref].append(rel)
                else:
                    invalid_source_path.append({"source_card": rel, "target": ref})

    raw_without_source_card = [
        rel for rel in sorted(set(raw_files)) if not raw_to_card.get(rel)
    ]

    return {
        "invalid_source_path_count": len(invalid_source_path),
        "invalid_source_paths": invalid_source_path,
        "missing_raw_reference_count": len(missing_raw_reference),
        "missing_raw_reference_examples": missing_raw_reference[:20],
        "raw_exempt_repo_mirror_files": count_exempt_raw_repo_mirrors(repo_root),
        "raw_without_source_card": len(raw_without_source_card),
        "raw_without_source_card_examples": raw_without_source_card[:50],
    }


def resolve_asset_target(repo_root: Path, source_file: Path, ref: str) -> Path | None:
    if ref.startswith("http://") or ref.startswith("https://"):
        return None
    ref = ref.replace("%20", " ")
    if ref.startswith("raw/assets/"):
        return repo_root / ref
    if ref.startswith("./") or ref.startswith("../") or ref.startswith("images/"):
        return (source_file.parent / ref).resolve()
    if ref.startswith("/"):
        return Path(ref)
    return None


def scan_missing_assets(repo_root: Path) -> dict:
    missing_by_file: defaultdict[str, list[str]] = defaultdict(list)
    for path in repo_root.rglob("*.md"):
        rel = path.relative_to(repo_root).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        refs: list[str] = []
        for pattern in ASSET_PATTERNS:
            refs.extend(match.group(1).strip() for match in pattern.finditer(text))
        for ref in refs:
            target = resolve_asset_target(repo_root, path, ref)
            if target is None:
                continue
            if not target.exists():
                missing_by_file[rel].append(ref)

    flattened = [
        {"source": source, "ref": ref}
        for source, refs in missing_by_file.items()
        for ref in refs
    ]
    return {
        "files_with_missing_assets": len(missing_by_file),
        "missing_reference_count": len(flattened),
        "top_files": [
            {"source": source, "count": len(refs), "refs": refs[:10]}
            for source, refs in sorted(
                missing_by_file.items(), key=lambda item: (-len(item[1]), item[0])
            )[:20]
        ],
    }


def scan_legacy_paths(repo_root: Path) -> dict:
    hits: defaultdict[str, list[str]] = defaultdict(list)
    scan_paths = [repo_root / "raw", repo_root / "wiki", repo_root / "outputs"]
    for pattern in LEGACY_PATH_PATTERNS:
        for base in scan_paths:
            if not base.exists():
                continue
            for path in base.rglob("*.md"):
                text = path.read_text(encoding="utf-8", errors="ignore")
                if pattern in text:
                    hits[pattern].append(path.relative_to(repo_root).as_posix())
    return {
        "pattern_count": len(hits),
        "patterns": {key: value[:20] for key, value in sorted(hits.items())},
    }


def scan_repo(repo_root: Path) -> dict:
    link_summary = scan_wiki_links(repo_root)
    frontmatter = scan_frontmatter(repo_root)
    duplicates = scan_duplicate_source_cards(repo_root)
    coverage = scan_source_paths_and_coverage(repo_root)
    assets = scan_missing_assets(repo_root)
    legacy_paths = scan_legacy_paths(repo_root)

    return {
        "repo_root": str(repo_root),
        "generated_at": date.today().isoformat(),
        "counts": {
            "wiki_broken_links_a": link_summary["counts"]["A"],
            "wiki_broken_links_a1": link_summary["counts"]["A1"],
            "wiki_broken_links_a4": link_summary["counts"]["A4"],
        },
        "link_issues": link_summary["issues"],
        "frontmatter": {**frontmatter["summary"], "examples": frontmatter["examples"]},
        "duplicate_source_cards": duplicates,
        "coverage": coverage,
        "missing_assets": assets,
        "legacy_paths": legacy_paths,
    }


def build_markdown_report(summary: dict) -> str:
    today = summary["generated_at"]
    frontmatter = summary["frontmatter"]
    coverage = summary["coverage"]
    duplicates = summary["duplicate_source_cards"]
    assets = summary["missing_assets"]
    legacy = summary["legacy_paths"]

    lines = [
        "---",
        f"created_at: {today}",
        "topics:",
        "  - 知识库维护",
        "  - 健康检查",
        "status: linked",
        "---",
        "",
        "# Wiki Health Check Report",
        "",
        f"> 生成时间：{today}",
        "",
        "## 核心指标",
        "",
        f"- A 类真实断链：{summary['counts']['wiki_broken_links_a']}",
        f"- raw 缺 frontmatter：{frontmatter['raw_missing_frontmatter']}",
        f"- raw 缺 source_type：{frontmatter['raw_missing_source_type']}",
        f"- wiki 缺 created_at：{frontmatter['wiki_missing_created_at']}",
        f"- 非标准 raw source_type：{frontmatter['nonstandard_raw_source_type']}",
        f"- 非标准 raw status：{frontmatter['nonstandard_raw_status']}",
        f"- 非标准 output status：{frontmatter['nonstandard_output_status']}",
        f"- 重复来源卡组：{duplicates['group_count']}",
        f"- 失效 source_path：{coverage['invalid_source_path_count']}",
        f"- 无源卡 raw 文件：{coverage['raw_without_source_card']}",
        f"- 缺失附件引用：{assets['missing_reference_count']}",
        "",
        "## Legacy Path 残留",
        "",
        f"- legacy pattern 命中：{legacy['pattern_count']}",
    ]

    if duplicates["groups"]:
        lines.extend(["", "## 重复来源卡示例", ""])
        for group in duplicates["groups"][:10]:
            lines.append(f"- {' | '.join(group)}")

    if coverage["invalid_source_paths"]:
        lines.extend(["", "## 失效 source_path 示例", ""])
        for item in coverage["invalid_source_paths"][:10]:
            lines.append(f"- {item['source_card']} -> `{item['target']}`")

    if assets["top_files"]:
        lines.extend(["", "## 缺失附件 Top Files", ""])
        for item in assets["top_files"][:10]:
            lines.append(f"- {item['source']} ({item['count']})")

    return "\n".join(lines) + "\n"


def print_summary(summary: dict) -> None:
    frontmatter = summary["frontmatter"]
    coverage = summary["coverage"]
    duplicates = summary["duplicate_source_cards"]
    assets = summary["missing_assets"]

    print("=" * 60)
    print("wiki_health_check.py — 统一健康检查")
    print("=" * 60)
    print(f"A 类真实断链: {summary['counts']['wiki_broken_links_a']}")
    print(
        "frontmatter: "
        f"raw缺frontmatter={frontmatter['raw_missing_frontmatter']}, "
        f"raw缺source_type={frontmatter['raw_missing_source_type']}, "
        f"wiki缺created_at={frontmatter['wiki_missing_created_at']}, "
        f"非标准raw status={frontmatter['nonstandard_raw_status']}, "
        f"非标准output status={frontmatter['nonstandard_output_status']}"
    )
    print(
        "source/raw: "
        f"失效source_path={coverage['invalid_source_path_count']}, "
        f"raw无源卡={coverage['raw_without_source_card']}, "
        f"缺raw引用来源卡={coverage['missing_raw_reference_count']}"
    )
    print(
        "其他: "
        f"重复来源卡组={duplicates['group_count']}, "
        f"缺失附件引用={assets['missing_reference_count']}, "
        f"legacy pattern={summary['legacy_paths']['pattern_count']}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="LLM-Wiki 统一健康检查")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--report", action="store_true", help="写入 Markdown 报告")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="仓库根目录，默认当前仓库",
    )
    args = parser.parse_args()

    summary = scan_repo(args.repo_root.resolve())

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_summary(summary)

    if args.report:
        report_path = args.repo_root / "outputs" / "logs" / "wiki-health-check-report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(build_markdown_report(summary), encoding="utf-8")
        print(f"\n报告已写入: {report_path.relative_to(args.repo_root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
