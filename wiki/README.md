# wiki

`wiki/` 只放由 `raw/` 编译出来的结构化知识页，不放原始资料。

建议把 `wiki/index.md` 作为“日常入口”，把 `wiki/schema.md` 作为“规则入口”：

- `wiki/index.md`
- `wiki/schema.md`
- `wiki/log.md`

目录职责：

- `sources/`：每个来源的一页摘要卡
- `indexes/`：主题索引、阅读地图、问题地图
- `concepts/`：概念、方法、人物、工具等条目
  - 其他（按需启用）：`entities/`、`queries/`、`comparisons/`

当前组织方式：

- 第一层仍然按页面角色分为 `sources/`、`indexes/`、`concepts/`
- 第二层按专题拆分为 `timeseries/`、`operationsresearch/`、`knowledge-base/`、`shared/`
- `knowledge-base/` 放知识库构建这个独立主题的来源、索引与概念页
- `shared/` 只放全库公共页面与工作台页面，例如健康检查清单、知识库工作台、开发工作流
- `wiki/README.md` 保留在 `wiki/` 根目录，作为这一层的总说明

约束：

- 先生成 `sources/`，再补 `indexes/`，最后沉淀 `concepts/`
- 页面之间尽量使用普通 Markdown 和 Wiki 链接语法互链
- 优先使用名称链接而不是路径链接，减少后续目录迁移成本
- 不把一次性问答结果直接堆进 `wiki/`，高价值输出回流时再补链接

推荐命名：

- 概念条目：`概念名.md`

当前常用入口：

- 跨主题方法入口：[[知识库建设方法总索引]]
- 全库工作台入口：[[知识库工作台]]
- 全库维护入口：[[知识库健康检查清单]]
- 时间序列主题入口：[[时间序列预测总索引]]
- 运筹优化主题入口：[[运筹优化算法总索引]]

本层子目录说明：

- `wiki/sources/README.md`
- `wiki/indexes/README.md`
- `wiki/concepts/README.md`
- `wiki/entities/README.md`
- `wiki/queries/README.md`
- `wiki/comparisons/README.md`
