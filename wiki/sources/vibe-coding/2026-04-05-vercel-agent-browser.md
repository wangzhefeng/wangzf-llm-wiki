---
source_type: web
source_url: https://github.com/vercel-labs/agent-browser
source_path: raw/web/vibe-coding/2026-04-05-vercel-labsagent-browser-Browser-automation-CLI-for-AI-agents.md
created_at: 2026-04-05
topics:
  - vibe-coding
  - programming-tools
related_concepts:
  - 浏览器自动化工具
  - Harness工程
status: linked
---
# 来源卡：vercel-labs/agent-browser：Browser automation CLI for AI agents

## 这份材料讲了什么

- 原文：[[raw/web/vibe-coding/2026-04-05-vercel-labsagent-browser-Browser-automation-CLI-for-AI-agents.md]]
- 来源：GitHub vercel-labs/agent-browser
- 类型：工具文档（README）

**agent-browser** 是 Vercel Labs 出品的原生 Rust CLI，专为 AI Agent 设计的浏览器自动化工具。

核心设计思路：用 **Accessibility Tree**（而非 DOM）作为页面表示，为 Agent 提供结构化页面快照（`snapshot` 命令），通过 `ref`（如 `@e2`）点击和填写元素，避免脆弱的 CSS 选择器。

主要命令分类：
- **导航**：`open`、`back`、`forward`、`refresh`
- **页面读取**：`snapshot`（获取可访问性树+ref）、`screenshot`（PNG截图+注释）
- **交互**：`click @ref`、`fill @ref "text"`、`key Enter`、`scroll`
- **高级**：`find`（自然语言元素定位）、`javascript`（执行 JS）、`pdf`（渲染 PDF）

以守护进程（daemon）方式运行，支持多标签管理（`tabs` 系列命令）。通过 Homebrew、npm 或 Cargo 安装。

## 价值是什么

提供了一个专为 AI Agent 优化的浏览器自动化接口——accessibility tree 方案比 DOM 操作更稳定，ref 机制让 LLM 能可靠地引用页面元素，是构建 Web 交互 Agent 的关键工具层。

## 连到哪些概念

- [[浏览器自动化工具]]
- [[Harness工程]]
- [[2026-04-09-vibe-coding-tools]]
- [[Vibe-Coding总索引]]
