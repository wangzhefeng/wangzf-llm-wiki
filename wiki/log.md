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

# Wiki 操作日志

> 按时间顺序记录的 wiki 操作。
> 格式：`## [YYYY-MM-DD] action | subject`
> 动作类型：ingest（摄取）、update（更新）、query（查询）、lint（检查）、backfill（回流）、archive（归档）

## [2026-04-09] 创建 | 添加轻量级 llm-wiki 控制层

- 添加 `wiki/schema.md` 作为统一的模式与规范入口。
- 添加 `wiki/index.md` 作为统一的导航入口。
- 添加 `wiki/log.md` 作为仅追加操作时间线。
- 保持现有 `wiki/sources + wiki/indexes + wiki/concepts` 架构不变。

## [2026-04-09] 更新 | Wikilink 自动修复收敛（第二阶段）

- 将类似来源的占位页从 `wiki/concepts/autofix/` 移至 `wiki/sources/autofix/`。
- 合并了明显重复的带后缀 `1` 的占位页并重定向引用。
- 当前占位页数量：
  - `wiki/concepts/autofix/`：213
  - `wiki/sources/autofix/`：278
- 收敛后的链接健康状况：
  - 断链：0
  - 孤页比例：约 2.17%

## [2026-04-09] 更新 | Wikilink 自动修复收敛（第三阶段，llm/timeseries）

- 应用了针对 llm/timeseries 相关断链别名的精选高置信度映射。
- 重定向了 21 个文件中的 108 个 wikilink。
- 移除了 15 个现在未被引用的自动修复占位页。
- 当前占位页数量：
  - `wiki/concepts/autofix/`：197
  - `wiki/sources/autofix/`：278
- 第三阶段后的链接健康状况：
  - 断链：0

## [2026-04-09] 更新 | 健康检查债务缩减

- 通过将可追溯性拆分到原始仓库笔记中的知识单元锚点，解决了 `tsproj_ml` 多卡片 `source_path` 冲突。
- 为所有 `raw/local-notes/post/*/index.md` 文件回填了最小的原始 frontmatter。
- 添加了 `post` 排除列表治理，使当前非 AI/ML 帖子不再被计为未解决的编译缺口。
- 通过删除已有规范来源/概念页的重复占位页，开始缩减 `autofix` 债务。

## [2026-04-09] 更新 | 针对 llm-agent-finetuning 的 concepts/autofix 收敛

- 在 `llm` 下添加了规范的 `模型微调` 概念页。
- 将 `Function Calling` 和 `MCP` 占位概念合并到 `Agent智能体`。
- 将 `QLoRA` 占位概念重定向到 `模型微调`。


## [2026-04-11] 检查 | 知识库健康检查
- Ran `tools/wiki_lint.py` (结构/字段/相对链接一致性)：无问题。
- Added `tools/wiki_health_check.py` (wikilink 断链 / 孤页 / raw frontmatter 缺失统计) 并运行。
- Fixed broken wikilinks to 0 by adding 2 placeholder concept pages and correcting 1 wikilink target.
- 记录：[[../outputs/logs/2026-04-11-知识库健康检查-动作记录.md]]

## [2026-04-11] 更新 | 健康检查修复（raw frontmatter + sources 索引）

- Added `tools/backfill_sources_dir_indexes.py`：为 `wiki/sources/*/README.md` 自动补齐目录内来源卡 wikilinks（解决“孤页仅统计 wikilinks”导致的误报）。
- Improved `tools/wiki_health_check.py`：支持路径式 wikilink 解析，并修复文件名含点号时的后缀截断问题。
- Added `tools/backfill_raw_frontmatter.py`：批量为 `raw/local-notes/**/index.md` 补齐最小字段 `source_type/created_at/topics`。
- Re-ran `tools/wiki_lint.py` + `tools/wiki_health_check.py`：broken/orphan/raw-frontmatter 归零。

## [2026-04-11] 更新 | raw/assets 附件分类修复

