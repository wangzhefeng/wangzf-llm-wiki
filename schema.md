---
created_at: 2026-04-18
aliases:
  - Wiki 规则 Schema
  - 知识库Schema设计
topics:
  - 知识库构建
  - schema
  - llm-wiki
related_concepts:
  - 知识库建设方法
  - 知识库工作台
status: active
---

# LLM Wiki 规则 Schema

## 1. 角色与单一出口

- `README.md`：GitHub 项目介绍
- `schema.md`：唯一规则入口
- `purpose.md`：研究目标、边界与优先级
- `wiki/index.md`：唯一统一导航入口
- `wiki/log.md`：唯一操作日志
- `wiki/log_lint.md`：唯一 lint / health 主报告

## 2. 模块边界

- `raw/`：唯一摄取入口，只放原始资料与最小元数据
  - `raw/assets/`：通用附件和非来源型素材，不代替 `raw/` 保存原始来源
  - `raw/datasets`：
  - `raw/images`：原始图片、截图、图表
  - `raw/notes`：个人笔记
  - `raw/papers`：论文原始材料
  - `raw/repos`：代码仓库原始材料
  - `raw/web`：网页原始材料
- `wiki/`：结构化知识层，放来源卡、索引、概念、实体、对比、问题页
  - `wiki/comparisons/`：横向比较页，适合多对象、多方案选择问题
  - `wiki/concepts/`：方法、理论、模型、工作流等概念页
  - `wiki/entities/`：人物、组织、项目等可跨主题复用的实体页
  - `wiki/indexes/`：TODO
  - `wiki/queries/`：可复用问题页，适合高频问题和证据路径模板
  - `wiki/sources/`：单个来源的摘要页，回答“这份材料讲了什么、价值是什么、连到哪些概念”
  - `wiki/index.md`：知识库主页，列出所有概念、实体、索引、问题页
  - `wiki/log.md`：唯一操作日志
  - `wiki/log_lint.md`：唯一 lint / health 主报告
- `outputs/`：派生结果层，放 `answers / syntheses / slides / figures`
  - `outputs/answers/`：问答结果
  - `outputs/figures/`：图表结果
  - `outputs/slides/`：演示结果
  - `outputs/syntheses/`：总结结果，阶段性综述或综合判断
- `prompts/`：提示词模板目录，不再依赖目录 README 作为入口

## 3. 原始层规范

`raw/` 允许放：

- 网页正文或网页裁剪结果
- 论文 PDF 与元数据页
- `repo-*.md` 仓库入口卡
- 数据集说明页
- 原始图片、截图、图表
- 本地笔记与历史专题材料

`raw/` 不允许放：

- 手工长篇总结
- 替代 `wiki/` 的索引、概念或结论页

`raw/assets/` 只放：

- 通用插图
- 封面图
- 引用素材
- 与单一来源不强绑定的附件

补充约束：

- 来源型 PDF、网页正文、原始截图优先进入 `raw/`
- 附件路径尽量保持稳定，避免后续改链
- 正式编译范围：`raw/web/**`、`raw/repos/repo-*.md`、`raw/notes/**`
- `raw/repos/**` 下镜像仓库文档默认只作背景证据，不逐文件编译

## 4. 知识层规范

`wiki/` 是结构化知识层，放来源卡、索引、概念、实体、对比、问题页。

- `wiki/sources/`：单个来源的摘要页，回答"这份材料讲了什么、价值是什么、连到哪些概念"。每个 topic 目录独立维护来源清单。
- `wiki/concepts/`：方法、理论、模型、工作流等概念页，按 topic 子目录组织。
- `wiki/entities/`：人物、组织、社区、项目等可跨主题复用的实体页，按 topic 子目录或根目录组织。
- `wiki/indexes/`：主题总索引、阅读地图、来源清单，按 topic 子目录组织。`shared/` 子目录放跨 topic 的流程与导航页。
- `wiki/comparisons/`：横向比较页，适合多对象、多方案选择问题。
- `wiki/queries/`：可复用问题页，适合高频问题和证据路径模板。

知识层规则：

- 页面互链优先使用 `[[wikilinks]]`
- 新增稳定页面后，必须补到至少一个主题索引入口
- 仅在"2+ 来源共同出现"或"单来源核心主题"时新建概念/实体页
- 原始层文件不做语义改写，修正写入 `wiki/` 层

## 5. 派生层规范

`outputs/` 是派生结果层，放 answers / syntheses / slides / figures。

- `outputs/answers/`：问答结果，针对具体问题的回答。
- `outputs/syntheses/`：总结结果，阶段性综述或综合判断。
- `outputs/slides/`：演示结果。
- `outputs/figures/`：图表结果。

派生层规则：

- 高价值结果优先进入 `outputs/answers` 或 `outputs/syntheses`
- 若问题会重复出现，再考虑沉淀到 `wiki/queries/` 或 `wiki/comparisons/`
- 做完 task 后：更新相关索引、补充来源卡或概念卡（如有新知识）

## 6. 页面字段规范

### `raw/**/*.md`

