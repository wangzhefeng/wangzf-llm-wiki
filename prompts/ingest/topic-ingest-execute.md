请基于我已经确认的专题纳入计划，直接在当前知识库中实施，不要只停留在分析。

执行约束：
- 保留原始目录，不覆盖、不删除旧文档，除非计划里明确要求迁移
- `raw/` 是唯一摄取入口，本地旧文档统一进入 `raw/notes/`
- 先补 `wiki/sources/`，再补 `wiki/indexes/`，最后补 `wiki/concepts/`
- 新页面统一使用普通 Markdown 和 frontmatter
- 不保留旧站点里的 `<style>`、`<details>`、Hugo 特有目录块
- 图片统一复制到 `raw/assets/attachments/<topic-slug>/`
- 新 wiki 页面只引用迁移后的图片路径
- 原始文档路径要可追溯，来源卡保留 `source_type` 和 `source_path`

请直接完成这些事情：

1. 创建或更新 `raw/notes/` 下的专题清单
2. 按计划创建来源卡、索引页、概念页
3. 必要时复制图片到 `raw/assets/attachments/<topic-slug>/`
4. 修正互链、来源路径和目录说明
5. 最后做验证，并报告：
   - 新增了哪些关键页面
   - 验证命令或验证方式
   - 还剩哪些风险或下一步

输出要求：
- 不要再重复写一版计划
- 直接实施
- 最终汇报按“做了什么 / 怎么验证 / 剩余风险”三部分组织
