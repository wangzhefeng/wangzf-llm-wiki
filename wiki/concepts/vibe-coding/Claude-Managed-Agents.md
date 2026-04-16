---
created_at: 2026-04-14
topics:
  - vibe-coding
  - agent-dev
related_concepts:
  - Harness工程
  - Agent智能体
  - Skills知识库
status: linked
---
# Claude Managed Agents

## 一句话定义

Claude Managed Agents 是 Anthropic 于 2026 年 4 月发布的官方 Harness 产品，以可组合 API 套件形式提供生产就绪的 Agent 运行环境，开发者只需定义任务、工具和护栏，其余基础设施由 Anthropic 托管。

## 核心要点

- **四大能力**：
  1. 生产级 Agent（沙箱/身份验证/工具执行全托管）
  2. 长运行会话（数小时自主工作，进度持久化，断线不丢状态）
  3. 多 Agent 协调（主 Agent 派生子 Agent，并行分解复杂任务）
  4. 可信治理（作用域权限、身份管理、执行追踪内置）

- **三个设计模式**：
  1. **使用 Claude 已知工具**：提供 bash 和文本编辑器等通用工具，让 Claude 自己组合解决方案，而非为每个任务设计专用工具
  2. **让 Claude 自主决策**：编排逻辑从 harness 转移到模型本身（通过代码执行工具），只有最终输出进入上下文窗口，降低 token 消耗
  3. **谨慎设置边界**：高安全/不可逆操作提升为专用工具（可拦截/审计/渲染确认 UI），而非全走 bash

- **产品定位转变**：Anthropic 从"模型 API 提供商"转型为"Agent 云服务商"，按 token + 每小时 $0.08 会话活跃时长计费

- **实测效果**：相比标准提示循环，任务成功率提升最多 10 个百分点；在最困难任务上提升幅度最大

- **实际案例**：Vibecode 开发速度提升 10x、Sentry 数周完成 bug-to-PR、Asana AI Teammates、Rakuten 企业 Agent 周内上线

## 代表来源

- [[2026-04-11-Anthropic-Managed-Agents]]
- [[2026-04-11-Harness工程]]

## 相关概念

- [[Harness工程]]：Claude Managed Agents 的底层理念
- [[Agent智能体]]：运行在 Managed Agents 上的执行主体
- [[2026-04-09-vibe-coding-skills]]：Managed Agents 中 Skills 的渐进式展开机制
- Vibe-Coding总索引
