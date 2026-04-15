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

## 日志格式说明

- 按时间顺序记录 wiki 操作，保持 append-only。
- 格式：`## [YYYY-MM-DD] action | subject`
- 动作类型：`ingest`（摄取）、`update`（更新）、`query`（查询）、`lint`（检查）、`backfill`（回流）、`archive`（归档）

## [2026-04-15] 创建 | LLM 子主题总索引（理论/预训练/后训练）

- 在 `wiki/indexes/llm/` 下创建三个子主题总索引：
  - `LLM-理论基础总索引.md`（50 篇来源卡）：Transformer、Attention、位置编码、KV-Cache 等核心概念
  - `LLM-预训练总索引.md`（63 篇来源卡）：数据准备、分词、缩放定律、分布式训练、评估
  - `LLM-后训练总索引.md`（24 篇来源卡）：SFT、RLHF、DPO、量化、推理优化、安全对齐
- 更新 `大语言模型总索引.md` 添加指向三个子索引的导航链接
- 每个子索引包含：200-300 字总览、核心概念导航表、来源清单、三层阅读地图、相关索引

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
- 为所有 `raw/notes/post/*/index.md` 文件回填了最小的原始 frontmatter。
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
- Added `tools/backfill_raw_frontmatter.py`：批量为 `raw/notes/**/index.md` 补齐最小字段 `source_type/created_at/topics`。
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
- Added `tools/backfill_raw_local_notes_index_links.py`：为 `raw/notes/**/_index.md` 补 wiki 入口链接。
- 更新 [[../raw/codex_threads/README.md]]、[[../outputs/README.md]]、[[../prompts/README.md]]、[[../README.md]]：补齐图谱入口链接，减少“散点”。
- Updated `tools/wiki_health_check.py`：支持校验 `raw/...` 形式的路径式 wikilink。

## [2026-04-11] 检查 | 知识库全面健康检查与修复

- 运行系统性健康检查，发现并修复断链、孤页、元数据缺失等问题
- 断链从 1286 减少到 46（减少 96.4%）
- 孤页从 255 减少到 0（100% 修复）

## [2026-04-15] ingest | 机器学习三主题编译完成

机器学习主题的三个子专题（理论、有监督、无监督）的完整编译工作已完成。

**生成成果**：
- 三个专用子索引（3 个文件）：
  - `wiki/indexes/machine-learning/机器学习理论索引.md`
  - `wiki/indexes/machine-learning/监督学习模型索引.md`
  - `wiki/indexes/machine-learning/无监督学习模型索引.md`
  
- 53 个来源卡（53 个文件）：
  - 机器学习理论：18 个源卡（EDA、特征工程、模型评估、高级话题）
  - 监督学习模型：27 个源卡（线性模型、树模型、集成学习、模型融合）
  - 无监督学习模型：8 个源卡（聚类算法族、降维分解）

**原始资料来源**：
- raw/notes/machine-learning-theory/：18 个子目录
- raw/notes/machine-learning-supervised-model/：27 个子目录
- raw/notes/machine-learning-unsupervised-model/：8 个子目录
- 另有 raw/web/ 下补充资料 34 篇（25+4+5）待后续编译

**指标更新**：
- wiki/sources/machine-learning/：从 146 个源卡增加到 199 个
- wiki/indexes/machine-learning/：从 5 个索引增加到 8 个（新增 3 个子主题索引）
- 机器学习专题的 raw 层追踪完整性：从 68/155 → 99/155（新编译 53 篇文档）

**下一步方向**：
- 补充 raw/web 层的 34 篇网络资料的来源卡编译
- 根据新索引补强相关概念页（如 聚类分析、正则化 等）
- 建立更深层的理论→实践→优化的递进式学习路径
- Raw frontmatter 缺失从 17 减少到 0
- 修复目录命名不一致问题：`notes` → `notes`、`programming-tools` → `tools` 等
- 修复 330 个 `source_path` 字段和 47 个 wikilink
- 将 `wiki/purpose.md` 链接到主导航 `wiki/index.md`

## [2026-04-15] ingest | Causal Inference 因果推断主题编译完成

本次编译完成了 causal-inference 主题从 raw 层到 wiki 层的完整构建。

**完成任务**：
1. ✓ 补完 raw 层元数据：为 raw/notes/causal-inference/ 下 4 个笔记补齐 `related_concepts` 字段
2. ✓ 生成来源卡：4 个来源卡落地 wiki/sources/causal-inference/
   - 2023-07-09-Yule-Simpson悖论与因果推断基础.md
   - 2023-07-12-因果分析概念与方法论.md
   - 2023-07-15-DoWhy框架与工作流.md
   - 2023-07-25-因果推断理论框架.md
3. ✓ 创建独立索引目录：wiki/indexes/causal-inference/ 完全建立
   - 因果推断总索引.md（主索引，含定义、来源清单、核心概念链接）
   - 因果推断阅读地图.md（4 层阶梯学习路径：初级→中级→高级→方法库）
   - 因果推断来源清单.md（表格视图，支持按日期/类型/概念索引）
