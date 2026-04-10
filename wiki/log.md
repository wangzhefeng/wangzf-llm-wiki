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

- Added `wiki/SCHEMA.md` as unified schema and conventions entry.
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
