---
source_type: local_note
title: Codex 线程历史整理入口
created_at: 2026-04-07
topics:
  - Codex 工作流
  - 线程整理
related_concepts:
  - Codex skill 设计
status: inbox
---

# Codex 线程历史整理入口

本目录用于沉淀“该项目中 Codex 的历史线程整理稿”，目标不是记录知识库主题内容，而是为后续固化 Codex 工作流程、总结经验问题、提炼 skill 提供原始材料。

## 建议使用方式

1. 每个重要线程单独整理为一份 Markdown
2. 优先记录任务目标、做法、有效经验、失败点、可复用提示词或操作模式
3. 不要求保留完整对话原文，优先压缩为结构化总结
4. 后续如果需要，再从这些整理稿中抽取流程、反模式、检查清单与 skill 草案

## 建议命名

- 单线程整理：`YYYY-MM-DD-线程主题.md`
- 阶段汇总：`YYYY-MM-DD-codex-线程阶段汇总.md`

## 当前模板

- [线程总结模板](./线程总结模板.md)

## 与其他线程交互的提示词（可直接复用）

```md
请基于当前线程内容，并以 `/Users/wangzf/projects_ai/wangzf_kb/raw/codex_threads/README.md` 和 `/Users/wangzf/projects_ai/wangzf_kb/raw/codex_threads/线程总结模板.md` 的要求为准，帮我整理这条线程，供我后续沉淀到 `raw/codex_threads/` 目录中。

整理目标不是总结知识库主题内容，而是提炼这条线程对于“Codex 在该项目中的工作流程、有效经验、问题、可固化步骤、可提炼 skill 素材”的价值。

要求：
1. 不要机械复述整段对话，不要写流水账。
2. 重点提炼任务目标、实际完成内容、关键决策、有效做法、问题与摩擦点、对 Codex 工作流固化的启发。
3. 不明确的信息标注“未明确”，不要猜测。
4. 输出使用中文，结构完整，避免空话。
5. 如果某一节没有有效信息，写“无”或“未明确”。

请严格按 `线程总结模板.md` 的章节结构输出最终版 Markdown。
```

## 模板使用与结果保存方式

1. 在历史线程中使用上述提示词，拿到结构化总结。
2. 对照 [线程总结模板](./线程总结模板.md) 快速检查章节完整性。
3. 将最终 Markdown 保存到 `raw/codex_threads/`。

说明：本仓库根目录 `README.md` 位于 `/Users/wangzf/projects_ai/wangzf_kb/README.md`，线程总结文件应保存到同一仓库目录下的 `/Users/wangzf/projects_ai/wangzf_kb/raw/codex_threads/`。

## 线程总结文件命名规范

优先提取“线程主要内容主题”，命名格式：

- `YYYY-MM-DD-主题关键词.md`

建议：

- 主题关键词控制在 2 到 4 个词，直接描述主任务。
- 避免使用“杂项”“临时”“对话记录”等低信息量词。
- 同一天多个线程可在末尾补 `-v2` 或更具体主题词区分。

示例：

- `2026-04-07-codex-线程交接流程.md`
- `2026-04-07-codex-上下文压缩与回填.md`
- `2026-04-08-codex-skill提炼-反模式清单.md`