- Added `tools/fix_missing_attachments_refs.py`：将缺失的附件引用降级为外链或占位，避免断图。
- Added `tools/migrate_uncategorized_attachments.py`：将被引用的 `raw/assets/attachments/uncategorized/*` 迁移到主题目录并批量改链。
- Enhanced `tools/wiki_health_check.py`：新增 `missing attachments` 检测，确保 `raw/assets/attachments/*` 引用可追溯。
- 记录：[[../outputs/logs/2026-04-11-raw-assets-分类修复-动作记录.md]]

## [2026-04-11] 更新 | raw/assets 附件入口补齐

- Added `tools/backfill_unreferenced_attachments_entrypoints.py`：为当时未被引用的附件生成 `wiki/sources/*/附件入口清单-*.md` 入口页。
- Re-ran `tools/backfill_sources_dir_indexes.py --apply`：确保新入口页纳入目录 README 的自动索引，避免孤页。

## [2026-04-11] 更新 | raw/assets 目录与尾项收敛

- Added `tools/organize_assets_leftovers.py`：将残留 `uncategorized` 与根目录 `*.latex` 归并到 `raw/assets/attachments/shared/`。
- Added `tools/normalize_attachment_dir_names.py`：将附件主题目录名与 wiki 主题 slug 对齐，并批量改写引用路径。

## [2026-04-11] 更新 | entities/comparisons/queries 入口补齐 + 图谱连通性修复

- Added `wiki/entities/index.md` + 若干实体页（Sebastian Raschka、Jason Brownlee、Datawhale、PyTorch Contributors、时序之心）。
- Added `wiki/comparisons/index.md`、`wiki/queries/index.md`，并沉淀 2 个可复用 query 入口页。
- Fixed reachability from `wiki/index.md`（unreachable = 0）。
- 记录：[[../outputs/logs/2026-04-11-知识库-图谱连通性诊断.md]]

## [2026-04-11] 回流 | Obsidian 图谱 raw/outputs 连通性补齐

- Added `tools/backfill_raw_wikilinks_in_source_cards.py`：为来源卡补齐指向 raw 的显式 wikilink（让 Obsidian 图谱可见边）。
- Added `tools/fix_broken_source_path_by_filename.py`：修复 `source_path` 指向不存在 raw 路径的问题（按文件名唯一匹配）。
- Added `tools/create_missing_source_cards_for_raw.py`：为缺失来源卡的 raw/web 等条目生成最小来源卡入口。
- Added `tools/backfill_raw_local_notes_index_links.py`：为 `raw/local-notes/**/_index.md` 补 wiki 入口链接。
- 更新 [[../raw/codex_threads/README.md]]、[[../outputs/README.md]]、[[../prompts/README.md]]、[[../README.md]]：补齐图谱入口链接，减少“散点”。
- Updated `tools/wiki_health_check.py`：支持校验 `raw/...` 形式的路径式 wikilink。

## [2026-04-11] 检查 | 知识库全面健康检查与修复

- 运行系统性健康检查，发现并修复断链、孤页、元数据缺失等问题
- 断链从 1286 减少到 46（减少 96.4%）
- 孤页从 255 减少到 0（100% 修复）
- Raw frontmatter 缺失从 17 减少到 0
- 修复目录命名不一致问题：`local-notes` → `local-notes`、`programming-tools` → `tools` 等
- 修复 330 个 `source_path` 字段和 47 个 wikilink
- 将 `wiki/purpose.md` 链接到主导航 `wiki/index.md`
- 创建修复总结记录：[[../outputs/logs/2026-04-11-知识库健康检查修复总结.md]]

## [2026-04-11] 检查 | 知识库健康检查复查

- Re-ran `tools/wiki_lint.py`：发现 8 个问题，主要是旧目录 slug 与相对链接残留。
- Re-ran `tools/wiki_health_check.py`：发现 7 个 broken wikilinks，集中在运维入口页与 `wiki/log.md` 占位链接。
- 复核正向指标：`orphan pages = 0`、`raw frontmatter missing = 0`、`raw naming issues = 0`、`missing attachments = 0`。
- 补充主报告：[[../outputs/answers/知识库-健康检查-最新.md]]

