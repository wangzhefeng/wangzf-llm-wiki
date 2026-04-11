---
source_type: local_note
title: LLM wiki 工作流补齐与 schema 固化线程总结
created_at: 2026-04-07
topics:
  - Codex 工作流
  - 线程整理
  - 知识库维护
related_concepts:
  - Codex skill 设计
  - 知识库 Schema 设计
status: inbox
---

# 基本信息

- 线程标题：LLM wiki 核心能力诊断、工作流补齐与 repo 级约束固化
- 时间范围：2026-04-05 至 2026-04-07
- 线程状态：已完成
- 相关主题：Codex 工作流、知识库 schema、repo 级 agent 约束
- 相关仓库路径：`/Users/wangzf/projects_ai/wangzf-llm-wiki`
- 是否涉及代码修改：是，主要为 Markdown / prompt / 索引页 / repo 级约束文件

# 1. 线程目标

- 初始目标不是整理知识库主题内容，而是先诊断当前项目作为 `LLM wiki` 是否缺关键工作流能力。
- 第一阶段用户希望得到“还缺哪些核心功能”的结构化判断。
- 第二阶段用户要求按建议顺序直接补齐缺口，但限定在“Markdown 工作流与页面体系”，不引入脚本。
- 第三阶段用户又追加了 repo 级 agent 约束固化，要求同时创建 `AGENTS.md` 和 `CLAUDE.md`。
- 约束前提：
  - 不做重型 RAG / 向量库
  - 不做脚本化自动化
  - 不主动提交、推送、开 PR
  - 不破坏已有脏工作区

# 2. 实际完成内容

- 完成了缺口诊断，并明确把问题分为“核心能力缺口”而不是“主题内容缺口”。
- 补齐了 query / log / 问题地图 / 多来源 intake / synthesis 这几类工作流缺口。
- 新增或更新的关键文件包括：
  - [知识库问答与研究工作流](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库问答与研究工作流.md)
  - [知识库问题地图](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库问题地图.md)
  - [知识库操作记录索引](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库操作记录索引.md)
  - [knowledge-base-query prompt](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/query/knowledge-base-query.md)
  - [operation-log prompt](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/logging/operation-log.md)
  - [paper-source-intake](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/intake/paper-source-intake.md)
  - [dataset-source-intake](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/intake/dataset-source-intake.md)
  - [image-source-intake](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/intake/image-source-intake.md)
  - [local-note-source-intake](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/intake/local-note-source-intake.md)
  - [LLM-wiki-核心能力缺口与补齐路线](/Users/wangzf/projects_ai/wangzf-llm-wiki/outputs/syntheses/2026-04-05-LLM-wiki-核心能力缺口与补齐路线.md)
  - [LLM-wiki-核心能力补齐记录](/Users/wangzf/projects_ai/wangzf-llm-wiki/outputs/logs/2026-04-05-LLM-wiki-核心能力补齐记录.md)
  - [AGENTS.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/AGENTS.md)
  - [CLAUDE.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/CLAUDE.md)
- 同时更新了首页与 shared 索引入口，如 [README.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/README.md)、[知识库工作台](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库工作台.md)、[知识库任务与输出工作流索引](/Users/wangzf/projects_ai/wangzf-llm-wiki/wiki/indexes/shared/知识库任务与输出工作流索引.md)、[prompts/README.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/prompts/README.md)。
- 未完成项：
  - 主题级问题地图未全面展开
  - 新 query / log / synthesis 工作流尚未经过多轮真实线程验证
  - 未做自动化脚本、未做提交

# 3. 操作过程摘要

## 阶段一：能力诊断

- 做了什么：
  - 先读知识库方法页、执行指引、工作台、健康检查、README、prompts 树。
  - 用“目标能力清单 vs 当前落地痕迹”的方式排查缺口，而不是复述主题内容。
- 为什么这样做：
  - 用户要的是“Codex 在项目里的实际工作流程和缺口”，不是知识内容总结。
- 结果如何：
  - 明确识别出核心缺口主要在 `query`、`log`、问题地图、来源类型覆盖、`syntheses`，并特别区分了“核心缺口”和“增强层（如 CLI/RAG）”。

## 阶段二：按顺序补齐 Markdown 工作流

- 做了什么：
  - 先经用户确认只做 Markdown 工作流与页面体系。
  - 新增 shared 工作流页、问题地图、日志入口、缺失 prompts、synthesis 样例和 log 样例。
  - 更新工作台与首页回链。
