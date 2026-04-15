# prompts

`prompts/` 存放会重复使用的提示词模板，目标是减少每次从头写提示词的成本。

当前分类基线与自动扩展触发条件见：

- [[prompts/prompt-分类与触发规则]]

约束：

- 模板只描述任务，不把临时上下文硬编码进去
- 先保持轻量，等工作流稳定后再扩展自动化

## 分类方式

当前已按“用途”完成子目录分类。

这样做的原因：

- 同一个专题会反复用到不同类型的 prompt
- 按用途分类更利于复用
- 目录名即任务语义，便于快速定位

## 1. 来源沉淀类

用于把原始资料从 `raw/` 编译进知识库。

- `intake/source-summary.md`
  通用来源摘要卡生成模板。适合你已经准备好 `raw` 材料，只想生成一页 `wiki/sources/` 摘要卡时使用。
- [[prompts/intake/web-source-intake]]
  网页来源沉淀模板。适合技术文章、官方文档、教程示例页。
- [[prompts/intake/repo-source-intake]]
  代码仓库来源沉淀模板。适合 GitHub 仓库、算法实现仓库、工程项目。
- `intake/paper-source-intake.md`
  论文来源沉淀模板。适合论文 PDF、论文笔记、论文元数据页。
- `intake/dataset-source-intake.md`
  数据集来源沉淀模板。适合数据说明页、数据字典、任务数据入口。
- `intake/image-source-intake.md`
  图片来源沉淀模板。适合关键截图、图表、示意图。
- `intake/local-note-source-intake.md`
  本地历史文档沉淀模板。适合 `raw/notes/` 中已有原文的结构化提升。

## 2. 查询研究类

用于围绕现有 wiki 发起问答、比较、研究和输出回流。

- `query/knowledge-base-query.md`
  统一 query 模板。适合先列证据，再给回答，并把结果写入 `answers/` 或 `syntheses/`。

## 3. 专题纳入类

用于把一个新专题成批纳入当前知识库。

- [[prompts/topic-intake/topic-intake-plan]]
  先产出专题纳入计划，不直接实施。适合新专题体量较大、结构还不清楚时使用。
- [[prompts/topic-intake/topic-intake-execute]]
  基于已确认计划直接实施。适合你已经确认范围、希望直接落盘到知识库时使用。

## 4. 维护检查类

用于检查知识库结构、链接和覆盖情况。

- `maintenance/wiki-lint.md`
  偏结构和格式检查。适合检查链接、frontmatter、角色边界、命名等问题。
- `maintenance/knowledge-base-health-check.md`
  偏全库健康度检查。适合从 `raw / sources / indexes / concepts / outputs` 全链路看哪里缺口最大。

## 5. 操作记录类

用于补时间导航记录。

- `logging/operation-log.md`
  操作记录模板。适合为 `ingest / query / lint / backfill` 落一条可回看的时间记录。

## 使用导航

如果你只是想先找到“当前该走哪类操作入口”，先看：

- [[知识库工作台]]
- [[知识库来源与专题摄取索引]]
- [[知识库维护检查索引]]

如果你要做的是“新增一份资料”：

1. 网页资料用 `intake/web-source-intake.md`
2. 仓库资料用 `intake/repo-source-intake.md`
3. 论文资料用 `intake/paper-source-intake.md`
4. 数据集资料用 `intake/dataset-source-intake.md`
5. 图片资料用 `intake/image-source-intake.md`
6. 本地历史文档用 `intake/local-note-source-intake.md`
7. 已经有 `raw` 材料，只想生成摘要卡时用 `intake/source-summary.md`

如果你要做的是“围绕现有库提问或研究”：

1. 先看 [[知识库问题地图]]
2. 再用 `query/knowledge-base-query.md`
3. 做完后补 `logging/operation-log.md`

如果你要做的是“新增一个专题”：

1. 先用 `topic-intake/topic-intake-plan.md`
2. 确认后再用 `topic-intake/topic-intake-execute.md`

如果你要做的是“检查现有知识库”：

1. 偏格式和结构问题，用 `maintenance/wiki-lint.md`
2. 偏整体状态和下一步优先级，用 `maintenance/knowledge-base-health-check.md`

## 后续约定

后续如果 prompt 数量继续增长，建议继续沿用这 5 类：

- 来源沉淀类
- 查询研究类
- 专题纳入类
- 维护检查类
- 操作记录类

当前已完成子目录化。后续新增模板默认放入对应类别目录。

## 当前分类快照（便于直接查找）

- 来源沉淀类：`prompts/intake/`
- 查询研究类：`prompts/query/`
- 专题纳入类：`prompts/topic-intake/`
- 维护检查类：`prompts/maintenance/`
- 操作记录类：`prompts/logging/`
