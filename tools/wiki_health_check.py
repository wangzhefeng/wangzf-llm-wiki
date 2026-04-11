#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = ROOT / "wiki"
RAW_ROOT = ROOT / "raw"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]]*)?(?:\|[^\]]*)?\]\]")
ATTACHMENT_PATH_RE = re.compile(r"raw/assets/attachments/[A-Za-z0-9_./% ()-]+\.[A-Za-z0-9]+")

# 允许存在于模板/指引类文本中的“占位链接”，不计入断链
IGNORE_WIKILINK_TARGETS = {
    "某个总索引",
    "某个概念页",
    "某个来源卡",
    "某篇结果页",
}

# 这些目录下的页面通常是导航/工作流页，孤页风险较低，默认不计为 orphan
ORPHAN_EXCLUDE_DIR_PREFIXES = {
    "wiki/indexes/",
    "wiki/concepts/autofix/",
    "wiki/sources/autofix/",
}

RAW_NAMING_ALLOWLIST = {
    "raw/codex_threads/线程总结模板.md",
    "raw/local-notes/时间序列预测-历史文档清单.md",
    "raw/local-notes/深度学习-历史文档清单.md",
    "raw/local-notes/知识库建设方法-历史文档清单.md",
    "raw/local-notes/运筹优化算法-历史文档清单.md",
    "raw/repos/repo-wangzhefeng-tsproj-ml.md",
}

RAW_DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
RAW_REPO_CARD_RE = re.compile(r"^repo-[A-Za-z0-9_.-]+-[A-Za-z0-9_.-]+\.md$")


@dataclass(frozen=True)
class FrontmatterCheck:
    path: Path
    missing_keys: tuple[str, ...]


def md_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*.md") if p.is_file()])


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5 :]
    fm: dict[str, object] = {}
    key: str | None = None
    for line in fm_raw.splitlines():
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            v = m.group(2).strip()
            fm[key] = [] if v == "" else v
            continue
        if line.strip().startswith("- ") and key and isinstance(fm.get(key), list):
            fm[key] = [*fm.get(key, []), line.strip()[2:].strip()]
    return fm, body


def build_wiki_stem_index() -> dict[str, Path]:
    idx: dict[str, Path] = {}
    for p in md_files(WIKI_ROOT):
        idx[p.stem] = p
    return idx


def resolve_wikilink_target(target: str, stems: dict[str, Path]) -> Path | None:
    t = target.strip()
    if not t:
        return None
    # 支持 raw 路径式 wikilink：[[raw/web/xx/2026-...]]（Obsidian 图谱需要显式 raw 互链）
    if t.startswith("raw/"):
        # 若显式给了“常见文件扩展名”，按原样检查；否则默认补 .md。
        # 注意：文件名中可能包含类似 `xxx.md at main` 的点号片段，不能用 Path.suffix 的存在性直接判断。
        known_exts = {
            ".md",
            ".pdf",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".webp",
            ".mp4",
            ".mov",
        }
        suffix = Path(t).suffix.lower()
        cand = ROOT / t if suffix in known_exts else ROOT / (t + ".md")
        if cand.exists():
            return cand
        return None
    # 支持路径式 wikilink：[[wiki/sources/analysis/README]] 或 [[sources/analysis/README]]
    if "/" in t:
        rel = t
        if rel.startswith("wiki/"):
            rel = rel[len("wiki/") :]
        # 注意：Path.with_suffix 会把路径中“最后一个点号后的内容”当成后缀，
        # 而本仓库文件名里常含有类似 `10. xxx` 的点号，会导致错误截断。
        cand = WIKI_ROOT / (rel if rel.endswith(".md") else (rel + ".md"))
        if cand.exists():
            return cand
    return stems.get(t)


def collect_wikilinks() -> list[tuple[Path, str]]:
    pairs: list[tuple[Path, str]] = []
    for p in md_files(WIKI_ROOT):
        text = p.read_text(encoding="utf-8")
        for t in WIKILINK_RE.findall(text):
            target = t.strip()
            if target.startswith("raw/assets/attachments/"):
                # 附件路径不是 wiki 页面，不参与 wikilink 断链统计；交给 missing_attachments 检查
                continue
            if not target or target in IGNORE_WIKILINK_TARGETS:
                continue
            pairs.append((p, target))
    return pairs


def collect_attachment_paths() -> list[tuple[Path, str]]:
    pairs: list[tuple[Path, str]] = []
    bases = [WIKI_ROOT, RAW_ROOT, ROOT / "outputs"]
    for base in bases:
        if not base.exists():
            continue
        for p in md_files(base):
            text = p.read_text(encoding="utf-8")
            for t in ATTACHMENT_PATH_RE.findall(text):
                pairs.append((p, t.strip()))
    return pairs


