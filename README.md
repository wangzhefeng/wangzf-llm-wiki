# wangzf-llm-wiki

一个面向 LLM 持续工作的 Markdown 知识库项目，用于把原始资料稳定转化为可检索、可复用、可回流的结构化知识。

## 项目概览

- 主链路：`raw -> wiki -> outputs`
- `raw/`：原始来源入口
- `wiki/`：结构化知识层
- `outputs/`：问答、综述、图表、演示稿等派生结果
- `prompts/`：可复用提示词模板

当前正式原始资料范围为：

- `raw/web/**`
- `raw/repos/repo-*.md`
- `raw/notes/**`

`raw/repos/**` 下镜像仓库文档默认只作背景证据，不逐文件下沉为来源层。

## 仓库入口

- [LLM Wiki 规则入口 `schema.md`](schema.md)
- [LLM Wiki `purpose.md`](purpose.md) # TODO
- [LLM Wiki 内部导航 `wiki/index.md`](wiki/index.md)
- [LLM Wiki 操作日志 `wiki/log.md`](wiki/log.md)
- [LLM Wiki 最新审查报告 `wiki/log_lint.md`](wiki/log_lint.md)

## 使用说明

- 想了解仓库规则、命名、流程与输出口，先读 `schema.md`
- 想了解研究目标、边界与优先级，读 `purpose.md`
- 想进入知识库内部导航与工作流，读 `wiki/index.md`
- 想查看最近维护动作与历史时间线，读 `wiki/log.md`
- 想查看最近一次 lint / health 结果，读 `wiki/log_lint.md`

## 说明

本 README 只承担 GitHub 项目介绍，不再作为 Agent 的控制文件入口。知识库内部执行入口已统一迁移到 `schema.md` 与 `wiki/index.md`。