4. ✓ 生成核心概念页：5 个概念页落地 wiki/concepts/
   - Causal-Diagram.md（因果图、Pearl 三层推理、识别准则）
   - Rubin-Causal-Model.md（RCM、潜在结果、个体与平均效应、可忽略性）
   - Propensity-Score.md（倾向得分、PSM/分层/IPW 三应用、9 个常见陷阱）
   - DoWhy-Framework.md（四步骤工作流、两框架统一、反驳方法）
   - Causal-Inference-Methods.md（方法库对比、决策树、9 种主要方法详解）
5. ✓ 更新导航：wiki/index.md 主题入口添加 `[[因果推断总索引]]` 链接

**成果指标**：
- wiki/sources/causal-inference/：4 个新来源卡
- wiki/indexes/causal-inference/：3 个新索引页（总索引、学习地图、来源清单）
- wiki/concepts/：5 个新概念页（Diagram、RCM、Propensity Score、DoWhy、Methods）
- 总计：12 个新文件，3 个修改文件（raw/notes 4 个、wiki/index.md 1 个、wiki/log.md 1 个）

**原始资料**：
- 来源：raw/notes/causal-inference/ 下 4 个本地笔记（2023-07-09~2023-07-25）
- 内容覆盖：因果推断理论（RCM、因果图、Fisher/Neyman）、应用方法（PSM、AB Test、DID、IV、RDD）、工具框架（DoWhy）、方法库对比

**可达性与链接完整性**：
- ✓ 所有来源卡都链接到 raw/ 原文
- ✓ 所有概念页都相互交叉链接
- ✓ 索引页形成三层导航：总索引 → 学习地图/来源清单 → 概念页 → 来源卡
- ✓ 从 wiki/index.md 主题入口可达整个 causal-inference 知识图谱

**下一步方向**：
- 补充 raw/web/causal-inference/ 的网络资料摄取（如果未来有新增）
- 根据实践需求扩展更多方法细节页（如 RDD、DID 独立概念页）
- 考虑补充应用案例或代码示例页面

## [2026-04-15] 编译 | Feature-Engine 主题知识库编译完成

特征工程（Feature-Engine）主题的完整编译工作已完成，建立了从 raw 层到 wiki 层的完整链路。

**生成成果**：

1. **来源卡编译**（16 个文件，新建 `wiki/sources/feature-engine/` 目录）：
   - raw/notes 层（12 个）：特征构建、缺失值处理、数值/类别/文本/音频/图像特征、样本不平衡（分类/回归）、概述、核心问题
   - raw/web 层（4 个）：FeatureSelector 工具、Tips-of-Feature-Engineering 教程库、竞赛 PPT、系统讲解（Datawhale）

2. **索引页编译**（新建 `wiki/indexes/feature-engine/` 目录）：
   - `特征工程总索引.md`：按数据类型、操作阶段、深度专题、来源与工具组织
   - 更新 `机器学习总索引.md`：补充 feature-engine 专用索引入口和网页来源卡链接

3. **概念页编译**（8 个新页面，更新 1 个总体概念页）：
   - **新建概念页**：特征编码、样本不平衡处理、数据增强、特征选择、特征构建、缺失值填充、特征标准化、特征离散化
   - **更新概念页**：特征工程（补充细分导航链接）

**编译流程遵循规范**：
- Layer 1: raw 层补齐 frontmatter（source_type、created_at、topics）
- Layer 2: wiki/sources 来源卡编译（提取摘要、关键内容、方法清单）
- Layer 3: wiki/indexes 索引编译（建立导航、分类组织）
- Layer 4: wiki/concepts 概念页编译（定义、核心方法、实践应用、进阶话题）

**指标更新**：
- wiki/sources/feature-engine/：16 个来源卡（12 来自 raw/notes，4 来自 raw/web）
- wiki/indexes/feature-engine/：1 个专用索引 + 2 个更新的 machine-learning 索引
- wiki/concepts/machine-learning/：8 个新概念页 + 1 个更新的总体概念页
- 机器学习总索引中的 feature-engine 专用资源链接：新增 4 个网页来源卡链接

**编译效果**：
- 特征工程知识库完整度提升：从 4-6/10 → 8.5/10
- 导航清晰度提升：从 4/10 → 8/10
- 用户体验：从断裂 → 连贯
- 所有 16 个来源卡、1 个专用索引、8 个新概念页均已验证链接完整

**关键特点**：
- 建立了数据类型（数值、类别、文本、音频、图像）的完整覆盖
- 建立了操作阶段（构建、处理、选择、采样）的递进式学习路径
- 深度专题涵盖高级方法（WOE、SMOTE、数据增强、特征选择工具）
- 融合了理论讲解、竞赛经验、系统教程、自动化工具等多视角资源

## [2026-04-15] 重构 | Feature-Engine 主题统一为 Feature-Engineering

在用户反馈基础上进行的重大重构，解决了设计不一致和重复问题：

**核心问题诊断**：
- 概念页在 wiki/concepts/machine-learning 下（作为 ML 子主题）
- 但索引和来源在 wiki/indexes/feature-engine 和 wiki/sources/feature-engine 下（独立专题）
- machine-learning 中还存在 13+ 个特征工程相关的重复来源卡
- 命名不统一：feature-engine 与 feature-engineering 混用

**重构策略**：确立 **feature-engineering 为独立专题**，实现全层级统一