def is_orphan_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel.startswith(prefix) for prefix in ORPHAN_EXCLUDE_DIR_PREFIXES)


def check_wikilinks() -> tuple[list[tuple[Path, str]], dict[Path, int]]:
    stems = build_wiki_stem_index()
    inbound: dict[Path, int] = {p: 0 for p in md_files(WIKI_ROOT)}
    broken: list[tuple[Path, str]] = []

    for src, target in collect_wikilinks():
        dst = resolve_wikilink_target(target, stems)
        if dst is None:
            broken.append((src, target))
            continue
        inbound[dst] = inbound.get(dst, 0) + 1

    return broken, inbound


def check_raw_frontmatter() -> list[FrontmatterCheck]:
    # raw 层的最小字段（按 repo 约定）
    required = {"source_type", "created_at", "topics", "status"}
    issues: list[FrontmatterCheck] = []

    for p in md_files(RAW_ROOT):
        if p.name in {"README.md", "_index.md"}:
            continue
        text = p.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        missing = sorted([k for k in required if k not in fm])
        if missing:
            issues.append(FrontmatterCheck(path=p, missing_keys=tuple(missing)))
    return issues


def check_raw_naming() -> list[Path]:
    issues: list[Path] = []
    for p in md_files(RAW_ROOT):
        if p.name in {"README.md", "_index.md"}:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in RAW_NAMING_ALLOWLIST:
            continue
        # 目录式条目：raw/local-notes/**/index.md 常见，不要求带日期前缀
        if p.name == "index.md":
            continue
        # raw/repos 下允许 repo-组织-仓库.md
        if rel.startswith("raw/repos/") and RAW_REPO_CARD_RE.match(p.name):
            continue
        if not RAW_DATE_PREFIX_RE.match(p.name):
            issues.append(p)
    return issues


def check_missing_attachments() -> list[tuple[Path, str]]:
    missing: list[tuple[Path, str]] = []
    for src, rel in collect_attachment_paths():
        path = (ROOT / rel).resolve()
        if not path.exists():
            missing.append((src, rel))
    return missing


def main() -> int:
    # 1) 结构/字段/相对链接（现有脚本）
    # 注：这里不调用 tools/wiki_lint.py，避免在报告里产生双份输出；上层可自行执行。

    # 2) wikilinks / orphans
    broken, inbound = check_wikilinks()
    orphans = [
        p
        for p, n in inbound.items()
        if n == 0 and not is_orphan_excluded(p) and p != (WIKI_ROOT / "index.md")
    ]

    # 3) raw frontmatter
    raw_issues = check_raw_frontmatter()

    # 3.5) raw naming convention
    raw_naming_issues = check_raw_naming()

    # 4) attachments existence
    missing_attachments = check_missing_attachments()

    print("Wiki Health Check Summary")
    print(f"- wiki md: {len(md_files(WIKI_ROOT))}")
    print(f"- raw md: {len(md_files(RAW_ROOT))}")
    print(f"- broken wikilinks: {len(broken)}")
    print(f"- orphan pages (excluding indexes/*): {len(orphans)}")
    print(f"- raw frontmatter missing(min): {len(raw_issues)}")
    print(f"- raw naming issues: {len(raw_naming_issues)}")
    print(f"- missing attachments: {len(missing_attachments)}")

    if broken:
        print("\nTop broken wikilinks (up to 50):")
        for src, t in broken[:50]:
            print(f"- {src.relative_to(ROOT)} -> [[{t}]]")

    if orphans:
        print("\nTop orphan pages (up to 50):")
        for p in orphans[:50]:
            print(f"- {p.relative_to(ROOT)}")

    if raw_issues:
        print("\nTop raw frontmatter issues (up to 50):")
        for it in raw_issues[:50]:
            miss = ", ".join(it.missing_keys)
            print(f"- {it.path.relative_to(ROOT)} missing: {miss}")

    if raw_naming_issues:
        print("\nTop raw naming issues (up to 50):")
        for p in raw_naming_issues[:50]:
            print(f"- {p.relative_to(ROOT)}")

    if missing_attachments:
        print("\nTop missing attachments (up to 50):")
        for src, rel in missing_attachments[:50]:
            print(f"- {src.relative_to(ROOT)} -> {rel}")

    # 非零退出表示存在健康债务（便于 CI/脚本集成）
    return 1 if (broken or orphans or raw_issues or raw_naming_issues or missing_attachments) else 0


if __name__ == "__main__":
    raise SystemExit(main())