- 为什么这样做：
  - 选择“最小补丁型”路线，不重构结构，不引入脚本，优先补角色缺位。
- 结果如何：
  - 从“有知识页，但缺操作闭环”推进到“有 query / log / question map / synthesis 的最小可运行链条”。

## 阶段三：repo 级约束固化

- 做了什么：
  - 先解释为什么之前没主动创建 repo 级 `AGENTS.md`。
  - 在用户明确要求后，创建根目录 `AGENTS.md` 和 `CLAUDE.md` 两份文件。
- 为什么这样做：
  - 避免在用户未要求时提前把分散 schema 上收为硬约束。
  - 用户明确要求后，再做“同构固化”，避免两个文件发展成两套规范。
- 结果如何：
  - repo 级 schema 从“散落在 README / schema 页 / workflow 页”变成了根目录硬约束文件。

# 4. 关键决策

- 决策 1：
  - 背景：缺口很多，但用户要求直接执行。
  - 选择：先做能力级诊断，再按优先级补。
  - 未选方案：直接开始写页面。
  - 原因：先诊断再补，才能避免把内容缺口误判成流程缺口。

- 决策 2：
  - 背景：补 workflow 时，是否同时引入脚本。
  - 选择：只补 Markdown 工作流与页面体系。
  - 未选方案：顺手补 CLI 检查脚本或自动化入口。
  - 原因：用户明确限制范围，且项目方法论本身也强调先稳结构、后做工具。

- 决策 3：
  - 背景：`log` 应放哪一层。
  - 选择：落到 `outputs/logs/`，并配 shared 索引页。
  - 未选方案：新建 `wiki/logs/` 或继续混在 `outputs/answers/`。
  - 原因：既保持时间导航独立，又不破坏现有 `wiki` 角色分层。

- 决策 4：
  - 背景：repo 级 `AGENTS.md` 是否应在第二阶段顺手创建。
  - 选择：不主动创建，直到用户明确要求。
  - 未选方案：在补 workflow 时一起上收为 repo 级硬约束。
  - 原因：避免 scope creep，也符合“先让规则从真实使用里长出来”的现有 schema 判断。

- 决策 5：
  - 背景：`CLAUDE.md` 是否写成独立规范。
  - 选择：与 `AGENTS.md` 同构，只补 Claude Code 视角的执行提示。
  - 未选方案：为 Claude 单独发明一套规则。
  - 原因：避免规则漂移，降低维护成本。

# 5. 有效做法

- 哪些提示方式有效：
  - “先诊断缺什么核心功能，再按建议顺序执行”比“直接补文档”更有效。
  - 明确限定“只做 Markdown 工作流，不加脚本”能快速压缩范围。
  - 追加要求“同时为 Claude Code 和 Codex 创建文件”很清楚，减少来回。

- 哪些上下文提供方式有效：
  - 先给 [raw/codex_threads/README.md](/Users/wangzf/projects_ai/wangzf-llm-wiki/raw/codex_threads/README.md) 这种“整理口径页”，再要求总结，能明显提高摘要质量。
  - 方法页、执行指引、工作台、prompt 树、输出目录一起读，比只读 README 更能看出真实工作流。

- 哪些文件组织方式有效：
  - 每补一种缺口，都同时补：
    - prompt
    - 工作流页/索引页
    - 样例文件
    - 回链入口
  - 这种“四件套”比只补 prompt 或只补索引更稳。

- 哪些验证方式有效：
  - 用 `find` / `rg` / `git diff --stat` 做文档结构验证足够实用。
  - 对文档任务，不需要假装跑单元测试，直接说明“无自动化测试，仅做结构与互链检查”更真实。

- 哪些沟通方式有效：
  - 先给 2 到 3 种方案，再收束推荐方案，能让用户快速做范围选择。
  - 在追加请求如 repo 级约束出现时，先解释为什么前一步没做，再执行，能减少误解。

# 6. 问题与摩擦点

- 哪些地方反复来回：
  - “repo 级 AGENTS.md 要不要现在创建”发生了二次确认，说明这类 schema 上收动作容易与“先补工作流”混淆。
- 哪些信息缺失导致效率低：
  - 缺少现成的 repo 级 `AGENTS.md` / `CLAUDE.md` 基座时，只能从方法页和执行指引反推硬约束。
