---
created_at: 2026-04-11
topics:
  - 知识库维护
  - raw
  - assets
related_concepts:
  - 知识库维护检查索引
status: summarized
---

# 2026-04-11 raw/assets 分类修复动作记录

## 背景

本轮重点处理两类健康债务：

1. 文档中引用了 `raw/assets/attachments/*`，但目标文件缺失（渲染断图）。
2. `raw/assets/attachments/uncategorized/*` 目录下的附件已完成初步分类，但需要把引用路径同步改写到分类后的目录中。

## 执行

- `python3 tools/fix_missing_attachments_refs.py --apply`
  - 对缺失附件引用进行修复：
    - 若原文有外链：转换为标准 Markdown 图片 `![](url)`
    - 若无外链：替换为 `<!-- missing attachment: ... -->`
- `python3 tools/migrate_uncategorized_attachments.py --apply`
  - 将被引用的 `raw/assets/attachments/uncategorized/*` 按“引用来源主题”迁移到对应主题目录，并批量改写所有 `[[...]]` 引用路径。

## 结果

- 缺失附件引用：归零（不再出现 `<!-- missing attachment -->` 指向不存在的文件）
- `uncategorized` 迁移：已将 **395** 个被引用附件迁移到主题目录并完成改链
- `uncategorized` 剩余文件：当前剩余 **21** 个文件（未被任何 Markdown 引用，建议后续人工判定保留/归档）

## 待处理（建议）

- 未被引用的附件（约 92 个）需要确认：
  - 是否是“生成物/缓存”可归档到 `raw/assets/attachments/_generated/` 或 `_stash/`
  - 是否应在对应来源卡或概念页补入口（让资产可发现、可追溯）

## 2026-04-11 补入口回合（本次会话）

- 目标：将当时未被引用的附件（92 个）补齐入口，避免成为“暗资产”。
- 做法：在 `wiki/sources/<topic>/` 生成附件入口清单页，并通过目录 README 的自动索引形成入链。
- 入口页：
  - `wiki/sources/timeseries-analysis/附件入口清单-timeseries.md`
  - `wiki/sources/deeplearning/附件入口清单-deeplearning.md`
  - `wiki/sources/operations-research/附件入口清单-operations-research.md`
  - `wiki/sources/shared/附件入口清单-uncategorized.md`
  - `wiki/sources/shared/附件入口清单-attachments-root.md`

## 2026-04-11 附件目录规范化（本次会话）

- 将附件目录名与 wiki 主题 slug 对齐（减少长期维护成本）：
  - `raw/assets/attachments/computer-vision/` -> `raw/assets/attachments/computer-vision/`
  - `raw/assets/attachments/machine-learning/` -> `raw/assets/attachments/machinelearning/`
  - `raw/assets/attachments/reinforcement-learning/` -> `raw/assets/attachments/reinforcement-learning/`
  - `raw/assets/attachments/control_algorithms/` -> `raw/assets/attachments/control-algorithms/`
- 将剩余 `uncategorized/` 与根目录 `*.latex` 归并到 `raw/assets/attachments/shared/`：
  - `raw/assets/attachments/uncategorized/` -> `raw/assets/attachments/shared/uncategorized/`
  - `raw/assets/attachments/gif*.latex` -> `raw/assets/attachments/shared/latex/`
