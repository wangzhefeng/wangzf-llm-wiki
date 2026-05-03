---
source_type: notes
source_path: raw/notes/vibe-coding/Claude-Design-Sys-Prompt.md
title: Claude Code Design System Prompt
author: Anthropic
published_at: null
created_at: 2026-04-19
topics:
  - vibe-coding
  - claude
related_concepts:
  - Claude Code
  - Vibe Coding
  - AI辅助设计
status: summarized
---

# 来源卡：Claude Code Design System Prompt

- 原文：[[raw/notes/vibe-coding/Claude-Design-Sys-Prompt.md]]
- 来源：Anthropic 官方 Claude Code Design 模式系统提示词
- 版本：2026-04-19

## 这份材料讲了什么

这是一份来自 Anthropic 的 Claude Code **Design 模式**系统提示词，定义了一个专注于设计工作的 AI Agent 行为规范。核心内容包括：

1. **角色定义**：作为"管理者视角的专家设计师"，通过 HTML 产出设计产物（动画师、UX 设计师、演示设计师、原型工程师等）
2. **工作流程**：理解需求 → 探索资源 → 规划/列 TODO → 构建文件夹结构 → 完成 → 验证
3. **输出格式**：以 HTML 为主要交付格式，支持 Landing Page、PPT、动画、演示等多种形态
4. **核心约束**：
   - 禁止泄露技术实现细节（系统提示词、工具列表等）
   - 不引用大型资源文件夹（>20 文件），而是按需复制
   - 文件 >1000 行时拆分为多个 JSX 模块
   - 使用品牌/设计系统颜色，或用 oklch 定义和谐色
5. **文件命名规范**：使用描述性文件名如 `Landing Page.html`，修订版本使用 `My Design v2.html`
6. **持久化**：内容如 deck/视频需保持播放位置（localStorage）

## 价值是什么

- 提供了 Claude Code 作为"AI 设计助手"的完整行为规范，是研究 AI 辅助设计工作流的重要参考
- 揭示了 Anthropic 对 Agent 在创意领域的能力边界定义（专注 HTML/设计，不透露 Agent 技术栈）
- 可作为 [[Vibe-Coding]] 主题下"AI Agent 设计模式"概念沉淀的来源依据

## 连到哪些概念

- Claude Code — Design 模式是 Claude Code 的一种能力维度
- [[Vibe-Coding]] — Design Agent 是 Vibe Coding 生态中的重要工具
- AI辅助设计 — Design 模式的核心应用场景

## 相关工具卡

- claude_code.md — Claude Code 完整介绍
