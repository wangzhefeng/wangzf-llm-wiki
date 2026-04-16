---
created_at: 2026-04-08
topics:
  - AI 工作流
  - llm-knowledge-base
  - 用户协作
related_concepts:
  - 知识库工作台
  - Codex 工作流
status: linked
---

# LLM wiki 供 AI 和用户使用的方式、方法、流程总结

## 文档目标

这份总结关注的不是“知识库怎么建”，而是“建好之后，用户与 AI 如何围绕这套 LLM wiki 协作，才能稳定得到可回流、可追溯、可继续扩展的结果”。

主证据线程：

- `2026-04-07-llm-wiki-工作流补齐与-schema-固化线程总结.md`
- `2026-04-07-知识库健康检查线程整理.md`
- `2026-04-07-知识库搭建与工作流固化线程.md`
- `2026-04-07-Marp演示稿工作流线程总结.md`

## 适用场景

- 用户希望围绕现有 wiki 做问答、研究、维护、来源摄取、输出生成
- AI 需要在仓库内找到正确入口，而不是仅凭会话内容猜流程
- 需要明确 repo prompt、工作台、AGENTS 约束、未来 skill 的分工边界
- 需要把“单轮好回答”升级为“持续可复用协作”

## 流程总览

AI 和用户围绕这套 wiki 的协作链条，可以收束为：

`用户给目标与边界 -> AI 先读入口与规范 -> AI 找证据与现状 -> AI 落盘产物 -> AI 回链入口 -> AI 留日志或下一步起点`

这里最重要的不是“会不会回答”，而是“回答之后有没有真正写回仓库并形成下一轮入口”。

## 标准步骤

### 1. 用户先给任务目标、边界和入口

高质量输入通常包括：

- 当前要解决的问题或主题
- 这轮是构建、维护、问答、研究、摄取还是输出生成
- 应优先阅读的入口页、prompt、上轮结果或线程整理稿
- 约束条件，如只做 Markdown、不要脚本、是否允许 commit/push

线程经验很清楚：当用户直接点名关键文件、提示词或工作台入口时，AI 的执行质量明显更高。

### 2. AI 起步时先读 repo 内规范，而不是立刻给泛化答案

AI 的标准起步顺序应是：

- 读 `README.md`
- 读 `知识库工作台`
- 读相关总索引、阅读地图、维护清单或问题地图
- 读本轮点名的 prompt 文件
- 必要时再读最近一次 `outputs/answers/` 或 `outputs/logs/`

这一步是本项目里最重要的真实经验之一。repo 内 prompt、README、工作台已经构成半结构化操作规范，AI 需要先消费它们。

### 3. AI 默认执行链不是“答完就结束”，而是“答完还要落盘”

根据任务类型，落盘目标不同：

- 问答与研究：`outputs/answers/` 或 `outputs/syntheses/`
- 维护与巡检：`outputs/answers/` + `outputs/logs/`
- 来源摄取：`raw/` + `wiki/sources/` + 必要的索引与概念回写
- 演示稿生成：`outputs/slides/` + `outputs/figures/` + 工作流或入口页回链

多条线程都暴露出同一个风险：如果不把“写回仓库”当作默认收尾动作，AI 很容易停在一次性对话结果。

### 4. 用户与 AI 通过工作台、问题地图和最近结果进行迭代

- 用户下一轮维护前，先读最近一次健康检查结果
- 用户下一轮研究前，先读总索引、问题地图和上一轮答案/综述
- AI 做完本轮任务后，要补回链入口，让下一轮不必从零找文件

这意味着工作台和最近结果页不是装饰页，而是跨线程协作的真正连接器。

### 5. 不同任务类型使用不同的工作模式

这套 wiki 至少已经跑过 5 类使用方式：

- 主题构建：围绕 `raw -> sources -> indexes -> concepts`
- 维护检查：围绕 `lint -> 修复 -> 回写 -> 复验 -> 记录`
- 问答研究：围绕证据路径、结构化判断、`outputs/answers` 或 `outputs/syntheses`
- 来源摄取：围绕 intake prompt 和来源卡编译
- 输出生成：围绕 `answers -> slides -> figures`，Marp 线程是典型样例

所以“如何使用 LLM wiki”不是单一动作，而是一组按任务类型切换的工作模式。

## 输入与输出

用户常见输入：

- 明确主题、问题、优先级
- 关键入口文件或 prompt
- 是否直接实施、只总结、还是先诊断
- 是否要保存输出、保存到哪一层

AI 常见输出：

- 结构化回答
- 线程相关的 Markdown 产物
- `outputs/answers/`、`outputs/syntheses/`、`outputs/slides/`、`outputs/logs/`
- 更新后的入口页、工作流页、最近结果回链

## 角色分工

用户负责：

- 决定任务意图和范围
- 指出当前最重要的入口文件、上轮结果或模板
- 在关键边界上纠偏，例如删除约束、是否需要 repo 级约束、哪些结论需要沉淀

AI 负责：

- 先读仓库内规范和入口，而不是凭印象给方法
- 区分 repo prompt、共享工作流页、AGENTS 约束、技能候选材料的角色
- 把会话结果变成仓库内可继续消费的资产
- 明确说明本轮做了什么、如何验证、残余风险和下一步入口

## 常见失败点与反模式

- 用户没有点名入口，AI 也没有主动先读仓库规范，双方都在抽象层对话
- AI 把“已回答”误当成“已交付”，没有把结果写入 `outputs`
- 把 repo prompt 和 skill 混为一谈，导致不知道本轮规范来自哪里
- 只生成结果文件，不更新工作台、最近结果或共享入口，导致后续线程仍难接续
- 用户想要的是流程固化或工作流总结，AI 却继续写主题内容

## 当前仓库中的对应入口或文件

- [README.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/README.md)
- [知识库工作台.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库工作台.md)
- [知识库问答与研究工作流.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库问答与研究工作流.md)
- [知识库问题地图.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库问题地图.md)
- [prompts/README.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/README.md)
- [AGENTS.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/AGENTS.md)

## 从线程证据抽出的关键经验

- 用户直接给“目标 + 边界 + 入口文件”时，AI 更容易进入正确工作模式
- repo 内 prompt 已经足够像任务规范，AI 应优先读取并执行到落地
- 工作台、问题地图、最近结果和日志，是跨线程上下文传递的真正媒介
- 生成 slide、研究综述、健康检查、来源卡等不同产物时，收尾动作不同，但都必须回到仓库
- `AGENTS.md` 适合承接稳定规则，skill 适合承接可复用流程；两者不应互相替代

## 仍未固化的问题

- 这套协作模式已经相当清楚，但仍主要以页面、prompt 和线程经验存在，尚未完整抽象为正式 skill
- repo prompt、AGENTS 约束和未来 skill 的分层边界虽然已显现，但还缺一份专门的规则图
- 多轮使用后，哪些入口最稳定、哪些步骤最应强制化，还需要更多真实任务继续验证
