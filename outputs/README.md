# outputs

`outputs/` 只放围绕当前知识库生成的派生结果，不放原始来源，也不替代 `wiki/`。

目录职责：

- `answers/`：单次问答结果
- `syntheses/`：阶段性综述或专题整理
- `slides/`：Marp 幻灯片或演示稿
- `figures/`：图表、示意图、流程图说明
- `logs/`：按时间记录一次 ingest、query、lint 或回流动作

约束：

- 输出优先写成可回看、可回链的 Markdown 或图表文件
- 高价值输出完成后，回链到相关 `wiki/` 页面
- 时间导航记录优先写入 `logs/`，不要只留在对话里

推荐命名：

- 输出结果：`YYYY-MM-DD-主题-用途.md`

## 图谱入口（近期关键输出）

- [[outputs/answers/2026-04-09-llm-timeseries-autofix-映射候选]]
- [[outputs/logs/2026-04-06-时间序列来源编译与synthesis产出记录]]
- [[outputs/logs/2026-04-11-raw-assets-分类修复-动作记录]]
- [[outputs/syntheses/2026-04-06-web批量摄取-知识库总结]]
- [[outputs/syntheses/2026-04-08-llm-wiki-维护流程总结]]
- [[outputs/syntheses/2026-04-08-llm-wiki-ai与用户使用流程总结]]
- [[outputs/syntheses/2026-04-08-llm-wiki-构建流程总结]]
