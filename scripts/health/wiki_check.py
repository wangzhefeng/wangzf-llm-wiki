#!/usr/bin/env python3
"""
Wiki 统一检查工具 - 整合了 wiki_lint.py 和 wiki_health_check.py 的功能

提供完整的知识库健康检查，包括：
1. 目录结构与字段格式检查（原 wiki_lint.py）
2. 链接网络与完整性检查（原 wiki_health_check.py）

用法:
  python wiki_check.py [--root PATH] [--checks CHECKS] [--output {summary,detailed}]
  
示例:
  python wiki_check.py                       # 运行所有检查
  python wiki_check.py --checks lint         # 只运行 lint 检查
  python wiki_check.py --checks health       # 只运行 health 检查
  python wiki_check.py --output detailed     # 详细输出
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

# ============================================================================
# 常量定义
# ============================================================================

class Severity(Enum):
    """检查结果严重度三级分类"""
    ERROR = "error"        # 阻塞性错误：必须修复（断链、缺字段、目录不一致）
    WARNING = "warning"    # 提示性警告：建议修复（孤儿页、低入口、过期内容）
    INFO = "info"          # 信息性提示：可关注（内容新鲜度、覆盖率统计）

# 原 wiki_lint.py 常量
ALLOWED_STATUS = {"summarized", "inbox", "linked", "archived", "active"}
EXPECTED_SOURCES = {
    "causal-inference",
    "control-algorithms",
    "deep-learning",
    "feature-engineering",
    "llm",
    "llm-wiki",
    "machine-learning",
    "nlp",
    "operations-research",
    "power-market-trading",
    "reinforcement-learning",
    "statistics-theory",
    "timeseries-analysis",
    "vibe-coding",
}
EXPECTED_CONCEPTS = set(EXPECTED_SOURCES)
# indexes 额外包含 shared 目录（sources/concepts 中无）
EXPECTED_INDEXES = EXPECTED_SOURCES | {"shared"}

# 原 wiki_health_check.py 常量
WIKILINK_RE = re.compile(r"\[\[([^\]#|]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
ATTACHMENT_PATH_RE = re.compile(
    r"raw/assets/attachments/[A-Za-z0-9_./% ()-]+\.[A-Za-z0-9]+"
)
FENCED_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)

IGNORE_WIKILINK_TARGETS = {
    "某个总索引",
    "某个概念页",
    "某个来源卡",
    "某篇结果页",
}

ORPHAN_EXCLUDE_DIR_PREFIXES = {
    "wiki/indexes/",
    "wiki/concepts/autofix/",
    "wiki/sources/autofix/",
}

RAW_NAMING_ALLOWLIST = {
    "raw/codex_threads/线程总结模板.md",
    "raw/codex_threads/README.md",
    "raw/local-notes/时间序列预测-历史文档清单.md",
    "raw/local-notes/深度学习-历史文档清单.md",
    "raw/local-notes/知识库建设方法-历史文档清单.md",
    "raw/local-notes/运筹优化算法-历史文档清单.md",
    "raw/repos/repo-wangzhefeng-tsproj-ml.md",
    "raw/notes/vibe-coding/agent.md",
    "raw/notes/vibe-coding/claude_code.md",
    "raw/notes/vibe-coding/codex.md",
    "raw/notes/vibe-coding/mcp.md",
    "raw/notes/vibe-coding/openclaw.md",
    "raw/notes/vibe-coding/rag.md",
    "raw/notes/vibe-coding/skills.md",
    "raw/notes/vibe-coding/tools.md",
}

RAW_DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
RAW_REPO_CARD_RE = re.compile(r"^repo-[A-Za-z0-9_.-]+-[A-Za-z0-9_.-]+\.md$")

LEGACY_NAMING_RULES = {
    "llm-knowledge-base": "llm-wiki",
    "prompts/query/knowledge-base-query": "prompts/query/llm-wiki-query",
    "prompts/maintenance/knowledge-base-health-check": "prompts/maintenance/llm-wiki-health-check",
    "wiki/indexes/knowledge-base-": "wiki/indexes/llm-wiki-",
    "wiki/sources/knowledge-base/": "wiki/sources/llm-wiki/",
    "wiki/concepts/knowledge-base/": "wiki/concepts/llm-wiki/",
}

LEGACY_NAMING_EXCLUDE_PATH_PREFIXES = {
    "outputs/logs/",
    "raw/codex_threads/",
    "raw/repos/",
}

LEGACY_NAMING_EXACT_PATHS = {
    "wiki/log.md",
}

WIKILINK_EXACT_SKIP_PATHS = {
    "wiki/log.md",
}

WIKILINK_MEDIA_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif")

# ============================================================================
# 工具函数
# ============================================================================

def get_root_path(root_arg: Optional[str] = None) -> Path:
    """获取仓库根目录路径"""
    if root_arg:
        return Path(root_arg).resolve()
    else:
        # 向后兼容：尝试从脚本位置推导
        # wiki_check.py 位于 scripts/health/ → 上溯 2 层到达项目根
        return Path(__file__).resolve().parents[2]

def md_files(base: Path) -> list[Path]:
    """获取目录下所有 Markdown 文件"""
    if not base.exists():
        return []
    return sorted([p for p in base.rglob("*.md") if p.is_file()])


def should_skip_legacy_naming_check(path: Path, root: Path) -> bool:
    """跳过历史日志、线程总结和仓库镜像中的旧命名。"""
    rel = path.relative_to(root).as_posix()
    if rel in LEGACY_NAMING_EXACT_PATHS:
        return True
    return any(rel.startswith(prefix) for prefix in LEGACY_NAMING_EXCLUDE_PATH_PREFIXES)


def should_skip_raw_repo_mirror(path: Path, root: Path) -> bool:
    """跳过 raw/repos 下的嵌套仓库镜像文档，只检查仓库入口卡。"""
    rel = path.relative_to(root)
    return rel.parts[:2] == ("raw", "repos") and len(rel.parts) > 3

def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """解析 frontmatter"""
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

def build_wiki_stem_index(wiki_root: Path) -> dict[str, Path]:
    """构建 wiki 文件词干索引（包含 wiki、raw、outputs 目录）"""
    idx: dict[str, Path] = {}
    
    # 包含 wiki 目录
    for p in md_files(wiki_root):
        idx[p.stem] = p
    
    # 包含 raw 目录（所有子目录）
    raw_root = wiki_root.parent / "raw"
    if raw_root.exists():
        for p in md_files(raw_root):
            # 避免覆盖 wiki 中的文件（如果有冲突，优先使用 wiki 版本）
            if p.stem not in idx:
                idx[p.stem] = p
    
    # 包含 outputs 目录
    outputs_root = wiki_root.parent / "outputs"
    if outputs_root.exists():
        for p in md_files(outputs_root):
            if p.stem not in idx:
                idx[p.stem] = p
    
    return idx

def resolve_wikilink_target(target: str, stems: dict[str, Path], root: Path, wiki_root: Path) -> Path | None:
    """解析 wikilink 目标"""
    t = target.strip()
    if not t:
        return None

    if t == "schema":
        cand = root / "schema.md"
        if cand.exists():
            return cand
    if t == "purpose":
        cand = root / "purpose.md"
        if cand.exists():
            return cand
    
    # 支持 raw 路径式 wikilink：[[raw/web/xx/2026-...]]（Obsidian 图谱需要显式 raw 互链）
    if t.startswith("raw/"):
        known_exts = {
            ".md", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".mov",
        }
        suffix = Path(t).suffix.lower()
        cand = root / t if suffix in known_exts else root / (t + ".md")
        if cand.exists():
            return cand
        return None
    
    # 支持 outputs 路径式 wikilink：[[outputs/answers/2026-...]]（输出结果页面）
    if t.startswith("outputs/"):
        known_exts = {
            ".md", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".mov",
        }
        suffix = Path(t).suffix.lower()
        cand = root / t if suffix in known_exts else root / (t + ".md")
        if cand.exists():
            return cand
        return None
    
    # 支持路径式 wikilink：[[wiki/sources/analysis/README]] 或 [[sources/analysis/README]]
    if "/" in t:
        rel = t
        if rel.startswith("wiki/"):
            rel = rel[len("wiki/"):]
        cand = wiki_root / (rel if rel.endswith(".md") else (rel + ".md"))
        if cand.exists():
            return cand
    
    # 最后检查 stem 索引
    result = stems.get(t)
    if result is not None:
        return result
    
    # 检查是否是目录（带有 index.md）
    # 首先在 raw/ 目录下检查（包括子目录）
    import glob
    raw_cand_dirs = list((root / "raw").rglob(t))
    for raw_cand_dir in raw_cand_dirs:
        if raw_cand_dir.is_dir():
            index_file = raw_cand_dir / "index.md"
            if index_file.exists():
                return index_file
    
    # 如果在 raw/ 中没找到，检查直接路径（向后兼容）
    raw_cand_dir = root / "raw" / t
    if raw_cand_dir.is_dir():
        index_file = raw_cand_dir / "index.md"
        if index_file.exists():
            return index_file
    
    # 然后在 wiki/ 目录下检查（包括子目录）
    wiki_cand_dirs = list(wiki_root.rglob(t))
    for wiki_cand_dir in wiki_cand_dirs:
        if wiki_cand_dir.is_dir():
            index_file = wiki_cand_dir / "index.md"
            if index_file.exists():
                return index_file
    
    # 如果在 wiki/ 中没找到，检查直接路径
    wiki_cand_dir = wiki_root / t
    if wiki_cand_dir.is_dir():
        index_file = wiki_cand_dir / "index.md"
        if index_file.exists():
            return index_file
    
    # 最后在 outputs/ 目录下检查（包括子目录）
    outputs_cand_dirs = list((root / "outputs").rglob(t))
    for outputs_cand_dir in outputs_cand_dirs:
        if outputs_cand_dir.is_dir():
            index_file = outputs_cand_dir / "index.md"
            if index_file.exists():
                return index_file
    
    # 如果在 outputs/ 中没找到，检查直接路径
    outputs_cand_dir = root / "outputs" / t
    if outputs_cand_dir.is_dir():
        index_file = outputs_cand_dir / "index.md"
        if index_file.exists():
            return index_file
    
    return None

def collect_wikilinks(wiki_root: Path) -> list[tuple[Path, str]]:
    """收集所有 wikilink"""
    pairs: list[tuple[Path, str]] = []
    for p in md_files(wiki_root):
        text = p.read_text(encoding="utf-8")
        text = FENCED_CODE_BLOCK_RE.sub("", text)
        for t in WIKILINK_RE.findall(text):
            target = t.strip()
            if target.startswith("raw/assets/attachments/"):
                # 附件路径不是 wiki 页面，不参与 wikilink 断链统计
                continue
            if not target or target in IGNORE_WIKILINK_TARGETS:
                continue
            pairs.append((p, target))
    return pairs

def collect_attachment_paths(root: Path, wiki_root: Path, raw_root: Path) -> list[tuple[Path, str]]:
    """收集所有附件引用"""
    pairs: list[tuple[Path, str]] = []
    bases = [wiki_root, raw_root, root / "outputs"]
    for base in bases:
        if not base.exists():
            continue
        for p in md_files(base):
            text = p.read_text(encoding="utf-8")
            for t in ATTACHMENT_PATH_RE.findall(text):
                pairs.append((p, t.strip()))
    return pairs

def is_orphan_excluded(path: Path, root: Path) -> bool:
    """判断页面是否应排除在孤页检查外"""
    rel = path.relative_to(root).as_posix()
    return any(rel.startswith(prefix) for prefix in ORPHAN_EXCLUDE_DIR_PREFIXES)

# ============================================================================
# 检查函数
# ============================================================================

@dataclass
class CheckResult:
    """检查结果，支持三级严重度"""
    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    
    @property
    def total_issues(self) -> int:
        return len(self.errors) + len(self.warnings) + len(self.infos)
    
    @property
    def error_count(self) -> int:
        return len(self.errors)
    
    @property
    def warning_count(self) -> int:
        return len(self.warnings)
    
    @property
    def info_count(self) -> int:
        return len(self.infos)

# 原 wiki_lint.py 检查函数

def check_dirs(root: Path) -> CheckResult:
    """检查目录结构"""
    errors = []
    sources = {p.name for p in (root / "wiki" / "sources").iterdir() if p.is_dir()}
    concepts = {p.name for p in (root / "wiki" / "concepts").iterdir() if p.is_dir()}
    indexes = {p.name for p in (root / "wiki" / "indexes").iterdir() if p.is_dir()}

    if sources != EXPECTED_SOURCES:
        errors.append(f"sources 顶层目录不一致: {sorted(sources)}")
    if concepts != EXPECTED_CONCEPTS:
        errors.append(f"concepts 顶层目录不一致: {sorted(concepts)}")

    if indexes != EXPECTED_INDEXES:
        errors.append(f"indexes 顶层目录不一致: {sorted(indexes)}")
    
    return CheckResult("目录映射", errors)

def check_source_path(root: Path) -> CheckResult:
    """检查 source_path 字段"""
    errors = []
    for p in md_files(root / "wiki" / "sources"):
        text = p.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        if "source_path" not in fm:
            continue
        values = fm["source_path"] if isinstance(fm["source_path"], list) else [fm["source_path"]]
        for val in values:
            if not isinstance(val, str) or not val.startswith("raw/"):
                errors.append(f"{p} source_path 非 raw/ 相对路径 -> {val}")
    return CheckResult("source_path", errors)

def check_status(root: Path) -> CheckResult:
    """检查 status 字段"""
    errors = []
    for p in md_files(root / "wiki"):
        for line_no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.startswith("status:"):
                continue
            val = line.split(":", 1)[1].strip()
            if val not in ALLOWED_STATUS:
                errors.append(f"{p}:{line_no} status 非法 -> {val}")
    return CheckResult("status", errors)

def check_relative_links(root: Path) -> CheckResult:
    """检查相对链接"""
    errors = []
    pat = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")
    for p in md_files(root / "wiki"):
        text = p.read_text(encoding="utf-8")
        for rel in pat.findall(text):
            link = rel.strip()
            if link.startswith(("http://", "https://", "/", "#", "mailto:")):
                continue
            target = (p.parent / link).resolve()
            if not target.exists():
                errors.append(f"{p} -> {link} (不存在)")
    return CheckResult("相对链接", errors)


def check_legacy_naming(root: Path) -> CheckResult:
    """检查仓库内应已迁移但仍残留的旧主题命名。"""
    errors = []
    scan_roots = [
        root / "wiki",
        root / "outputs",
        root / "prompts",
        root / "raw" / "README.md",
        root / "raw" / "assets" / "README.md",
        root / "raw" / "notes" / "llm-wiki",
        root / "raw" / "web" / "llm-wiki",
    ]

    files: list[Path] = []
    for item in scan_roots:
        if item.is_file():
            files.append(item)
        elif item.exists():
            files.extend(md_files(item))

    seen: set[Path] = set()
    for p in sorted(files):
        if p in seen or should_skip_legacy_naming_check(p, root):
            continue
        seen.add(p)
        rel = p.relative_to(root).as_posix()

        for legacy, replacement in LEGACY_NAMING_RULES.items():
            if legacy in rel:
                errors.append(f"{rel} 路径仍含旧命名 -> {legacy} (建议: {replacement})")

        text = p.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("source_path:"):
                continue
            if stripped.startswith("- 原文：[[raw/") or stripped.startswith("- 来源：`raw/"):
                continue
            if "raw/assets/attachments/knowledge-base/" in stripped:
                continue
            for legacy, replacement in LEGACY_NAMING_RULES.items():
                if legacy in line:
                    errors.append(
                        f"{rel}:{line_no} 仍含旧命名 -> {legacy} (建议: {replacement})"
                    )

    return CheckResult("旧命名残留", errors)

# 原 wiki_health_check.py 检查函数

@dataclass(frozen=True)
class FrontmatterCheck:
    path: Path
    missing_keys: tuple[str, ...]

def check_wikilinks(root: Path, wiki_root: Path) -> CheckResult:
    """检查 wikilink 断链和孤页"""
    stems = build_wiki_stem_index(wiki_root)
    inbound: dict[Path, int] = {
        p: 0
        for p in md_files(wiki_root)
        if p.relative_to(root).as_posix() not in WIKILINK_EXACT_SKIP_PATHS
    }
    errors = []
    warnings = []

    # 收集并检查 wikilink
    for src, target in collect_wikilinks(wiki_root):
        if src.relative_to(root).as_posix() in WIKILINK_EXACT_SKIP_PATHS:
            continue
        if target.startswith("raw/") or target.startswith("../outputs/") or target.startswith("outputs/"):
            continue
        if target.lower().endswith(WIKILINK_MEDIA_SUFFIXES):
            continue
        dst = resolve_wikilink_target(target, stems, root, wiki_root)
        if dst is None:
            errors.append(f"{src.relative_to(root)} -> [[{target}]]")
            continue
        inbound[dst] = inbound.get(dst, 0) + 1

    # 检查孤页
    orphans = [
        p
        for p, n in inbound.items()
        if n == 0 and not is_orphan_excluded(p, root) and p != (wiki_root / "index.md")
    ]
    
    for orphan in orphans:
        warnings.append(f"{orphan.relative_to(root)}")
    
    result = CheckResult("wikilinks", errors, warnings)
    result.stats = {
        "broken_count": len(errors),
        "orphan_count": len(orphans),
    }
    return result

def check_raw_frontmatter(root: Path, raw_root: Path) -> CheckResult:
    """检查 raw frontmatter"""
    required = {"source_type", "created_at", "topics", "status"}
    errors = []

    for p in md_files(raw_root):
        if should_skip_raw_repo_mirror(p, root):
            continue
        if p.name in {"README.md", "_index.md"}:
            continue
        text = p.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        missing = sorted([k for k in required if k not in fm])
        if missing:
            miss_str = ", ".join(missing)
            errors.append(f"{p.relative_to(root)} missing: {miss_str}")
    
    return CheckResult("raw frontmatter", errors)

def check_raw_naming(root: Path, raw_root: Path) -> CheckResult:
    """检查 raw 命名规范"""
    errors = []
    
    for p in md_files(raw_root):
        if should_skip_raw_repo_mirror(p, root):
            continue
        if p.name in {"README.md", "_index.md"}:
            continue
        rel = p.relative_to(root).as_posix()
        if rel in RAW_NAMING_ALLOWLIST:
            continue
        if p.name == "index.md":  # 目录式条目
            continue
        if rel.startswith("raw/repos/") and RAW_REPO_CARD_RE.match(p.name):
            continue
        if not RAW_DATE_PREFIX_RE.match(p.name):
            errors.append(f"{p.relative_to(root)}")
    
    return CheckResult("raw naming", errors)

def check_missing_attachments(root: Path, wiki_root: Path, raw_root: Path) -> CheckResult:
    """检查缺失的附件"""
    errors = []
    
    for src, rel in collect_attachment_paths(root, wiki_root, raw_root):
        path = (root / rel).resolve()
        if not path.exists():
            errors.append(f"{src.relative_to(root)} -> {rel}")
    
    return CheckResult("missing attachments", errors)

def check_content_freshness(root: Path, wiki_root: Path, stale_days: int = 90) -> CheckResult:
    """检查 wiki 页面内容新鲜度。
    
    扫描 wiki/ 下 .md 文件，检测 updated_at / created_at 字段。
    - 超过 stale_days 未更新的页面标记为 INFO
    - 无任何日期标记的页面标记为 WARNING
    """
    from datetime import datetime, timedelta
    
    now = datetime.now()
    cutoff = now - timedelta(days=stale_days)
    
    infos = []
    warnings = []
    fresh_count = 0
    no_date_count = 0
    
    date_keys = ("updated_at", "updated", "created_at", "created", "date")
    
    for p in md_files(wiki_root):
        rel = str(p.relative_to(root))
        text = p.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        
        # 提取最近日期
        latest_date = None
        for key in date_keys:
            val = fm.get(key)
            if isinstance(val, str):
                # 提取 YYYY-MM-DD 格式
                m = re.search(r'(\d{4}-\d{2}-\d{2})', val)
                if m:
                    try:
                        d = datetime.strptime(m.group(1), "%Y-%m-%d")
                        if latest_date is None or d > latest_date:
                            latest_date = d
                    except ValueError:
                        pass
        
        if latest_date is None:
            no_date_count += 1
            warnings.append(f"{rel} 无日期标记 (建议添加 updated_at)")
        elif latest_date < cutoff:
            days_ago = (now - latest_date).days
            infos.append(f"{rel} 最后更新于 {latest_date.strftime('%Y-%m-%d')} ({days_ago} 天前)")
        else:
            fresh_count += 1
    
    result = CheckResult("content freshness", warnings=warnings, infos=infos)
    result.stats = {
        "fresh_pages": fresh_count,
        "stale_pages": len(infos),
        "no_date_pages": no_date_count,
        "stale_threshold_days": stale_days,
    }
    return result

# ============================================================================
# 主函数
# ============================================================================

def run_all_checks(root: Path, check_types: set[str] = None, output_format: str = "summary") -> dict:
    """运行所有检查"""
    if check_types is None:
        check_types = {"lint", "health"}
    
    wiki_root = root / "wiki"
    raw_root = root / "raw"
    
    results = {}
    
    # Lint 检查
    if "lint" in check_types:
        results["目录映射"] = check_dirs(root)
        results["source_path"] = check_source_path(root)
        results["status"] = check_status(root)
        results["相对链接"] = check_relative_links(root)
        results["旧命名残留"] = check_legacy_naming(root)
    
    # Health 检查
    if "health" in check_types:
        results["wikilinks"] = check_wikilinks(root, wiki_root)
        results["raw frontmatter"] = check_raw_frontmatter(root, raw_root)
        results["raw naming"] = check_raw_naming(root, raw_root)
        results["missing attachments"] = check_missing_attachments(root, wiki_root, raw_root)
        results["content freshness"] = check_content_freshness(root, wiki_root)
    
    return results

def print_summary(results: dict, root: Path):
    """打印摘要报告（支持三级严重度）"""
    print("=" * 60)
    print("Wiki 统一检查报告")
    print("=" * 60)
    
    # 统计信息
    total_errors = sum(len(r.errors) for r in results.values())
    total_warnings = sum(len(r.warnings) for r in results.values())
    total_infos = sum(len(r.infos) for r in results.values())
    
    print(f"仓库根目录: {root}")
    print(f"检查项目: {len(results)} 项")
    print(f"发现错误: {total_errors} 个  |  警告: {total_warnings} 个  |  信息: {total_infos} 个")
    print()
    
    # 按检查项汇总
    for name, result in sorted(results.items()):
        ec = result.error_count
        wc = result.warning_count
        ic = result.info_count
        
        if ec > 0:
            icon = "❌"
        elif wc > 0:
            icon = "⚠️ "
        elif ic > 0:
            icon = "ℹ️ "
        else:
            icon = "✅"
        
        parts = []
        if ec: parts.append(f"错误:{ec}")
        if wc: parts.append(f"警告:{wc}")
        if ic: parts.append(f"信息:{ic}")
        detail = "  ".join(parts) if parts else "通过"
        print(f"{icon} {name:22} {detail}")
    
    print("\n" + "=" * 60)
    
    # 显示详细信息
    for name, result in sorted(results.items()):
        if not result.errors and not result.warnings and not result.infos:
            continue
        
        print(f"\n{name}:")
        
        if result.errors:
            print("  ❌ 错误:")
            for err in result.errors:
                print(f"    - {err}")
        
        if result.warnings:
            print("  ⚠️  警告:")
            for warn in result.warnings:
                print(f"    - {warn}")
        
        if result.infos:
            print("  ℹ️  信息:")
            for info in result.infos:
                print(f"    - {info}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Wiki 统一检查工具")
    parser.add_argument("--root", help="仓库根目录路径", default=None)
    parser.add_argument("--checks", help="检查类型: lint, health, all (默认: all)", 
                       default="all", choices=["lint", "health", "all"])
    parser.add_argument("--output", help="输出格式: summary, detailed (默认: summary)",
                       default="summary", choices=["summary", "detailed"])
    parser.add_argument("--max-errors", type=int, default=50,
                       help="每个类别最多显示的错误数 (默认: 50)")
    
    args = parser.parse_args()
    
    # 确定根目录
    root = get_root_path(args.root)
    
    # 确定检查类型
    if args.checks == "all":
        check_types = {"lint", "health"}
    else:
        check_types = {args.checks}
    
    print(f"开始检查仓库: {root}")
    print(f"检查类型: {', '.join(sorted(check_types))}")
    print()
    
    # 运行检查
    results = run_all_checks(root, check_types, args.output)
    
    # 输出结果
    print_summary(results, root)
    
    # 确定退出码（有任何错误则返回1）
    has_errors = any(len(result.errors) > 0 for result in results.values())
    return 1 if has_errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