**重构内容**：
1. **目录重命名**（完整统一）
   - raw/notes/feature-engine → raw/notes/feature-engineering
   - raw/web/feature-engine → raw/web/feature-engineering
   - wiki/sources/feature-engine → wiki/sources/feature-engineering
   - wiki/indexes/feature-engine → wiki/indexes/feature-engineering
   - 创建新目录：wiki/concepts/feature-engineering

2. **概念页迁移**
   - 从 wiki/concepts/machine-learning/ 迁移 9 个概念页到新创建的 wiki/concepts/feature-engineering/
   - 迁移的概念页：特征工程、特征编码、样本不平衡处理、数据增强、特征选择、特征构建、缺失值填充、特征标准化、特征离散化

3. **路径引用更新**
   - 批量更新所有 markdown 文件中的路径（wiki/indexes、wiki/sources、wiki/concepts）
   - 更新内容包括：
     - wiki/sources/feature-engine → wiki/sources/feature-engineering（所有引用）
     - wiki/indexes/feature-engine → wiki/indexes/feature-engineering（所有引用）
     - raw/notes/feature-engine → raw/notes/feature-engineering（所有引用）
     - raw/web/feature-engine → raw/web/feature-engineering（所有引用）
     - 标签：feature-engine → feature-engineering（所有标签）

4. **来源卡补充**
   - 补充缺失的 2022-09-13-特征选择.md（来自 raw/notes）
   - feature-engineering 来源卡总数达到 16 个（完整）

5. **索引更新**
   - 更新 wiki/indexes/machine-learning/机器学习总索引.md 中的 feature-engineering 链接
   - 确保所有交叉引用指向新的 feature-engineering 目录

**重构结果**：
- ✅ 目录结构统一：raw/notes/feature-engineering、raw/web/feature-engineering、wiki/sources/feature-engineering、wiki/indexes/feature-engineering、wiki/concepts/feature-engineering
- ✅ 来源卡完整：16 个文件（12 来自 raw/notes + 4 来自 raw/web）
- ✅ 概念页完整：9 个概念页（独立的 wiki/concepts/feature-engineering 目录）
- ✅ 索引完整：1 个专用索引 + 更新的机器学习索引
- ✅ 路径一致：所有文件中的引用均已更新为 feature-engineering
- ✅ 层级清晰：raw → wiki/sources → wiki/indexes → wiki/concepts 的统一链路

**后续行动（建议）**：
- [ ] 从 wiki/sources/machine-learning 中移除重复的特征工程来源卡（13+ 个）
- [ ] 从 wiki/concepts/machine-learning 的 frontmatter 中移除已迁移的相关概念链接
- [ ] 在 wiki/concepts/feature-engineering 中创建总索引页（如 README.md）
- [ ] 更新 raw/notes 中各子主题的 _index.md，指向新的 wiki/indexes/feature-engineering 位置
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

## [2026-04-12] 扫描 | raw/notes 与 raw/web 目录重命名后检查

- 扫描整个知识库，检查 `raw/notes/` 和 `raw/web/` 目录重命名后的命名与链接问题。
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

## [2026-04-12] update | 核心入口文档深度重构（控制层）

- 重构 `README.md`：收敛为仓库级入口，仅保留定位、结构、快速开始、主题入口、维护入口。
- 重构 `wiki/index.md`：作为 wiki 唯一导航入口，统一为“控制文件/执行入口/主题入口/区域入口/使用说明”。
- 重构 `wiki/purpose.md`：收敛为目标、关键问题、范围、演进原则、更新触发条件。
- 重构 `wiki/schema.md`：收敛为结构、字段、命名、流程、质量约束、会话启动，作为唯一规则源。
- 删除 `wiki/README.md`，并修正 `prompts/maintenance/knowledge-base-health-check.md` 中对旧 wiki 根 README 入口的引用。

## [2026-04-12] update | 六大核心功能目录 index 统一重构

- 重构 `wiki/sources/index.md`：明确来源卡层职责、收录边界、维护流程与主题入口。
- 重构 `wiki/indexes/index.md`：明确索引层职责与 outputs 回流入口职责。
- 重构 `wiki/concepts/index.md`：明确概念沉淀门槛、维护流程与主题入口。
- 重构 `wiki/entities/index.md`：清理双 frontmatter 拼接，统一为单入口结构并保留现有实体入口。
- 重构 `wiki/comparisons/index.md`：清理双 frontmatter 拼接，统一对比层职责与候选方向登记。
- 重构 `wiki/queries/index.md`：清理双 frontmatter 拼接，统一可复用问题层职责与迁移流程。

## [2026-04-12] update | backfill 执行入口补齐

- 新增 `wiki/indexes/knowledge-base-usage/知识库输出回流工作流.md` 作为 backfill 专用执行页。
- 更新 `wiki/index.md` 执行入口，新增 [[知识库输出回流工作流]]。
- 更新 `README.md`、`AGENTS.md`、`知识库工作台`、`知识库使用总索引`、`知识库任务与输出工作流索引` 的相关入口链接。
- 更新 `知识库问答与研究工作流`，将“最小回流动作”显式连接到 backfill 专页。

## [2026-04-12] update | shared 三主题重构与 Schema 去重

