---
title: LLM 架构--Prompt
created: 2024-04-09
updated: 2026-04-15
type: source
tags:
  - llm-theory
sources:
  - raw/notes/llm-theory/2024-04-09-llm-prompt
status: summarized
---
## 内容摘要
<details><summary>目录</summary><p> - [预训练模型和 Prompt](#预训练模型和-prompt) - [Pretrain](#pretrain) - [Promot](#promot) - [Prompt 工作流](#prompt-工作流) - [Prompt Template](#prompt-template)

## 关键要点
- 左边是传统的 Model Tuning 的范式：对于不同的任务，都需要将整个预训练模型进行精调，
- 右边是 Prompt Tuning，对于不同的任务，仅需要插入不同的 Prompt 参数，
- Prompt 模版（Template）的构造

## 来源信息
- 原始文件：2024-04-09-llm-prompt
- 来源类型：notes
