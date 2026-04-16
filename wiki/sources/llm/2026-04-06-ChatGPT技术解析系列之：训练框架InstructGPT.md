---
title: "ChatGPT技术解析系列之：训练框架InstructGPT"
created: 2026-04-15
updated: 2026-04-15
type: source
tags:
  - llm
sources:
  - raw/web/llm/2026-04-06-ChatGPT技术解析系列之：训练框架InstructGPT.md
status: summarized
---
## 内容摘要
目录 收起 一、chatGPT设计思想 1、教会模型怎么说话 2、引导模型按照人类的意图（intention）说话 3、给模型的回答进行排序/打分 4、将打分结果反馈给模型，帮助模型更好总结人类意图 二、GPT3、GPT3.5与GPT-SFT 三、奖励模型（RM, Reward Model） 四、基于人类反馈的强化学习（RLHF）

## 关键要点
- **action** ：(prompt, completion)对，prompt表示问题，completion表示模型的回答。
- **reward** ：(prompt completion)对的得分。
- **state** ：根据得分结果，优化迭代GPT3/GPT3.5，改变状态，得到最终的chatGPT

## 来源信息
- 原始文件：2026-04-06-ChatGPT技术解析系列之：训练框架InstructGPT.md
- 来源类型：web