```yaml
---
source_type: web | papers | repos | datasets | images | notes
created_at: YYYY-MM-DD
topics:
  - topic-a
status: inbox
---
```

- `source_type`、`created_at`、`topics` 必填
- `topics` 控制在 1 到 3 个

### `wiki/**/*.md`

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: source | concept | entity | comparison | query | summary
tags:
  - tag-a
sources:
  - raw/web/xxx.md
status: linked
---
```

- 历史页面可暂保留 `created_at/topics/related_concepts/status`
- 目录导航页允许 `status: active`
- 来源卡推荐保留 `source_path`
- `source_path` 必须是 `raw/` 相对路径；允许单值或列表

## 7. 命名与主题规范

- 原始网页：`YYYY-MM-DD-标题.md`
- 仓库来源：`repo-组织名-仓库名.md`
- 概念页：`概念名.md`
- 输出结果：`YYYY-MM-DD-主题-用途.md`
- 操作日志固定追加到 `wiki/log.md`
- 审查报告固定写入 `wiki/log_lint.md`
- 模板/清单类文件允许无日期前缀
- `raw/notes/**/index.md` 允许目录式命名

活跃主题：

- `llm`
- `llm-wiki`
- `timeseries-analysis`
- `operations-research`
- `machine-learning`
- `deep-learning`
- `statistics-theory`
- `causal-inference`
- `nlp`
- `feature-engineering`
- `control-algorithms`
- `power-market-trading`
- `reinforcement-learning`
- `vibe-coding`

常见旧别名：

- `timeseries` -> `timeseries-analysis`
- `statistics` -> `statistics-theory`
- `operationsresearch` -> `operations-research`
- `machinelearning` -> `machine-learning`
- `deeplearning` / `deep-learning-theory` -> `deep-learning`
- `knowledge-base` / `llm-knowledge-base` -> `llm-wiki`

不再新增的旧名：

- `agent-dev`
- `computer-vision`
- `data-analysis`
- `data-structure-algorithm`
- `tools`
- `programming-tools`
- `others`

## 8. 默认执行顺序

1. `raw`
2. `wiki/sources`
3. `wiki/indexes`
4. `wiki/concepts`
5. `outputs`
6. `wiki/log.md`
7. `wiki/log_lint.md`

规则：

- 页面互链优先使用 `[[wikilinks]]`
- `raw/` 是原始事实层，允许做最小维护性修复，不允许写解释性知识内容
- ingest / query / lint / backfill / task 统一追加到 `wiki/log.md`
- `wiki/log.md` 保持 append-only
- 最新 lint / health 结果统一覆盖到 `wiki/log_lint.md`
- 原始层文件不做语义改写，修正写入 `wiki/` 层
- 新增稳定页面后，必须补到至少一个主题索引入口
- 仅在“2+ 来源共同出现”或“单来源核心主题”时新建概念/实体页
- 当前标准收尾顺序：`基线盘点 -> 修断链 -> 重编译 sources -> 刷新 indexes/concepts -> 更新流程文档 -> 复验与日志收尾`

## 9. 动作规则

- `ingest`
  - 先读 `raw`，再补 `wiki/sources`
  - 需要时补 `entities / concepts / indexes`
  - 新内容必须能从至少一个索引入口到达
- `query`
  - 先读相关索引、来源、概念，再回答
  - 高价值结果优先进入 `outputs/answers` 或 `outputs/syntheses`
  - 若问题会重复出现，再考虑沉淀到 `wiki/queries/` 或 `wiki/comparisons/`
- `lint`
  - 优先发现：断链、孤页、缺入口、命名漂移、来源缺口、应独立成页但尚未成页的概念
  - 先产出建议，再按当前仓库流程修复
  - 不把“内容薄弱但已登记”误报成结构错误
- `backfill`
  - 检查 outputs/ 中高价值结果是否已有对应入口
  - 优先回流：syntheses（综述）、answers（问答）中经判定有长期价值的
  - 回流后：补入对应主题索引，在相关来源卡中补充 [[outputs/...]] 链接
  - 不回流：一次性临时答案、明显过时内容、已被新覆盖的旧输出
- `log`
  - ingest / query / lint / backfill / task 统一追加到 wiki/log.md
  - 格式：## [YYYY-MM-DD] action | subject
  - action 类型：ingest / update / query / lint / backfill / archive / task
  - 每条记录包含：时间戳、操作类型、简要描述、关键产出
  - 保持 append-only，不修改历史记录
- `task`
  - 适用于：代码开发、演示构建、数据分析等任务驱动工作流
  - 产出优先写入 outputs/ 对应子目录，再回链到 wiki/
  - 任务完成后：更新相关索引、补充来源卡或概念卡（如有新知识）
  - 复用 prompts/task/llm-wiki-task.md 模板

## 10. 会话启动

1. [[schema]]
2. [[purpose]]
3. [[wiki/index]]
4. [[log]]（最近 20~30 行）
5. [[log_lint]]
6. 任务相关主题总索引（`wiki/indexes/*/`）
