# CLAUDE.md

本文件为 Claude Code 专属补充配置。**主规范为 [AGENTS.md](AGENTS.md)**，冲突时以 AGENTS.md 为准。

## Claude Code 专属提示

- 复杂任务开始前，至少读：`README.md`、`wiki/index.md`、`wiki/purpose.md`、`wiki/schema.md`、`wiki/log.md`。
- `wiki/CONCEPTS-RULES.md` 是 `wiki/concepts/` 层的独立规则，编译新主题或补充概念页时优先查阅。
- 无用户明确要求时，不提交、推送、开 PR。

## Frontmatter 最小字段（raw 层快速参考）

```yaml
---
source_type: web | paper | repo | dataset | image | notes
created_at: YYYY-MM-DD
topics:
  - topic-a          # 1-3 个
related_concepts:
  - 相关概念名
status: inbox        # inbox | summarized | linked | archived
---
```

## 执行入口速查

| 任务 | 入口文件 |
|---|---|
| 摄取 | `wiki/indexes/shared/知识库来源与专题摄取索引.md` |
| 问答研究 | `wiki/indexes/shared/知识库问答与研究工作流.md` |
| 输出回流 | `wiki/indexes/shared/知识库输出回流工作流.md` |
| 维护检查 | `wiki/indexes/shared/知识库维护检查索引.md` |
| 全局调度 | `wiki/indexes/shared/知识库工作台.md` |