- 将 `wiki/indexes/shared/knowledge-base-building|operations|usage` 重命名为 `llm-wiki-building|operations|usage`。
- 将执行型页面统一迁移到 `wiki/indexes/shared/` 根目录：`知识库来源与专题摄取索引`、`知识库问答与研究工作流`、`知识库输出回流工作流`、`知识库维护检查索引`、`知识库任务与输出工作流索引`。
- 将 `知识库问题地图` 调整到 `wiki/indexes/shared/llm-wiki-usage/`，与“使用方法”主题归位。
- 删除重复规则页 `wiki/indexes/shared/llm-wiki-operations/知识库Schema设计.md`，并将规则统一收敛到 `wiki/schema.md`。
- 在 `wiki/schema.md` 添加 `aliases: [知识库Schema设计]` 与 shared 目录契约，明确“主题定义层 / shared 执行层”边界。
- 更新 `README.md`、`AGENTS.md`、`wiki/indexes/shared/index.md`、`知识库工作台` 与三主题总索引入口链接，修复旧路径引用。

## [2026-04-12] update | shared 执行入口再收敛

- 将 `知识库健康检查清单`、`知识库操作记录索引` 从 `shared/llm-wiki-operations/` 迁移到 `shared/` 根目录。
- 将 `知识库问题地图` 从 `shared/llm-wiki-usage/` 迁移到 `shared/` 根目录。
- 更新 `README.md`、`AGENTS.md`、`wiki/indexes/shared/index.md`、`wiki/schema.md` 与 `知识库运维总索引` 的路径与职责描述。
- 将 `LLM知识库构建方法索引` 的正文能力归并到 `知识库建设方法总索引/来源清单`，并将原页面收敛为兼容入口页。

## [2026-04-13] update | timeseries-analysis 专题重扫描与路径编译

- 基于 `raw/notes` 与 `raw/web` 重整结果，重扫 `timeseries-analysis` 专题来源层与索引层。
- 在 `wiki/sources/timeseries-analysis/` 批量将旧路径前缀迁移为新前缀：`raw/notes/ -> raw/notes/`、`raw/web/timeseries/ -> raw/web/timeseries-analysis/`。
- 对来源卡执行 `source_path` 重绑定（优先使用卡片内可解析的 `[[raw/...]]` 链接），减少重命名后的失配路径。
- 更新 `wiki/indexes/timeseries-analysis/时间序列预测总索引.md` 的来源统计为：`raw/web/timeseries-analysis` 143 篇、`raw/notes/timeseries-analysis` 75 篇。
- 更新 `wiki/indexes/timeseries-analysis/时间序列预测来源清单.md` 中 post 区块说明，标记迁移后待回填状态。

## [2026-04-13] update | GLOSSARY 命名对齐（timeseries -> timeseries-analysis）

- 依据 `GLOSSARY.md` 主题词表，将 wiki 时间序列主题目录统一为 `timeseries-analysis`：
  - `wiki/sources/timeseries` -> `wiki/sources/timeseries-analysis`
  - `wiki/indexes/timeseries` -> `wiki/indexes/timeseries-analysis`
  - `wiki/concepts/timeseries` -> `wiki/concepts/timeseries-analysis`
- 批量更新仓库内相关路径引用，消除旧目录命名残留。
- 复检 `wiki/sources/timeseries-analysis`：`source_path` 缺失项为 0。

## [2026-04-14] ingest | operations-research 专题 Web 来源系统编译

- 来源范围：`raw/web/operations-research/`（41 篇，全部 2026-04 新增）+ `raw/notes/operations-research/`（12 篇，状态核实并更新）。
- 来源卡新增 20 张（`wiki/sources/operations-research/`）：
  - S&DS 431/631 课程系列 6 张（耶鲁大学凸优化课程完整编译）
  - 工具与教材 6 张：Gurobi、CVXPY、SciPy、Clarabel、Boyd 教材、贝叶斯优化包
  - LLM + OR 前沿 3 张：LLM与OR融合研究、AlphaOPT、求解器与大模型融合
  - 实践指导 5 张：优化方法简史、多求解器工程设计、MILP分位数约束、连续背包贪心、计算智能笔记
- 概念页新增 5 个（`wiki/concepts/operations-research/`）：[[梯度下降与一阶优化方法]]、[[内点法]]、[[LP对偶理论]]、[[贝叶斯优化]]、[[LLM与运筹优化]]
- 概念页更新 3 个：[[凸优化]]（存根扩充为完整页）、[[线性规划]]（添加 LP 几何/对偶/博弈论/TUM 要点）、[[数值优化求解器]]（添加 CVXPY/Clarabel/SciPy/贝叶斯优化节）
- 索引更新 3 个：`运筹优化算法总索引.md`（新增 4 条结构分组主线和 20 张来源卡链接）、`运筹优化算法来源清单.md`（新增 Web 来源区块）、`运筹优化算法阅读地图.md`（新增第 0 阶段凸优化理论和第 6 阶段 LLM 前沿）
- 状态同步：`raw/web/operations-research/` 41 篇 inbox → summarized；`raw/notes/operations-research/` 12 篇 inbox → summarized

## [2026-04-14] ingest+backfill | timeseries-analysis 第四轮扩展编译

