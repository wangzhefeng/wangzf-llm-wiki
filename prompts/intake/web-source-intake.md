请基于我提供的网页 URL、所属专题和当前知识库上下文，直接执行一次“网页来源沉淀”。

适用场景：
- 官方文档
- 教程示例页
- 技术博客
- 长篇文章

执行约束：
- 当前知识库采用 `raw -> wiki/sources -> wiki/indexes -> wiki/concepts -> outputs` 分层
- `raw/` 是唯一摄取入口
- 网页原始材料统一先进入 `raw/web/`
- 不要一上来把网页直接改写成最终综述
- 先补来源层，再补索引层，最后补概念层
- 重要图片、图表、截图优先本地化到 `assets/attachments/<topic-slug>/<page-slug>/`
- 新页面统一使用普通 Markdown 和 frontmatter
- 不要编造网页中没有出现的信息
- 如果网页信息不足以支撑概念更新，要明确写出 `missing_context`

请按下面顺序执行：

1. 在 `raw/web/` 创建或更新一页原始来源笔记
   - 文件名建议：`YYYY-MM-DD-页面短名.md`
   - 至少记录：
     - `source_type: web`
     - `source_url`
     - `created_at`
     - `topics`
     - `related_concepts`
     - `status`
   - 页面正文至少包括：
     - 页面标题、作者/机构、发布时间
     - 页面主旨
     - 关键知识点
     - 关键图表或示例
     - 适用边界
     - 待沉淀方向

2. 在 `wiki/sources/<topic>/` 创建 1 张来源摘要卡
   - 来源卡必须保留：
     - `source_type`
     - `source_url`
     - `source_path`
     - `created_at`
     - `topics`
     - `related_concepts`
     - `status`
   - 来源卡正文至少回答：
     - 这篇网页讲什么
     - 核心结论有哪些
     - 它对当前知识库的价值是什么
     - 它和哪些现有概念相关
     - 它的局限或适用边界是什么

3. 只在确有增量时更新 `wiki/indexes/<topic>/` 和 `wiki/concepts/<topic>/`
   - 优先回写：
     - 总索引
     - 阅读地图
     - 与该网页最相关的 1-3 个概念页
   - 更新时只补“这篇网页带来的新增信息”，不要整页重写

4. 如果网页里有高价值图片或图表
   - 复制到 `assets/attachments/<topic-slug>/<page-slug>/`
   - 新建的 `wiki/` 页面只引用复制后的本地路径
   - 不修改原始网页地址

5. 最后做最小验证
   - 检查 `raw/web/` 原始来源页是否已创建
   - 检查来源卡是否已创建并包含关键 frontmatter
   - 检查概念页或索引页是否已经挂上入口
   - 检查新增链接是否能解析
   - 检查是否残留旧路径、空页面或明显占位内容

输出要求：
- 不要只给计划，直接实施
- 最终汇报按三部分组织：
  - 做了什么
  - 怎么验证
  - 剩余风险
- 如果你判断该网页只值得停留在来源层，要明确说明原因
- 如果网页质量很高，最后单独建议是否值得进一步沉淀到 `outputs/`

使用时我会补充这些最小信息：
- 网页 URL
- 所属专题，例如 `timeseries`
- 希望优先连接的概念页（可选）
