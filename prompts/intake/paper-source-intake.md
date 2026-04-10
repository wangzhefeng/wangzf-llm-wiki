请基于我提供的论文 PDF、论文笔记或论文元数据，在当前知识库中直接执行一次“论文来源沉淀”。

执行约束：
- 当前知识库采用 `raw -> wiki/sources -> wiki/indexes -> wiki/concepts -> outputs` 分层
- 论文原始材料统一先进入 `raw/papers/`
- 不把论文直接改写成概念百科
- 先补来源层，再补索引层，最后补概念层
- 不编造论文中没有出现的信息
- 如果 PDF 只有题录没有正文，要明确标注 `missing_context`

请按下面顺序执行：

1. 在 `raw/papers/` 创建或更新原始来源页
   - 至少保留：
     - `source_type: paper`
     - `source_url`（如有）
     - `created_at`
     - `topics`
     - `related_concepts`
     - `status`
   - 正文至少包括：
     - 论文标题、作者、年份、出处
     - 研究问题
     - 方法概要
     - 实验或结论概要
     - 待沉淀方向

2. 在 `wiki/sources/<topic>/` 创建 1 张来源摘要卡
   - 必须保留：
     - `source_type`
     - `source_url`（如有）
     - `source_path`
     - `created_at`
     - `topics`
     - `related_concepts`
     - `status`
   - 正文至少回答：
     - 这篇论文解决什么问题
     - 方法核心是什么
     - 关键实验或结论是什么
     - 它对当前知识库的价值是什么
     - 局限和适用边界是什么

3. 只在确有增量时更新索引页和概念页
   - 优先更新：
     - 总索引
     - 阅读地图
     - 最相关的 1-3 个概念页

4. 如果论文里有关键图表值得长期引用
   - 复制到 `assets/attachments/<topic-slug>/<paper-slug>/`
   - wiki 页面只引用本地化后的路径

5. 最后做最小验证
   - 检查 `raw/papers/` 原始页已创建
   - 检查来源卡 frontmatter 完整
   - 检查索引页或概念页是否已补入口

输出要求：
- 直接实施，不只给计划
- 最终汇报按“做了什么 / 怎么验证 / 剩余风险”组织