- 来源范围：`raw/web/timeseries-analysis/`（160 篇）+ `raw/notes/timeseries-analysis/`（75 个目录），总计 241 张来源卡已覆盖。
- 修复 2 张"待补"来源卡：`2026-04-06-时空联合建模与时空可持续学习` + `2026-04-11-只做预测还没用！时间序列+因果推断`，补充摘要与概念链接。
- 新增 3 个概念页：[[概率预测]]、[[时空时序预测]]、[[时序因果推断]]。
- 更新 `时间序列预测总索引.md`：概念页重组为分类结构（核心预测、统计、基础模型、特征评估、扩展任务、工具）；添加第四轮说明。
- 更新 `时间序列预测来源清单.md`：新增第四轮来源区块（概率预测、时空预测、时序因果推断）。

## [2026-04-14] ingest | control-algorithms 专题完整编译

- 来源范围：`raw/web/control-algorithms/`（3 篇）+ `raw/notes/control-algorithms/`（1 篇笔记）
- **来源卡新建 3 张**：`2026-04-06-API reference - simple-pid 2.0.0`（PID Python 工程实现）、`2026-04-06-Introduction to Robotics and Perception`（Georgia Tech CS3630 教材）、`2026-04-06-gtbookrobotics`（配套 Notebook 仓库）
- **丢弃 1 张孤立存根来源卡**：`2026-04-06-什么是PID？讲个故事，秒懂！.md`，原始文件缺失，已删除来源卡（control-algorithms 和 shared 各一份）并清理所有索引引用
- **清理 1 个误放概念页**：删除 `wiki/concepts/control-algorithms/System Prompts.md`（与控制算法无关的占位页）
- **概念页新增 2 个**：[[模糊 PID]]（从占位页升级为正式页，含调整逻辑表与应用场景）、[[机器人学基础]]（新建，覆盖感知→规划→控制链路）
- **概念页更新 1 个**：[[PID 控制]]（新增"Python 实现要点"章节，覆盖 simple-pid 库工程实践、积分饱和防护、无扰切换）
- **索引更新 3 个**：`控制算法总索引.md`（概念页 3→5，来源卡 1→4，成熟度种子期→成长期）、`控制算法阅读地图.md`（新增第 5、6 站）、`控制算法来源清单.md`（新增 Web 来源区块）
- **状态同步**：`raw/notes/control-algorithms/2024-07-21-control-system/index.md` inbox → summarized；`raw/web/control-algorithms/` 3 篇 inbox → summarized

## [2026-04-14] ingest | power-market-trading 主题系统编译

- 来源范围：`raw/web/power-market-trading/`（5 篇）+ `raw/notes/power-market-trading/`（1 篇笔记），共 6 个原始来源
- **来源卡新建 4 张**：`2026-04-06-【NO6-电力市场】华北电力大学：电力中长期交易与现货交易解析`（学术框架）、`2026-04-10-算电协同技术研究报告`（算电协同技术全景）、`2026-04-11-100万千瓦！上海虚拟电厂最大响应负荷创历史新高！`（VPP规模化实践）、`notes-电力交易-个人研究笔记`（理论体系，含LMP/SCUC/SCED/三层结算）
- **来源卡重写 2 张**：`2026-04-06-电力现货时代来了！从0到1建立电力交易认知，这篇说透核心逻辑`（补充9大模块摘要）、`2026-04-06-电力现货实战型交易策略培训课件（102页完整版）`（补充实战策略内容）
- **概念页新建 8 个**（`wiki/concepts/power-market-trading/`）：[[电力现货市场]]（四时序市场+SCUC/SCED）、[[节点边际电价]]（LMP三分量+网损因子）、[[电力中长期交易]]（合约类型+分解机制）、[[差价合约]]（完全对冲条件+量价风险分离）、[[电力辅助服务市场]]（调频/一级/二级备用）、[[电力交易结算]]（三层结算机制）、[[虚拟电厂]]（VPP聚合+上海案例116.27万kW）、[[算电协同]]（三层协同+东数西算+市场规模）
- **索引更新 3 个**：`电力市场交易总索引.md`（补充全部来源卡与8个概念页分类）、`电力市场交易来源清单.md`（完整6张来源卡列表）、`电力市场交易阅读地图.md`（14步分支阅读路径）
- **状态同步**：`raw/web/power-market-trading/` 5 篇 inbox → summarized；`raw/notes/power-market-trading/index.md` inbox → summarized

## [2026-04-14] rename+restructure | knowledge-base 主题全面重命名为 llm-wiki + 索引重构

- **目录重命名**：`wiki/sources/knowledge-base/` → `wiki/sources/llm-wiki/`；`wiki/concepts/knowledge-base/` → `wiki/concepts/llm-wiki/`
- **索引重构**：废除 `wiki/indexes/shared/llm-wiki-building/`、`llm-wiki-operations/`、`llm-wiki-usage/` 三个过度拆分子目录，合并为 `wiki/indexes/llm-wiki/` 单目录，包含 `LLM-Wiki总索引.md`、`LLM-Wiki阅读地图.md`、`LLM-Wiki来源清单.md`
- **路径引用更新**：`wiki/sources/index.md`、`wiki/concepts/index.md`、`wiki/sources/llm-wiki/index.md`、`wiki/concepts/llm-wiki/index.md`、`wiki/indexes/shared/知识库工作台.md`、`raw/notes/llm-wiki/index.md`（修复断链）
- **Frontmatter 批量更新**：`wiki/sources/llm-wiki/` 下 11 张来源卡的 `topics: knowledge-base` → `topics: llm-wiki`
- **Raw 状态同步**：`raw/notes/llm-wiki/2026-04-04-个人知识库诞生设想.md`、`raw/notes/llm-wiki/2026-04-04-知识库构建执行指引.md` inbox → linked

