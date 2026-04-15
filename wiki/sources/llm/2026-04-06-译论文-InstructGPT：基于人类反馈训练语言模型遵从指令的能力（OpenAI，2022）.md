---
title: "[译][论文] InstructGPT：基于人类反馈训练语言模型遵从指令的能力（OpenAI，2022）"
created: 2026-04-15
updated: 2026-04-15
type: source
tags:
  - llm-theory
sources:
  - raw/web/llm-theory/2026-04-06-译论文-InstructGPT：基于人类反馈训练语言模型遵从指令的能力（OpenAI，2022）.md
status: summarized
---
## 内容摘要
本文翻译自 2022 年 OpenAI 的论文： [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) ， 整理翻译了其中感兴趣的部分。 ![[raw/assets/attachments/llm/fig-1 1.png]]

## 关键要点
- - [2.1.1 RLHF：来自游戏领域](#211-rlhf来自游戏领域)
- 先收集一组 **==“预期的模型行为应该是什么样”==** 的数据集， 然后使用 **==监督学习来微调 GPT-3==** （SFT），
- 接着，收集一组排名形式组织的 **==模型输出==** （rankings of model outputs）作为数据集， 使用 **==人类反馈强化学习==** （RLHF）进一步微调上一步得到的模型。

## 来源信息
- 原始文件：2026-04-06-译论文-InstructGPT：基于人类反馈训练语言模型遵从指令的能力（OpenAI，2022）.md
- 来源类型：web
