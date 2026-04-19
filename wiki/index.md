---
created_at: 2026-04-09
topics:
  - 知识库导航
  - index
  - llm-wiki
related_concepts:
  - 知识库工作台
  - LLM-Wiki总索引
status: linked
---

# Wiki 统一入口

> wiki 子系统唯一导航入口

## 控制文件

- [[schema]]：唯一规则源，定义结构、页面职责、执行约束与输出规则
- [[purpose]]：定义研究目标、边界与当前重点
- [[wiki/index]]：当前统一导航入口
- [[wiki/log]]：唯一操作日志（append-only）
- [[wiki/log_lint]]：最新 lint / health 审查主报告

## 快速开始

1. 先读控制文件：`schema -> purpose -> wiki/index -> wiki/log -> wiki/log_lint`
2. 按任务类型进入入口：
   - ingest(知识摄取)：[[知识库来源与专题摄取索引]]
   - query(问答/研究)：[[知识库问答与研究工作流]]
   - backfill(输出回流)：[[知识库输出回流工作流]]
   - lint(审查维护)：[[知识库维护检查索引]]
   - log(日志记录)：[[知识库操作记录索引]]
   - task(任务执行)：[[知识库任务与输出工作流索引]]
3. 当前标准顺序：`基线盘点 -> 修断链 -> 重编译 sources -> 刷新 indexes/concepts -> 更新流程文档 -> 复验与日志收尾`
4. 健康检查统一入口：
   - `python3 .env/health/wiki_check.py --checks lint`
   - `python3 .env/health/wiki_check.py --checks health`
   - `python3 .env/run_tool.py health check`

## Prompt 入口

### 分类总览

- `ingest/`：把原始资料编译成来源卡
- `query/`：围绕现有 wiki 做问答与研究
- `lint/`：做结构检查、健康检查与收尾
- `backfill/`：做高价值输出回流
- `log/`：为操作时间线补标准记录
- `task/`：做高价值任务执行

### 关键 prompt

- ingest
  - `prompts/ingest/source-summary.md`
  - `prompts/ingest/topic-ingest-plan.md`
  - `prompts/ingest/topic-ingest-execute.md`
- query
  - `prompts/query/llm-wiki-query.md`
- lint
  - `prompts/lint/llm-wiki-lint.md`
  - `prompts/lint/llm-wiki-health-check.md`
- log
  - `prompts/log/llm-wiki-logging.md`
- task
  - `prompts/task/llm-wiki-task.md`

### 何时用哪个

- 新增一份资料：优先用 `ingest/*`
  - 新增一个专题：先 `ingest/topic-ingest-plan`，再 `ingest/topic-ingest-execute`
- 围绕现有库提问或研究：优先用 `query/llm-wiki-query.md`
- 做结构检查或全库体检：用 `lint/*`
- 做完 ingest / query / lint / backfill 后补时间记录：用 `log/llm-wiki-log.md`
- 做高价值任务：用 `task/llm-wiki-task.md`

### 使用规则

- 新增 prompt 默认进入现有分类目录，不再放 `prompts/` 根目录
- 满足以下任一条件才新建分类：
  - 单一分类模板数 `>= 8`
  - 连续 3 次使用中频繁找不到或误选模板
  - 同一类模板稳定分化出 3 个以上子场景
  - 新模板与现有五类都不匹配，且预计会复用 `>=3` 次
- 文件名保持稳定语义，不使用 `v2`、`v3`、`final` 这类一次性后缀

## 执行入口

中心调度：[[知识库工作台]]（五类操作的统一导航枢纽）

| 操作 | 入口 | 说明 |
|---|---|---|
| ingest 摄取 | [[知识库来源与专题摄取索引]] | 纳入新资料或新专题 |
| query 问答 | [[知识库问答与研究工作流]] | 围绕已有 wiki 研究与问答 |
| backfill 回流 | [[知识库输出回流工作流]] | 高价值输出沉淀回库 |
| lint 维护 | [[知识库维护检查索引]] | 健康检查与结构修复 |
| task 任务 | [[知识库任务与输出工作流索引]] | 开发、演示等任务驱动工作流 |
| log 追踪 | [[知识库操作记录索引]] | 全库操作时间线与复盘 |

> query 选题辅助：[[知识库问题地图]]
> lint 知识审查：[[知识库健康检查清单]]

## 主题入口

- [[大语言模型总索引]]
- [[时间序列预测总索引]]
- [[运筹优化算法总索引]]
- [[机器学习总索引]]
- [[统计学理论总索引]]
- [[因果推断总索引]]
- [[深度学习总索引]]
- [[自然语言处理总索引]]
- [[强化学习总索引]]
- [[特征工程总索引]]
- [[控制算法总索引]]
- [[电力市场交易总索引]]
- [[Vibe-Coding总索引]]
- [[LLM-Wiki总索引]]

## 区域入口

- `wiki/sources/`：来源卡层（入口：[[wiki/sources/index]]）
- `wiki/indexes/`：索引层（入口：[[wiki/indexes/index]]）
- `wiki/concepts/`：概念层（入口：[[wiki/concepts/index]]）
- `wiki/entities/`：实体层（入口：[[wiki/entities/index]]）
- `wiki/comparisons/`：对比层（入口：[[wiki/comparisons/index]]）
- `wiki/queries/`：问题沉淀层（入口：[[wiki/queries/index]]）

## 使用说明

- 本页只承担导航与执行入口，不承载底层规则细节；规则统一维护在 [[schema]]
- 新增稳定页面后，至少更新一个主题总索引，并补到本页对应入口区块