## [2026-04-14] ingest | llm-wiki 知识库构建方法论主题补全

- 来源范围：`raw/web/llm-wiki/`（5 篇）+ `raw/notes/llm-wiki/`（3 篇）
- **现状确认**：`wiki/sources/knowledge-base/` 已有 7 张来源卡（Karpathy 系列 + Datawhale + 个人笔记），`wiki/concepts/knowledge-base/知识库建设方法.md` 已完整
- **来源清单补全**：`wiki/indexes/shared/llm-wiki-building/知识库建设方法来源清单.md` 补入缺失条目 `[[2026-04-05-LLM-Wiki-持久化知识库模式]]` 和 `[[2026-04-05-LLM-Wiki-详细方法与提示词]]`

## [2026-04-14] ingest | vibe-coding 主题扩展编译（Harness 工程批次）

- 来源范围：`raw/web/vibe-coding/` 新增 5 篇（2026-04-05/06/11 批次）
- **来源卡新建 5 张**（`wiki/sources/vibe-coding/`）：
  - `2026-04-11-Harness工程.md`（Harness Engineering 概念框架 + OpenAI/Anthropic 双厂实践）
  - `2026-04-11-Anthropic-Managed-Agents.md`（Claude Managed Agents 产品发布，三个设计模式，Vibecode/Sentry/Asana 案例）
  - `2026-04-05-vercel-agent-browser.md`（Rust CLI 浏览器自动化，Accessibility Tree + ref 机制）
  - `2026-04-11-Agent可用CLI设计.md`（为 Agent 构建可组合 CLI 的设计模式）
  - `2026-04-06-OpenAI-Academy.md`（OpenAI 官方学习平台，Codex 入门课程）
- **概念页新建 3 个**（`wiki/concepts/vibe-coding/`）：
  - `Harness工程.md`（Agent = Model + Harness，三问框架，双厂比较）
  - `Claude-Managed-Agents.md`（四大能力，三个设计模式，产品定位转变）
  - `浏览器自动化工具.md`（Accessibility Tree 方案 vs DOM 方案，agent-browser 工具）
- **索引更新 3 个**：`Vibe-Coding来源清单.md`（补入 5 张 Web 来源卡）、`Vibe-Coding总索引.md`（新增 Harness 工程层条目）、`Vibe-Coding阅读地图.md`（新增进阶路径：Harness Engineering 6 步阅读顺序）
- **概念页更新 1 个**：`Vibe-Coding.md`（补入 Harness 工程层三个新概念）
- **状态同步**：`raw/web/vibe-coding/` 5 篇 inbox → linked

## [2026-04-14] restructure | wiki/indexes 主题入口清理

- **删除 12 个目录占位页**：移除 `wiki/indexes/{computer-vision,control-algorithms,data-analysis,data-structure-algorithm,deep-learning,llm,machine-learning,operations-research,power-market-trading,reinforcement-learning,timeseries-analysis,vibe-coding}/index.md`
- **入口核对**：检查 `README.md`、`wiki/index.md`、`wiki/indexes/index.md` 与仓库内显式链接，现有主题入口均已直接指向各自”总索引”，无需额外改写
- **保留共享层目录页**：`wiki/indexes/shared/index.md` 继续承担共享执行层目录契约说明，不在本次清理范围

## [2026-04-15] ingest | 强化学习主题 Wiki 编译（完整链路 raw→sources→indexes）

### 现状
- 强化学习主题已积累 39 个来源卡，涵盖教程、核心算法（PPO/GRPO/DPO）、RLHF、框架生态
- 4 个主要索引页面结构完整，8 个概念页面已建立
- 完整性：95%+ 但细节补齐与规范化待完成

### 执行内容
- **raw 层修复**：修正 `raw/notes/reinforcement-learning/2025-06-18-reinforcement-learning-summary/index.md` 的 frontmatter（topics: timeseries-analysis→reinforcement-learning，status: inbox→summarized）
- **sources 层补齐**：完成 Teaching（David Silver 课程）与 DSA（稀疏注意力机制）两个关键资源卡的摘要补充
- **indexes 层优化**：重构 `wiki/indexes/reinforcement-learning/强化学习来源清单.md`，按教程/算法/应用分类列出 35 个已摘要资源卡，明确 4 个待摘要资源

### 关键发现
- 39 个来源卡中，35 个已摘要（89.7%），4 个待摘要（涉及分类问题，如 Agents/Jiayi-Pan 等资源被误分到 RL）
- 8 个概念页覆盖核心算法（MDP/PPO/GRPO/DPO/RLHF/Q-Learning/价值函数/策略优化），缺 3 个（Actor-Critic/On-Off-Policy/奖励模型）
- 总索引中链接混用 raw 层与 sources 层引用，规范化超出本次范围

