# wangzf-llm-wiki

一个面向 LLM 持续工作的 Markdown 知识库，目标是把原始资料稳定转化为可检索、可复用、可回流的结构化知识。

## 定位

- 主链路：`raw -> wiki -> outputs`
- 核心任务：`ingest / query / lint / backfill`
- 标准原始资料：`raw/web/**`、`raw/repos/repo-*.md`、`raw/notes/**`，以及按需纳入的 `papers / datasets / images`
- `raw/repos/**` 下的镜像仓库文档默认只作背景证据，不逐文件下沉为来源层

## 结构总览

- `raw/`：原始来源入口（原件 + 最小元数据）
- `wiki/`：结构化知识层（来源卡、索引、概念等）
- `outputs/`：问答、综述、图表、演示稿、操作日志
- `prompts/`：可复用提示词模板
- `raw/assets/`：通用附件与素材

控制文件职责：
- [Wiki 统一入口](wiki/index.md)：wiki 内导航与执行入口
- [Wiki 规则 Schema](wiki/schema.md)：结构、字段、命名、流程约束
- [Wiki 目标](wiki/purpose.md)：范围、关键问题、演进方向
- [Wiki 操作日志](wiki/log.md)：仅追加的时间线记录

## 快速开始

1. 先读控制文件：`purpose -> schema -> index -> log`
2. 按任务类型进入入口：
   - 摄取：[知识库来源与专题摄取索引](wiki/indexes/shared/知识库来源与专题摄取索引.md)
   - 问答/研究：[知识库问答与研究工作流](wiki/indexes/shared/知识库问答与研究工作流.md)
   - 输出回流：[知识库输出回流工作流](wiki/indexes/shared/知识库输出回流工作流.md)
   - 维护：[知识库维护检查索引](wiki/indexes/shared/知识库维护检查索引.md)
3. 当前标准执行顺序：`基线盘点 -> 修断链 -> 重编译 sources -> 刷新 indexes/concepts -> 更新流程文档 -> 复验与日志收尾`
4. 健康检查统一入口：
   - `python3 .env/health/wiki_check.py --checks lint`
   - `python3 .env/health/wiki_check.py --checks health`
   - `python3 .env/run_tool.py health check`
5. 将高价值结果写入 `outputs/`，并补回对应索引入口

## 主题入口

- [大语言模型总索引](wiki/indexes/llm/大语言模型总索引.md)
- [时间序列预测总索引](wiki/indexes/timeseries-analysis/时间序列预测总索引.md)
- [运筹优化算法总索引](wiki/indexes/operations-research/运筹优化算法总索引.md)
- [机器学习总索引](wiki/indexes/machine-learning/机器学习总索引.md)
- [统计学理论总索引](wiki/indexes/statistics-theory/统计学理论总索引.md)
- [因果推断总索引](wiki/indexes/causal-inference/因果推断总索引.md)
- [深度学习总索引](wiki/indexes/deep-learning/深度学习总索引.md)
- [自然语言处理总索引](wiki/indexes/nlp/NLP基础任务总索引.md)
- [强化学习总索引](wiki/indexes/reinforcement-learning/强化学习总索引.md)
- [特征工程总索引](wiki/indexes/feature-engineering/特征工程总索引.md)
- [控制算法总索引](wiki/indexes/control-algorithms/控制算法总索引.md)
- [电力市场交易总索引](wiki/indexes/power-market-trading/电力市场交易总索引.md)
- [Vibe-Coding 总索引](wiki/indexes/vibe-coding/Vibe-Coding总索引.md)
- [LLM-Wiki总索引](wiki/indexes/llm-wiki/LLM-Wiki总索引.md)

## 维护入口

- [知识库工作台](wiki/indexes/shared/知识库工作台.md)
- [知识库健康检查清单](wiki/indexes/shared/知识库健康检查清单.md)
- [知识库维护检查索引](wiki/indexes/shared/知识库维护检查索引.md)
- [知识库操作记录索引](wiki/indexes/shared/知识库操作记录索引.md)
- [最新健康检查报告](outputs/answers/知识库-健康检查-最新.md)
- [提示词模板入口](prompts/README.md)

## 当前基线

- `2026-04-17` 实测：`lint = 0 errors / 0 warnings`
- `2026-04-17` 实测：`health = 0 errors / 50 warnings`
- 当前 warning 主要是少量低入口来源卡与长尾孤页，不再属于真实坏链阻塞项；说明见[最新健康检查报告](outputs/answers/知识库-健康检查-最新.md)
