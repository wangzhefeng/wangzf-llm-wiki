---
created_at: 2026-04-09
topics:
  - 知识库维护
  - 操作日志
  - llm-wiki
related_concepts:
  - 知识库操作记录索引
  - 知识库健康检查清单
status: linked
---

# Wiki Log

> Chronological record of wiki operations.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, backfill, archive

## [2026-04-09] create | Add lightweight llm-wiki control layer

- Added `wiki/schema.md` as unified schema and conventions entry.
- Added `wiki/index.md` as unified navigation entry.
- Added `wiki/log.md` as append-only operation timeline.
- Kept existing `wiki/sources + wiki/indexes + wiki/concepts` architecture intact.

## [2026-04-09] update | Wikilink autofix convergence (phase 2)

- Moved source-like placeholder pages from `wiki/concepts/autofix/` to `wiki/sources/autofix/`.
- Merged obvious duplicate placeholders with suffix `1` and rewired references.
- Current placeholder volumes:
  - `wiki/concepts/autofix/`: 213
  - `wiki/sources/autofix/`: 278
- Link health after convergence:
  - broken wikilinks: 0
  - orphan ratio: ~2.17%

## [2026-04-09] update | Wikilink autofix convergence (phase 3, llm/timeseries)

- Applied curated high-confidence mappings for llm/timeseries-related broken-target aliases.
- Rewired 108 wikilinks across 21 files.
- Removed 15 now-unreferenced autofix placeholder pages.
- Current placeholder volumes:
  - `wiki/concepts/autofix/`: 197
  - `wiki/sources/autofix/`: 278
- Link health after phase 3:
  - broken wikilinks: 0

## [2026-04-09] update | Health-check debt reduction

- Resolved the `tsproj_ml` multi-card `source_path` collision by splitting traceability to knowledge-unit anchors in the raw repo note.
- Backfilled minimal raw frontmatter for all `raw/local-notes/post/*/index.md` files.
- Added `post` exclusion-list governance so current non-AI/ML posts stop being counted as unresolved compilation gaps.
- Started `autofix` debt reduction by deleting duplicate placeholder pages that already had canonical source/concept pages.

## [2026-04-09] update | concepts/autofix convergence for llm-agent-finetuning

- Added canonical `模型微调` concept page under `llm`.
- Merged `Function Calling` and `MCP` placeholder concepts into `Agent智能体`.
- Redirected `QLoRA` placeholder concept to `模型微调`.

## [2026-04-11] lint | 知识库健康检查

- Ran `tools/wiki_lint.py` (结构/字段/相对链接一致性)：无问题。
- Added `tools/wiki_health_check.py` (wikilink 断链 / 孤页 / raw frontmatter 缺失统计) 并运行。
- Fixed broken wikilinks to 0 by adding 2 placeholder concept pages and correcting 1 wikilink target.
- Logged: `outputs/logs/2026-04-11-知识库健康检查-动作记录.md`

## [2026-04-11] update | 健康检查修复（raw frontmatter + sources 索引）

- Added `tools/backfill_sources_dir_indexes.py`：为 `wiki/sources/*/README.md` 自动补齐目录内来源卡 wikilinks（解决“孤页仅统计 wikilinks”导致的误报）。
- Improved `tools/wiki_health_check.py`：支持路径式 wikilink 解析，并修复文件名含点号时的后缀截断问题。
- Added `tools/backfill_raw_frontmatter.py`：批量为 `raw/local-notes/**/index.md` 补齐最小字段 `source_type/created_at/topics`。
- Re-ran `tools/wiki_lint.py` + `tools/wiki_health_check.py`：broken/orphan/raw-frontmatter 归零。

## [2026-04-11] update | raw/assets 附件分类修复

- Added `tools/fix_missing_attachments_refs.py`：将缺失的附件引用降级为外链或占位，避免断图。
- Added `tools/migrate_uncategorized_attachments.py`：将被引用的 `raw/assets/attachments/uncategorized/*` 迁移到主题目录并批量改链。
- Enhanced `tools/wiki_health_check.py`：新增 `missing attachments` 检测，确保 `raw/assets/attachments/*` 引用可追溯。
- Logged: `outputs/logs/2026-04-11-raw-assets-分类修复-动作记录.md`

## [2026-04-11] update | raw/assets 附件入口补齐

- Added `tools/backfill_unreferenced_attachments_entrypoints.py`：为当时未被引用的附件生成 `wiki/sources/*/附件入口清单-*.md` 入口页。
- Re-ran `tools/backfill_sources_dir_indexes.py --apply`：确保新入口页纳入目录 README 的自动索引，避免孤页。

## [2026-04-11] update | raw/assets 目录与尾项收敛

- Added `tools/organize_assets_leftovers.py`：将残留 `uncategorized` 与根目录 `*.latex` 归并到 `raw/assets/attachments/shared/`。
- Added `tools/normalize_attachment_dir_names.py`：将附件主题目录名与 wiki 主题 slug 对齐，并批量改写引用路径。