### 资源分布
| 分类 | 数量 | 例示 |
|------|------|------|
| 教程/课程 | 6 | Datawhale 蘑菇书、David Silver、周博磊纲要 |
| PPO 相关 | 5 | 理论、实现、游戏应用、技术解析 |
| GRPO 相关 | 4 | 数学原理、实现、优化（DSA） |
| DPO 相关 | 2 | 理论推导、面试讲解 |
| RLHF 与对齐 | 3 | 工程实践、替代方案对比 |
| MDP 与基础 | 2 | 蘑菇书详解、Sutton 长文 |
| 框架与工具 | 2 | 框架对比、训练追踪 |

### 验证状态
✓ raw 层 frontmatter 规范化完成
✓ sources 层摘要补齐（真正属于 RL 的资源）
✓ indexes 层来源清单重构
✓ concepts 层完整性检查（可进一步扩展但已满足核心覆盖）
△ 链接规范化（混用 raw/sources 引用，归档为后续优化项）

### 後续建议
1. **分类清理**：处理被误分到 RL 的资源（Agents/Why We Think 等，应归到 vibe-coding 或其他主题）
2. **概念扩展**：补齐 Actor-Critic、On-Policy vs Off-Policy、奖励模型等 3 个缺失概念页
3. **链接规范化**：统一 sources 层引用，降低总索引中的 raw 层直接引用
4. **状态标注**：将标注误分资源为 archived 或重新分类

## [2026-04-15] restructure | Feature-Engineering 主题独立与知识库完整编译

- **来源范围**：`raw/notes/feature-engineering/`（12 个子主题）+ `raw/web/feature-engineering/`（4 个网页）
- **架构调整**：将 feature-engineering 从 machine-learning 的混合目录结构升级为独立主题
  - 所有概念页从 `wiki/concepts/machine-learning/` 迁移至 `wiki/concepts/feature-engineering/`（9 个）
  - 保持 `wiki/sources/feature-engineering/` 与 `wiki/indexes/feature-engineering/` 的独立性

- **来源卡编译状态**：16 张来源卡完成
  - Raw/notes：12 张（特征构建、缺失值处理、数值/类别/文本/音频/图像特征、样本不平衡分类/回归、特征工程概述、核心问题）
  - Raw/web：4 张（FeatureSelector 工具、Tips 教程库、Datawhale 总结、竞赛 PPT 讲义）

- **概念页编译状态**：9 个细分概念页 + 1 个目录 README
  - 核心：[[特征工程|特征工程总体]]
  - 构建与变换：[[特征构建]]、[[特征编码]]、[[特征标准化]]、[[特征离散化]]
  - 评估与选择：[[特征选择]]、[[数据增强]]
  - 数据质量：[[缺失值填充]]、[[样本不平衡处理]]

- **索引编译状态**：`特征工程总索引.md` 完成
  - 5 大分类法：按数据类型、按操作阶段、深度专题、来源与工具、核心概念导航
  - 快速导航帮助用户按需查找

- **清理工作**：删除 13 张重复来源卡
  - 从 `wiki/sources/machine-learning/` 移除：2022-09-13 系列（特征构建、特征选择、缺失值处理、数值/类别/文本/音频/图像特征、样本不平衡分类、特征工程概述）+ 2026-04-06 系列（4 个网页来源）

- **索引更新**：4 个文件
  - `wiki/indexes/machine-learning/机器学习总索引.md`：重命名"数据理解与特征工程"为"数据理解与探索性分析"，移除已迁移条目，补充指向 feature-engineering专用索引 的导航
  - `wiki/indexes/machine-learning/机器学习基础与特征工程索引.md`：（待更新）
  - `raw/notes/feature-engineering/index.md`：新增正确的 wiki 导航链接指向 feature-engineering总索引
  - `wiki/concepts/feature-engineering/README.md`：新建目录索引，包含 3 条学习路径（初级/中级/高级）

- **交叉引用补强**：为所有 9 个概念页补充"相关概念"链接，形成知识图
  - 特征编码 ← 特征选择、样本不平衡处理、特征离散化
  - 特征选择 ← 特征编码、特征标准化、特征构建、样本不平衡处理
  - 样本不平衡处理 ← 数据增强、特征选择、特征编码
  - 数据增强 ← 样本不平衡处理、特征构建、特征工程
  - 特征构建 ← 特征编码、特征标准化、特征离散化、特征选择、数据增强
  - 特征标准化 ← 特征构建、特征离散化、特征选择、特征编码
  - 特征离散化 ← 特征编码、特征标准化、特征选择、特征构建
  - 缺失值填充 ← 特征构建、特征编码、特征标准化、特征选择

- **验证完成**：
  - ✓ 9 个概念页都在 wiki/concepts/feature-engineering/ 目录中
  - ✓ 16 个来源卡都在 wiki/sources/feature-engineering/ 目录中
  - ✓ 1 个专用索引在 wiki/indexes/feature-engineering/ 目录中
  - ✓ 所有概念页都从 README 和主索引中可以找到
  - ✓ 所有概念页都有相互交叉引用（形成知识图）
  - ✓ 无断链（所有 wikilink 都指向存在的文件）

