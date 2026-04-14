---
created_at: 2026-04-14
topics:
  - vibe-coding
  - agent-dev
related_concepts:
  - Agent智能体
  - Claude-Managed-Agents
  - 浏览器自动化工具
status: linked
---
# Harness 工程

## 一句话定义

Harness 工程是为 AI 模型搭建"工作环境"的工程学科，核心公式为 **Agent = Model + Harness**：模型提供智能，Harness 让这个智能可在生产中真正使用。

## 核心要点

- **Harness 回答三个问题**：AI 在哪干活（工作台/文件系统）、用什么干活（工具/沙箱）、怎么知道干得对不对（反馈/检查机制）

- **OpenAI 的 Harness 要素**：整理好的文件台（分层文档、精简 AGENTS.md）、可机读的错误信息（Linter 受众从人变 AI）、完整可观测性堆栈（日志/指标/UI 全暴露给 AI）、架构约束规则（依赖方向自动拦截）

- **Anthropic 的 Harness 要素**：生成器与评估器拆分、多维打分标准（质量/原创性/工艺/功能）、迭代 5-15 轮的反馈循环

- **上下文管理**：AI 记忆不是无限的，重要信息应存文件系统而非全塞上下文；定期运行 doc-gardening Agent 扫描过时文档

- **与传统工程的区别**：不是手把手教 AI，而是设计环境、设定标准、建立反馈——工程师角色从"写代码"变为"设计系统让 AI 写代码"

- **Mitchell Hashimoto 定义**：每当发现 Agent 犯了一个错误，就花时间设计方案使 Agent 永远不再犯同样的错误——这是 Harness 迭代的驱动力

## 代表来源

- [[2026-04-11-Harness工程]]
- [[2026-04-11-Anthropic-Managed-Agents]]
- [[2026-04-09-vibe-coding-agent]]

## 相关概念

- [[Claude-Managed-Agents]]：Anthropic 将 Harness 工程产品化的实现
- [[浏览器自动化工具]]：Harness 工具层的 Web 交互组件
- [[Agent智能体]]：Harness 承载的运行主体
- [[Vibe-Coding总索引]]
