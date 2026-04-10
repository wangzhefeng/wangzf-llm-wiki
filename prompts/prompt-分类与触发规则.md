# prompts 分类与触发规则

本页定义两件事：

1. 当前 prompts 的分类落位
2. 何时自动新建分类（目录或子类）

## 当前分类落位（v2：已目录化）

### A. 来源沉淀类

- `prompts/intake/source-summary.md`
- `prompts/intake/web-source-intake.md`
- `prompts/intake/repo-source-intake.md`
- `prompts/intake/paper-source-intake.md`
- `prompts/intake/dataset-source-intake.md`
- `prompts/intake/image-source-intake.md`
- `prompts/intake/local-note-source-intake.md`

### B. 查询研究类

- `prompts/query/knowledge-base-query.md`

### C. 专题纳入类

- `prompts/topic-intake/topic-intake-plan.md`
- `prompts/topic-intake/topic-intake-execute.md`

### D. 维护检查类

- `prompts/maintenance/wiki-lint.md`
- `prompts/maintenance/knowledge-base-health-check.md`

### E. 操作记录类

- `prompts/logging/operation-log.md`

## 自动触发新建分类规则

满足任一条件即触发“新建分类”动作：

1. 单一分类模板数 `>= 8`
2. 连续 3 次使用中，出现“找 prompt 超过 30 秒或误选模板”
3. 同一类模板出现 3 个以上稳定子场景（例如维护检查拆为：健康检查、结构 lint、回流检查）
4. 新增模板与现有五类都不匹配，且预计会复用 `>= 3` 次

## 触发后的落地动作（固定流程）

1. 在 `prompts/README.md` 增加新分类入口和一句用途定义
2. 如果需要目录化，先创建子目录（例如 `prompts/maintenance/`）
3. 保留旧路径兼容说明 1 个迭代周期，避免链接瞬时失效
4. 更新共享入口页里的 prompt 导航（至少更新 `知识库维护检查索引` 或相关工作流索引）

## 当前默认策略

- 新增 prompt 必须放入已有分类目录，不再放在 `prompts/` 根目录
- 根目录仅保留：`README.md` 与分类规则文档

## 命名约束

- 文件名继续采用 `动作-对象-用途.md` 或现有稳定命名风格
- 不使用“v2/v3/final”等一次性后缀
- 同一动作的轻量/完整版用明确后缀区分（例如 `wiki-lint` vs `knowledge-base-health-check`）