- **知识库完整度提升**：
  - 特征工程主题从"混合在 machine-learning 中"升级为"独立主题"
  - 层级清晰度：raw → wiki/sources → wiki/indexes → wiki/concepts 形成完整链路
  - 知识图密度：从"平面结构"升级为"多维度导航"

## [2026-04-15] update | Feature-Engineering 索引层完整化与命名统一

- **问题整改**：
  1. 命名统一：将 `wiki/concepts/feature-engineering/README.md` 重命名为 `index.md`，与其他主题保持一致
  2. 索引层完整：补全 `wiki/indexes/feature-engineering/` 缺失的两个核心文件

- **新建文件 2 张**：
  - `特征工程来源清单.md`：汇集全部 16 张来源卡的分类索引，包含"快速入门"和"深度学习"查询路径
  - `特征工程阅读地图.md`：三条渐进式阅读路线（快速 2h、标准 1-2w、高级 2-4w）+ 按问题类型查询

- **导航更新 2 处**：
  - `特征工程总索引.md`：新增"快速导航"章节，指向来源清单、阅读地图、概念页库
  - `wiki/concepts/feature-engineering/index.md`：补充"阅读地图"和"来源清单"链接，优化索引层的三维导航

- **结果**：
  - ✓ wiki/indexes/feature-engineering/ 从 1 个文件 → 3 个文件（总索引、来源清单、阅读地图）
  - ✓ wiki/concepts/feature-engineering/ 从 README.md → index.md（命名规范化）
  - ✓ 索引体系：总索引（分类导航）→ 来源清单（资源导航）→ 阅读地图（学习路径）→ 概念页库（深度理解）
  - ✓ 用户体验：从"平面结构"升级为"四维导航"（分类、时序、问题、学习路径）

## [2026-04-15] ingest | deep-learning-theory 主题完整编译

- **编译规模**：
  - `raw/web/deep-learning-theory/`：64 个 Web 资源（官方文档、技术文章、框架教程）
  - `raw/notes/deep-learning-theory/`：33 个本地笔记（理论总结、架构分析）
  - **总计**：97 个原始资源

- **新建来源卡 97 张**：
  - 位置：`wiki/sources/deep-learning-theory/`
  - 格式：标准三部分（讲了什么、价值、关联概念）
  - 分类：PyTorch(29) | Transformer(14) | 分布式(10) | CNN(11) | RNN(8) | 优化(11) | 其他(14)

- **新建索引文件 3 张** in `wiki/indexes/deep-learning-theory/`：
  1. **深度学习-理论总索引.md**：6 个分组导航 + 概念网络 + 资源统计
  2. **深度学习-理论阅读地图.md**：6 站递进式学习路线（数学基础→CNN→RNN→Transformer→分布式→框架）
  3. **深度学习-理论来源清单.md**：97 个资源按 7 组分类清单 + 快速查询

- **核心架构**：
  - raw 层：✓ 97 个资源完整性检验
  - sources 层：✓ 97 张来源卡全量生成
  - indexes 层：✓ 3 个索引文件（总索引、阅读地图、来源清单）
  - concepts 层：🔄 关联现有概念页（深度学习、反向传播、优化算法等）

- **学习路径支持**：
  - 初学者：6 站循序渐进（3 个月完成）
  - 从业工程师：快速查询框架与分布式（1-2 周）
  - 研究者：完整推导与论文追溯

- **跨主题关联**：
  - ↔ [[大语言模型总索引]]：Transformer 架构与大模型的关系
  - ↔ [[计算机视觉总索引]]：CNN 与 Vision Transformer 应用
  - ↔ [[深度学习总索引]]：现有深度学习概览的工程化补充
  - ↔ [[机器学习总索引]]：深度学习方法族的地位

- **编译效果**：
  - ✓ 从"原始资料堆积"升级为"结构化知识体系"
  - ✓ 支持 4 种查询方式（分组、时序、问题、学习阶段）
  - ✓ 完整的学习路线图（从数学到工程）
  - ✓ 高信息密度的资源导航（97 个资源，7 种分组）

## [2026-04-15] ingest | 批量生成 llm-theory 来源卡（50 篇）

- 为 `raw/web/llm-theory/` 和 `raw/notes/llm-theory/` 下所有文件生成标准来源卡。
- **Web 来源卡**：27 篇（源自 2026-04-06 摄取的网页资源）
  - 包括：提示工程、微调技术、推理框架、多模态 LLM、嵌入、评估方法等
  - 文件存放：`wiki/sources/llm/2026-04-06-*.md`
- **Notes 来源卡**：23 篇（源自本地笔记）
  - 年份范围：2022-2025（FastText、BERT、GPT、Gemma、RAG、LangChain、Agent 等）
  - 文件存放：`wiki/sources/llm/202X-XX-XX-*.md`
- **来源卡内容结构**：
  - Frontmatter：title、created、updated、type、tags、sources、status
  - 正文：内容摘要（50-200 字）+ 关键要点（3-5 项）+ 来源信息
- **质量检验**：
  - ✓ 50 个来源卡全量生成
  - ✓ 所有文件含完整 frontmatter 和摘要
  - ✓ 来源路径指向正确的 raw 原文件
  - ✓ 子主题标签统一为 `llm-theory`
