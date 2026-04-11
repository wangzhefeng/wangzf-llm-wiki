# wangzf_kb

一个面向 LLM 持续工作的 Markdown 知识库。核心目标不是堆积笔记，而是把原始资料稳定转化为可检索、可复用、可回流的结构化知识。

## 定位

- 本仓库主链路：`raw -> wiki -> outputs`
- 主要内容对象：网页、论文、仓库、数据集、本地历史文档
- 主要使用方式：`ingest / query / lint / backfill`

## 职责边界（重要）

- `README.md`（本页）：
  仓库级入口。回答“这个仓库是什么、有哪些模块、从哪里开始”。
- `wiki/index.md`：
  wiki 子系统统一导航。回答“在 wiki 内先看什么、从哪个入口执行”。
- `wiki/schema.md`：
  wiki 结构与字段规范。回答“页面和流程应遵循什么约束”。
- `wiki/log.md`：
  wiki 操作时间线。回答“最近做了什么、下一轮如何衔接”。

简化理解：`README` 管仓库全局，`wiki/index` 管 wiki 导航，二者互补而非替代。

## 目录概览

- `raw/`：原始来源入口（外部原件与最小元数据）
- `wiki/`：结构化知识层（`sources` / `indexes` / `concepts` 等）
- `outputs/`：问答、综述、演示稿、图表与日志等派生结果
- `prompts/`：可复用提示词模板
- `raw/assets/`：通用附件与素材

## 快速开始

1. 先看 wiki 控制入口：
   - [Wiki Index](wiki/index.md)
   - [Wiki Schema](wiki/schema.md)
   - [Wiki Log](wiki/log.md)
2. 再进入共享工作台：
   - [知识库工作台](wiki/indexes/knowledge-base-operations/知识库工作台.md)
3. 按任务类型选择工作流：
   - 摄取： [知识库来源与专题摄取索引](wiki/indexes/knowledge-base-building/知识库来源与专题摄取索引.md)
   - 问答/研究： [知识库问答与研究工作流](wiki/indexes/knowledge-base-usage/知识库问答与研究工作流.md)
   - 维护： [知识库维护检查索引](wiki/indexes/knowledge-base-operations/知识库维护检查索引.md)

## 主题入口

- [大语言模型总索引](wiki/indexes/llm/大语言模型总索引.md)
- [时间序列预测总索引](wiki/indexes/timeseries/时间序列预测总索引.md)
- [运筹优化算法总索引](wiki/indexes/operationsresearch/运筹优化算法总索引.md)
- [机器学习总索引](wiki/indexes/machinelearning/机器学习总索引.md)
- [数据分析总索引](wiki/indexes/analysis/数据分析总索引.md)
- [深度学习总索引](wiki/indexes/deeplearning/深度学习总索引.md)
- [计算机视觉总索引](wiki/indexes/computervision/计算机视觉总索引.md)
- [强化学习总索引](wiki/indexes/reinforcementlearning/强化学习总索引.md)
- [控制算法总索引](wiki/indexes/control_algorithms/控制算法总索引.md)
- [电力市场交易总索引](wiki/indexes/power-market-trading/电力市场交易总索引.md)
- [Vibe Coding总索引](wiki/indexes/vibe-coding/Vibe Coding总索引.md)

## 标准工作顺序

1. 新资料进入 `raw/`
2. 先补 `wiki/sources/` 来源卡
3. 再更新 `wiki/indexes/` 导航与阅读路径
4. 再补 `wiki/concepts/` 概念网络
5. 高价值结果写入 `outputs/` 并回流到 wiki 入口页

## 常用资源

- [知识库建设方法总索引](wiki/indexes/knowledge-base-building/知识库建设方法总索引.md)
- [知识库运维总索引](wiki/indexes/knowledge-base-operations/知识库运维总索引.md)
- [知识库使用总索引](wiki/indexes/knowledge-base-usage/知识库使用总索引.md)
- [提示词模板入口](prompts/README.md)
- [来源卡提示词](prompts/intake/source-summary.md)
- [问答研究提示词](prompts/query/knowledge-base-query.md)
- [健康检查提示词](prompts/maintenance/wiki-lint.md)

## 线程沉淀

需要把历史线程经验回流时，使用 `raw/codex_threads/`：

- [使用说明](raw/codex_threads/README.md)
- [线程总结模板](raw/codex_threads/线程总结模板.md)
