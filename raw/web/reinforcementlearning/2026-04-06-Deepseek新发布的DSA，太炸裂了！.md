---
author:
- null
- '[[不戒]]'
created: 2026-04-06
created_at: 2026-04-06
description: DeepSeek-V3.2-Exp 技术报告解读
source_type: web
status: inbox
tags:
- null
- clippings
title: Deepseek新发布的DSA，太炸裂了！
topics:
- 强化学习
source_url: https://mp.weixin.qq.com/s/He9uruxD9UgA51_4XbTZBw
published_at: null
related_concepts: []
---

不戒 *2025年9月30日 21:03*

**✅** **我是丁师兄，专注于智能驾驶大模型，持续分享LLM面试干货。**

**✅** ，已帮助多名同学成功上岸

**offer捷报**

![[Image 98.webp|图片]]

又一位学员报喜！ [二本背景，成功拿下大模型offer](https://mp.weixin.qq.com/s?__biz=MzkyNjczNjY1NQ==&mid=2247491569&idx=1&sn=028317671558cfd99cd5afd143572129&scene=21#wechat_redirect) ，年包30W左右，薪资怒涨50%！

为了助力秋招， [训练营迎来核弹级更新](https://mp.weixin.qq.com/s?__biz=MzkyNjczNjY1NQ==&mid=2247490799&idx=2&sn=e8bba9ff11afe11d9037c19c6deb5794&scene=21#wechat_redirect) ，我将手把手带大家实战一个真实企业级项目，此外也增加了多模态专题【面试常考】。准备秋招的小伙伴们，卷起来吧！

看到了 DeepSeek 在 huggingface 上创建了一个新项目，还是熟悉的味道，选择在长假前发布模型 DeepSeek-V3.2-Exp（全员卷王体质啊，还有点人性还是留了一天时间给各个云厂商更新线上的模型）。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

与以往不一样，这次模型和技术报告居然一起更新了，那么在下载模型的过程中，咱们就顺便看下技术报告，有哪些创新的地方，值不值得放弃中秋国庆假期去深入研究一下。

01

**模型架构**

DeepSeek-V3.2-Exp 的架构核心整体是在前段时间发布的 DeepSeek-V3.1-Terminus 模型上改进的，主要创新点（改进点）是在持续学习的过程中引入了一个新的原创注意力机制——DeepSeek Sparse Attention（DSA）。

技术报告也提到这个注意力机制主要是为了在长上下文序列的场景下提升训练和推理的计算效率（说白了就是省钱）。报告中也给出了成本节约的对比图。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

可以从图中看出，在长上下文场景下推理时的成本相对 V3.1 是大幅下降而且在 128K 的场景下降成本远超了 50%。

emmm，所以官网 api 降价 50% 的定价原因，应该是从之前他们说的 64K 常用的长度出发的吧，应了黄教主那句话，“你用得越多越便宜”。

这里还有个细节，V3.2 Exp 是基于 3.1 的持续学习，也就是说通过这个新的注意力机制。

DeepSeek 可以实现对模型低成本的持续训练参数更新，也就是可以通过低成本的持续学习去不断地让模型学习现在正在生产的人类知识。

本来已经开始被人嫌弃的 RAG 方案现在更加雪上加霜～没有了成本顾虑，以后就是长上下文的时代。

在报告中也提到了 V3.2 的模型主要是使用 128K 的数据进行持续学习的，意味着它能够处理最长达 128K 个 token 的长文本输入，相比较于之前的版本，在长上下文的场景下 V3.2 会有更好的表现。

02

**Lightning Indexer**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**Lightning Indexer** 是 DSA 的关键组件。主要负责计算查询 token（query token）于前文 token（preceding token）的索引分数，通过分数去确定 query token 需选择哪些 token，目的是降低计算量，提升长上下文场景下模型的训练和推理效率。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

DeepSeek 团队在技术报告也提到，DSA 也是采用 MQA（Multi-Query Attention）模式设计的，为的是与 DeepSeek-V3.1-Terminus 兼容以进行持续训练。

同时使用 ReLU 作为激活函数，主要是为了提升计算吞吐量。由于 Lightning Indexer 的头数 Heads 较少，且能采用 FP8 精度进行计算，其计算效率非常高。

该分数决定了哪些 tokens 会被选择，分数越高，被选择的可能性越大。

也因为 MLA 和 DSA 都是基于 MQA 的模式设计，可以实现 KV 参数的共享。

在这个架构中，Lightning Indexer 先通过计算索引分数筛选 token，再配合后续的注意力计算模块（MLA），共同完成稀疏注意力机制的功能，使得模型在处理长序列时能更高效地聚焦关键信息。

03

**训练**

报告中提到 V3.2 的模型训练分为了三个阶段：

持续预训练（Continued Pre-Training）：包括 Dense Warm-up Stage 和 Sparse Training Stage。

Dense Warm-up Stage 主要是为 DSA 注意力机制的核心组件 Lightning Indexer 提供初始参数，并使其输出与原有密集注意力的分布对齐，避免因新组件引入导致模型性能波动。

这一步仅用 1000 步（总计 2.1B token）实现索引器与主注意力的分布对齐，为后续稀疏训练铺垫基础，且未破坏主模型原有的长上下文处理能力。

Sparse Training Stage 引入 “细粒度 token 选择机制”（fine-grained token selection mechanism），让主模型与索引器共同适配 DSA 的稀疏注意力模式，同时保持索引器筛选逻辑的准确性。

在 15000 步（总计 943.7B token）训练后，可精准定位对查询 token 重要的键值对，且主模型语言建模能力未出现显著退化。

后训练（Post-Training）：该阶段沿用 DeepSeek-V3.1-Terminus 的训练流水线、算法与数据，仅采用 DSA 稀疏注意力模式。

核心目的是 “在稀疏架构下补全多任务能力，验证 DSA 对性能的影响”，分为专家蒸馏（Specialist Distillation）和混合 RL 训练（Mixed RL Training）两个模块。

专家蒸馏是让稀疏架构的模型吸收各领域 “专家模型” 的能力，避免因稀疏化导致特定领域性能下降，同时降低大规模领域训练的成本。

针对 6 大领域：数学、竞赛编程、通用逻辑推理、智能体编码、智能体搜索、写作 / 通用问答，用专家模型生成 “长思维链推理” 和 “直接响应” 两类数据，让主模型通过 “蒸馏” 学习专家知识。

混合 RL 训练是为了融合 “推理、智能体、人类对齐” 三大训练目标，在稀疏架构下平衡多领域性能，同时解决传统多阶段 RL 训练的 “灾难性遗忘” 问题（即训练新任务时忘记旧任务能力）。

这个阶段依然是采用 GRPO（Group Relative Policy Optimization）算法，将多阶段训练合并为单 RL 阶段。

报告也给出了 DSA 的效果，除了上面的效率提升（成本下降）以外，也提到了在 BrowseComp（搜索智能体）、SWE Verified（代码智能体）等任务上的训练曲线与 DeepSeek-V3.1-Terminus 高度对齐（这里的重点是，省了一半的成本就实现了与 V3.1 媲美的效果）。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

综上，DeepSeek-V3.2-Exp 贯彻了 DeepSeek 一贯的节约资源、勤俭持家的作风。

并且针对长上下文训练以及那么多排行榜就选了 BrowseComp 和 SWE Verified。

这两个榜单也说明了 DeepSeek 在 Agent 基础模型技术上一直持续发力并不是外界说的没有跟进热点关注，相反未来 DeepSeek 在 Agent 的应用潜力更加可期。

作者：不戒，已获作者授权发布

来源：https://zhuanlan.zhihu.com/p/1956122182821344546  

**END**

**加入学习**

**✅** **我是丁师兄，专注于智能驾驶大模型，持续分享LLM面试干货。**

**✅** ，已帮助多名同学成功上岸

**微信：** **dsxaigc**  

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

继续滑动看下一个

丁师兄大模型

向上滑动看下一个