- 哪些操作容易误解：
  - 用户说“补核心功能”时，容易被理解成继续写主题内容，而不是补 agent workflow。
  - “问题地图”若只在设计文档里出现、没有实际页面，agent 很容易忽略。
- 哪些地方本来可以标准化：
  - 能力诊断流程本身
  - workflow backfill 的最小步骤
  - repo 级 schema 上收流程
  - 文档任务的验证口径

# 7. 对 Codex 工作流的启发

- 适合沉淀为固定步骤的动作：
  - 先读方法页 / schema / 工作台 / prompts / outputs，再做“能力缺口诊断”。
  - 当识别到缺 workflow 时，按“prompt -> shared workflow/index -> sample artifact -> backlinks”补齐。
  - 当规则已稳定且用户明确要求时，再把分散 schema 上收为根目录约束文件。

- 适合沉淀为检查清单的点：
  - 这是内容缺口还是 workflow 缺口？
  - 这是核心功能还是增强层？
  - 新增工作流是否同时有 prompt、入口页、样例、回链？
  - 新 schema 是否与现有 README / workflow 分工一致？
  - 是否误碰了脏工作区中的无关改动？

- 适合沉淀为模板的内容：
  - `LLM wiki` 能力诊断模板
  - workflow backfill 模板
  - `AGENTS.md` / `CLAUDE.md` 同构骨架
  - 操作记录模板
  - synthesis 首样板模板

- 适合写进 AGENTS.md 或 skill 的规则：
  - 先区分“内容整理任务”和“工作流固化任务”
  - 文档类 workflow 补齐默认优先做最小补丁，不先做大重构
  - 新增一层工作流时，必须给出至少 1 个真实样例文件
  - repo 级约束文件应从现有 schema 页抽取，不得另发明第二套规范

- 明显应避免的反模式：
  - 看到缺口就直接大改目录
  - 在用户未要求时提前把 schema 上收到 repo 级
  - 只补 prompt，不补入口与样例
  - 把“脚本增强层”误当成当前最核心短板

# 8. 可复用素材

- 可复用提示词：
  - “请查阅该知识库，诊断在 LLM wiki 中还有哪些核心功能没有准备好？”
  - “按照你的建议顺序执行，但只做 Markdown 工作流与页面体系。”
  - “同时为 Claude Code 和 Codex 创建 CLAUDE.md 和 AGENTS.md。”

- 可复用命令：
  - `sed -n`
  - `rg -n`
  - `find ... | sort`
  - `git diff --stat`
  - `git status --short`

- 可复用文件模板：
  - 操作记录
  - synthesis 样例
  - repo 级 `AGENTS.md`
  - repo 级 `CLAUDE.md`

- 可复用目录约定：
  - `outputs/logs/`
  - `outputs/syntheses/`
  - `wiki/indexes/shared/` 作为共享工作流与入口层

# 9. 遗留问题

- 还没解决的问题：
  - `timeseries`、`operationsresearch` 的专题问题地图尚未分别建立。
  - 新 query / log / synthesis 工作流还缺更多真实样例。
- 还没验证的假设：
  - `outputs/logs/` 是否会成为稳定使用的时间导航层，未明确。
  - `AGENTS.md` 与 `CLAUDE.md` 是否足以减少后续 agent 误解，未明确。
- 后续适合单开新线程处理的事项：
  - 把本线程经验抽成 `Codex skill`
  - 为知识库项目设计“能力缺口诊断 skill”
  - 为 repo 级 schema 上收设计独立流程

# 10. 与其他线程的关系

- 依赖了哪些前序线程：未明确
- 给哪些后续线程提供了上下文：
  - 任何涉及本仓库知识库整理、workflow backfill、prompt 扩展、repo 级 agent 约束的后续线程
- 如果要串成阶段汇总，这条线程属于哪个阶段：
  - “Codex 工作流识别与 schema 固化”阶段

# 11. 一句话结论

- 这条线程的价值不在知识库主题内容，而在于把“如何补 Codex 工作流缺口”跑成了一次真实样例。
- 它证明了：先做能力诊断，再做最小补丁式 workflow backfill，比直接重构更适合当前仓库。
- 它还把“分散 schema -> repo 级 AGENTS/CLAUDE”这条上收路径跑通了，但也表明这一步最好由用户明确触发。
- 对后续 skill 设计最有价值的，不是单个文件内容，而是这条线程暴露出的判断顺序、补齐顺序和反模式边界。

# 12. 补充要求

- 无
