---
created_at: 2026-04-06
topics:
  - 大语言模型
  - 智能体
related_concepts:
  - 工具调用
  - 规划
  - 上下文工程
status: inbox
---

# Agent（智能体）

## 定义

LLM Agent 是基于大语言模型的智能系统，能够感知环境、规划行动序列、使用外部工具来自主完成任务。

## 核心架构

```
感知 → 思考（LLM） → 行动（工具调用） → 观察结果 → 循环...
```

### 1. 核心组件

| 组件 | 功能 |
|------|------|
| **大脑（LLM）** | 理解任务、推理决策、生成行动 |
| **记忆（Memory）** | 存储历史信息、支持长期推理 |
| **规划（Planning）** | 分解复杂任务、制定策略 |
| **工具（Tools）** | 执行具体操作（搜索、代码执行、API 调用等） |

### 2. 工具调用（Function Calling）

LLM 生成结构化的函数调用，系统执行后返回结果：

```json
{
  "function": "search",
  "arguments": {"query": "2024年诺贝尔物理学奖"}
}
```

### 3. 规划方法

- **单步规划**: 一次生成一个行动
- **多步规划**: 提前规划完整行动序列
- **反思规划**: 根据执行结果调整计划

### 4. 记忆类型

- **短期记忆**: 当前对话上下文
- **长期记忆**: 向量数据库存储的历史信息
- **工作记忆**: 当前任务相关的中间状态

## 主流框架

### ReAct（Reasoning + Acting）

交替进行推理和行动：

```
Thought: 我需要计算这个数学问题
Action: Calculator["23 * 45"]
Observation: 1035
Thought: 现在我可以用这个结果...
```

### CAMEL 框架

多智能体协作框架，支持角色扮演的多 Agent 系统。

### Claude Code / Code Agent

完整 Code Agent 开发涉及：
- **ReAct**: 推理-行动循环
- **Function Calling**: 工具调用
- **上下文工程**: 管理上下文窗口
- **MCP（Model Context Protocol）**: 模型上下文协议
- **Task/Todo/Skills**: 任务管理和技能系统

## 多智能体系统

多个 Agent 协作完成复杂任务：

- **协作模式**: 多个 Agent 分工合作
- **竞争模式**: Agent 之间辩论或对抗
- **层级模式**: 主 Agent 调度子 Agent

## 应用场景

- **代码助手**: Claude Code、GitHub Copilot Workspace
- **研究助手**: 搜索、阅读、总结论文
- **数据分析**: 查询数据库、生成可视化
- **自动化工作流**: 邮件处理、日程安排

## 相关来源

- [[大语言模型专题来源]]
- [[2026-04-06-从零搓出一个Claude Code，一篇超详细的总结！]]
- [[2026-04-06-GitHub---datawhalechinahandy-multi-agent-This-is-a-multi-agent-tutorial-based-on]]
- [[2026-04-06-Agents]] — AI Agent 完整教材
- [[2026-04-06-Agents Companion]] — Agent 配套教材

## 相关概念

- [[ReAct]]
- [[RAG检索增强生成]]
- [[提示词工程]]
- [[上下文工程]]
