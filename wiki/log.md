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

## [2026-04-11] update | entities/comparisons/queries 入口补齐 + 图谱连通性修复

- Added `wiki/entities/index.md` + 若干实体页（Sebastian Raschka、Jason Brownlee、Datawhale、PyTorch Contributors、时序之心）。
- Added `wiki/comparisons/index.md`、`wiki/queries/index.md`，并沉淀 2 个可复用 query 入口页。
- Fixed reachability from `wiki/index.md`（unreachable = 0）。
- Logged: `outputs/logs/2026-04-11-知识库-图谱连通性诊断.md`

## [2026-04-11] backfill | Obsidian 图谱 raw/outputs 连通性补齐

- Added `tools/backfill_raw_wikilinks_in_source_cards.py`：为来源卡补齐指向 raw 的显式 wikilink（让 Obsidian 图谱可见边）。
- Added `tools/fix_broken_source_path_by_filename.py`：修复 `source_path` 指向不存在 raw 路径的问题（按文件名唯一匹配）。
- Added `tools/create_missing_source_cards_for_raw.py`：为缺失来源卡的 raw/web 等条目生成最小来源卡入口。
- Added `tools/backfill_raw_local_notes_index_links.py`：为 `raw/local-notes/**/_index.md` 补 wiki 入口链接。
- Updated `raw/codex_threads/README.md`、`outputs/README.md`、`prompts/README.md`、`README.md`：补齐图谱入口链接，减少“散点”。
- Updated `tools/wiki_health_check.py`：支持校验 `raw/...` 形式的路径式 wikilink。

## [2026-04-11] lint | 知识库全面健康检查与修复

- 运行系统性健康检查，发现并修复断链、孤页、元数据缺失等问题
- 断链从 1286 减少到 46（减少 96.4%）
- 孤页从 255 减少到 0（100% 修复）
- Raw frontmatter 缺失从 17 减少到 0
- 修复目录命名不一致问题：`local-notes` → `localnotes`、`programming-tools` → `tools` 等
- 修复 330 个 `source_path` 字段和 47 个 wikilink
- 将 `wiki/purpose.md` 链接到主导航 `wiki/index.md`
- 创建修复总结记录：`outputs/logs/2026-04-11-知识库健康检查修复总结.md`

## [2026-04-11] lint | 知识库健康检查复查

- Re-ran `tools/wiki_lint.py`：发现 8 个问题，主要是旧目录 slug 与相对链接残留。
- Re-ran `tools/wiki_health_check.py`：发现 7 个 broken wikilinks，集中在运维入口页与 `wiki/log.md` 占位链接。
- 复核正向指标：`orphan pages = 0`、`raw frontmatter missing = 0`、`raw naming issues = 0`、`missing attachments = 0`。
- 补充主报告：`outputs/answers/知识库-健康检查-最新.md`

## [2026-04-11] update | 健康检查问题修复收敛

- Fixed `tools/wiki_lint.py` directory expectations to match current repo slugs.
- Fixed stale relative links in knowledge-base operations entry pages.
- Normalized legacy `source_path` prefixes across `wiki/sources/**/*.md`.
- Enhanced `tools/fix_broken_source_path_by_filename.py` to repair `index.md` directory items and ` 1.md` filename variants.
- Backfilled placeholder raw entries for remaining missing sources so `source_path` traceability no longer points to non-existent files.
- Verified with `python3 -m unittest tests/test_wiki_health_regressions.py`, `python3 tools/wiki_lint.py`, `python3 tools/wiki_health_check.py`.