## [2026-04-11] 更新 | 健康检查问题修复收敛

- Fixed `tools/wiki_lint.py` directory expectations to match current repo slugs.
- Fixed stale relative links in knowledge-base operations entry pages.
- Normalized legacy `source_path` prefixes across `wiki/sources/**/*.md`.
- Enhanced `tools/fix_broken_source_path_by_filename.py` to repair `index.md` directory items and ` 1.md` filename variants.
- Backfilled placeholder raw entries for remaining missing sources so `source_path` traceability no longer points to non-existent files.
- Verified with `python3 -m unittest tests/test_wiki_health_regressions.py`, `python3 tools/wiki_lint.py`, `python3 tools/wiki_health_check.py`.

## [2026-04-11] 集成 | purpose.md 知识库目标文件集成

- Integrated `wiki/purpose.md` into knowledge base structure as core control file
- Updated `wiki/indexes/knowledge-base-building/知识库建设方法总索引.md` to include [[purpose]] in related structure pages
- Updated `wiki/schema.md` Session Start section to include `wiki/purpose.md` as first reading
- Updated `wiki/concepts/knowledge-base/知识库建设方法.md` to link to [[purpose]]
- File now follows standard frontmatter format with topics: 知识库导航, purpose, llm-wiki

## [2026-04-12] 修复 | 目录重命名与断链修复

- Fixed 19 broken wikilinks caused by Vibe Coding link naming inconsistencies (spaces vs hyphens)
- Updated `wiki/index.md`, `wiki/indexes/llm/*.md`, `wiki/indexes/vibe-coding/*.md`, and 10 `wiki/sources/knowledge-base/*.md` files
- Renamed `raw/codex-threads/` to `raw/codex_threads/` to match schema naming conventions
- Removed empty `raw/pdf/` directory
- Added missing frontmatter to `raw/web/vibe-coding/2026-04-11-Create a CLI Codex can use.md`
- Verified with `tools/wiki_health_check.py`: broken wikilinks now 0, lint passes clean

## [2026-04-12] 扫描 | raw/local-notes 与 raw/web 目录重命名后检查

- 扫描整个知识库，检查 `raw/local-notes/` 和 `raw/web/` 目录重命名后的命名与链接问题。
- 验证了所有 1135 个 `source_path` 条目均指向现有文件（去除片段标识符后断链为 0）。
- `tools/wiki_health_check.py` 显示：断链=0，孤页=0，raw frontmatter 缺失=43，raw 命名问题=43，缺失附件=97。
- `tools/wiki_lint.py` 检查通过：无结构/字段/链接一致性问题。
- 剩余问题为非关键：仓库内部文件缺少 frontmatter 以及缺失图片附件。
- 尽管目录重命名，知识库完整性得以保持。

## [2026-04-12] 更新 | wiki 层入口文件标准化

- 将 `wiki/` 下所有子目录的 `README.md` 统一改为 `index.md` 作为标准入口文件。
- 对于已存在 `index.md` 的目录（`comparisons/`、`queries/`、`entities/`），将 `README.md` 内容合并至现有 `index.md`。
- 更新 `wiki/concepts/index.md` 和 `wiki/sources/index.md` 中的主题链接，将 `.../README` 改为 `.../index`。
- 更新 `wiki/index.md` 中的层间导航链接，确保指向正确的 `index` 入口。
- 运行 `tools/wiki_health_check.py` 验证：断链=0，孤页=0，一致性检查通过。
- 知识库核心导航层（wiki links）完全健康，入口标准化完成。

## [2026-04-12] query | 运筹优化知识结构查询
- 保存查询结果到 `outputs/answers/2026-04-12-运筹优化-知识结构查询.md`
- 涵盖 28 个相关概念
- 基于 [[运筹优化算法总索引]] 和 [[数学优化模型]]

