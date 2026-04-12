---
source_type: internal
source_path: "raw/readme-20260412200431.md"
title: "raw 目录说明"
author: unknown
created_at: 2026-04-12
topics:
- knowledge-base
status: archived
---
# raw

`raw/` 是知识库的唯一摄取入口，只存放外部来源原件和最小元数据。

放在这里的内容：

- 网页正文或网页裁剪结果
- 论文 PDF 与同名元数据页
- 仓库入口说明、README 摘录、关键目录说明
- 数据集说明或索引页
- 原始图片、截图、图表
- 本地个人文档或历史专题资料
- 知识库自身的方法论文档与执行指引

约束：

- 不在 `raw/` 里手工写长篇总结
- 先收集来源，再交给 LLM 编译到 `wiki/`
- 目录约定：
  - `web/`
  - `papers/`
  - `repos/`
  - `datasets/`
  - `images/`
  - `local-notes/`

推荐命名：

- 原始网页：`YYYY-MM-DD-标题.md`
- 论文笔记：`YYYY-作者简写-标题短名.md`
- 仓库来源：`repo-组织名-仓库名.md`
- 本地个人文档清单：`主题名-历史文档清单.md`
