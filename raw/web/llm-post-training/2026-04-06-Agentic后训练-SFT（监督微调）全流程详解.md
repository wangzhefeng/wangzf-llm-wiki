---
source_type: web
title: "Agentic后训练 - SFT（监督微调）全流程详解"
author:
  - 
  - "[[笨鸟先飞]]"
created_at: 2026-04-06
status: inbox
published: 
created: 2026-04-06
description: "本文将从Agentic SFT入手，介绍SFT如何赋能智能体（Agent），从而真正使得大模型能够创造生产力。"
tags:
  - 
  - "clippings"
source_url: "https://mp.weixin.qq.com/s/mLpaek5BMWx3gWSC_UhIhw"
published_at: null
related_concepts: []
topics:
  - llm-post-training
  - 大语言模型后训练
---

笨鸟先飞 *2026年1月8日 19:50*

*原文：https://zhuanlan.zhihu.com/p/1981322057150141868*

在大模型技术飞速发展的现在，学术界和工业界已有很多针对大模型监督微调（Supervised Fine-Tuning）的详细调研和总结。

目前业界尚未对Agentic SFT有较为详细的入门介绍和案例讲解，本文将从Agentic SFT入手，介绍SFT如何赋能智能体（Agent），从而真正使得大模型能够创造生产力。

## 1、什么是SFT? 为什么需要SFT？

### 1.1 SFT基础概念

想要了解微调，就需要了解大模型训练的“全过程”。如果你正在从0到1训练一个大语言模型，你需要经历：

**预训练** ：模型在庞大无标签文本上学习通用语言规律和世界知识（成本极高，通常由大公司完成）。

**后训练** ：这是将“知识渊博”但“未经驯化”的预训练模型，转化为“有用、无害、诚实”的助手的核心过程。此阶段成本远低于预训练，但至关重要，直接决定了模型的可用性和安全性。它通常包含几个关键子步骤：

- • **监督微调（SFT）** ：使用高质量的人工编写（或合成）的“指令-回答”配对数据，教会模型理解并遵循人类的指令格式。
- • **奖励模型训练** ：训练一个能判断回答质量的“打分器”，其依据是人类对同一问题的多个答案的偏好排序。
- • **基于人类反馈的强化学习（RL）** ：利用上一步的“打分器”，通过强化学习算法（如PPO，GRPO）引导模型优化其回答，使其更符合人类的价值观和偏好。

SFT，即监督微调，是帮助大模型在后训练中实现其最终目标的第一步。

![[Image 96.webp|图片]]

图1 大模型训练流程（预训练-监督微调）

### 1.2 为什么需要SFT（重要）

在这里，再次强调系列文章第一部分所提到的点：为什么我们需要SFT？

从训练的角度来看，SFT可以通过人类标注的模式，使得大模型在达成的效果上和人类的目标和价值观对齐，并且可以通过“从参数规模较大的大模型中生成特定任务的问答对去训练小模型”的方式，来减少模型的参数量，用更小的模型实现精确的具体领域的任务。

在此基础上，从大模型Agent应用的角度来看，在Agent执行任务的过程中，经过SFT+RL（RL会在后文进一步介绍）的小模型能够在不损失精度的情况下，用更高的效率处理大量的推理任务。

同时，参数量更小的模型对硬件设备要求更低，更易本地部署，从而解决从外部调用大模型API可能造成的用户隐私泄露问题。

**综上所述，SFT，尤其是Agentic SFT是帮助大模型在完成特定任务的同时兼顾精度、成本与推理效率的重要工具** 。

同时，也有人要问，既然RL（reinforcement learning）是通过让大模型和环境交互来学习到更加符合人类价值观和偏好的方法，为什么还要在RL之前进行SFT呢？

下文SFT的数学原理和后面系列文章即将介绍的RL数学原理会给你答案。

简而言之，在RL训练中，如果我们直接跳过SFT而进行RL的冷启动（冷启动是指从一个相对比较原始的参数水平开始训练模型），那么在大模型和环境交互的过程中，很可能会出现因为大模型初始水平较差、任务难度较高而导致的执行任务失败率高、奖励信号稀疏的问题，即很难得到正向的RL反馈，从而使得训练徒劳无功。

在这里举一个Deepanalyze-8B论文 <sup>[1]</sup> 的例子，在这篇论文里，作者希望训练模型使其拥有“调用多个数据科学工具并合理编排执行”的能力。

但在实际训练中，如果一开始就让大模型去做复杂的数据科学任务，那么大模型成功执行任务并反馈的概率会非常低。这篇论文通过微调步骤，先让大模型学会调用单个工具，而后再去使用RL教会大模型使用多个工具，从而解决了奖励信号稀疏的问题。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图2 Deepanalyze-8B 训练过程（先微调再强化学习）

综上所述，如果在RL之前使用SFT对大模型进行“岗前培训”，大模型会在RL的“实战操作”过程中有更好的表现和更快的学习速度。

### 1.3 如何获取SFT的训练数据？

一般来说，SFT训练数据的核心是高质量的“指令-输出”配对数据。模型在训练时，会接收一个“指令”，尝试生成一个“输出”，然后将其与数据集中提供的“标准输出”进行比较，计算损失函数，并反向传播以更新模型权重。

这个过程明确地“监督”模型去学习“对于这个指令，我应该生成那样的回答”，因此被称为监督微调。下面给几个例子方便读者理解。

Qwen3-SFT最佳实践数据格式模板 <sup>[2]</sup> ：

```
# 通用格式
{"messages": [
    {"role": "system", "content": "<system-prompt>"},
    {"role": "user", "content": "<query1>"},
    {"role": "assistant", "content": "<response1>"}
]}
# 带think的格式
{"messages": [
    {"role": "user", "content": "Where is the capital of Zhejiang?"},
    {"role": "assistant", "content": "<think>\n...\n</think>\n\nThe capital of Zhejiang is Hangzhou."}
]}
```

SFT的训练数据示例：

```
{
  "messages": [
    {"role": "user", "content": "写一首关于春天的诗"},
    {"role": "assistant", "content": "春风拂面柳丝长，\n百花争艳满园香。\n燕子归来寻旧巢，\n人间处处是韶光。"}
  ]
}
```

多轮对话的SFT训练数据示例：

```
{
  "messages": [
    {"role": "user", "content": "你好！"},
    {"role": "assistant", "content": "你好！有什么可以帮助你的吗？"},
    {"role": "user", "content": "我想学习Python，应该从哪里开始？"},
    {"role": "assistant", "content": "学习Python可以从以下几个步骤开始：\n1. 安装Python环境\n2. 学习基础语法\n3. 练习小项目\n你想先从哪个部分了解？"},
    {"role": "user", "content": "基础语法有哪些重要概念？"},
    {"role": "assistant", "content": "Python基础语法的核心概念包括：\n- 变量和数据类型\n- 条件语句（if/else）\n- 循环（for/while）\n- 函数定义\n- 列表、字典等数据结构\n建议先掌握这些，然后通过实际编码巩固。"}
  ]
}
```

Agentic SFT的训练数据格式示例:

```
{
  // 1. 智能体身份定义
  "agent_definition": {
    "name":"数据分析助手",
    ...
  },

  // 2. 完整的交互轨迹
  "interaction_trajectory": [
    {
        "turn": 1,
        "role":"user",
        "message":"帮我分析我手上股票的发展前景"
    },
    {
        "turn": 2,
        "role":"assistant",
        "message":"好的，为了....我现在需要...."
        "action":"调取用户数据..."
        "plan": [
            {"id":"t1","task":"..."},
            {"id":"t2","task":"..."}
        ],
        "tool_calls":[
            ...
        ],
        ...
    },
  ],

  // 3. 元数据与评估信息
  "metadata": {
    "task_completed": true,
    "tools_used": ["t1", "t2"],
    "complexity": "medium",
    ...
  }
}
```

与普遍意义的SFT不同的是，Agentic SFT需要关注训练模型“感知需求”、“调用工具”、“获取环境反馈并交互”等智能体所需要的能力，其格式也随着Agent具体要求的变化而变化，在这里给大家提供一个参考样例——Deepanalyze训练数据：

```
https://huggingface.co/datasets/RUC-DataLab/DataScience-Instruct-500K/viewer/default/train?views%5B%5D=train&row=0
```

OpenAI在 InstructGPT 和 ChatGPT 的初期开发中，为人机对齐设定了黄金标准。

他们的方法核心是通过人类反馈来构建和精炼数据 <sup>[3]</sup>,由于人工标注成本极高、规模有限，目前社区和工业界广泛采用的一种高效方法是：使用一个更强的“教师模型”（如GPT-4、Claude-3等），通过精心设计的Prompt，来为大量用户指令生成高质量的回复，从而蒸馏出SFT数据集。相关数据收集、合成方法，本部分系列文章会有详细介绍，接下来让我们主要关注本文的核心重点：SFT的原理和实现。

## 2、SFT的数学原理和常用技术

### 2.1 数学原理

与传统监督学习相同，SFT通过最大化由人工标注数据定义的条件似然函数，从而使模型输出更接近人类目标响应，并依据此计算损失函数（Loss），反向传播（Backpropagation）更新大模型的参数。

在监督微调中，训练的核心目标是是最大化似然函数，这里给一个简单的计算例子：

给定： 输入（指令、prompt）: 标准输出序列（每一个元素为输出的token,序列长度为T）：

假设当前语言模型参数为，语言模型从输出的自回归分布为：

其中：

该公式的含义为每一个输出的token，计算在已知输入和前序tokens生成的情况下，模型（参数）输出该token的概率，并计算中所有概率的乘积。

在每一个单独的时间步 ，模型接收 和 ，并输出一个未归一化的logits向量, 对该向量施加softmax，得到整个词汇表上该时间步的条件概率分布：

目标token 的对数概率为：

其中，为模型输出token 的logits分数，为词汇表的大小。

基于以上的计算公式，样本总损失（通过 “交叉熵损失” 来计算）可以计算为：

如果本次训练采取了B个批量的”指令-输出对”，那么损失可以计算为：

在计算清楚损失之后，我们需要计算损失对模型参数 的梯度，并根据梯度来反向传播(Backpropagation)更新参数θ，目标是使得反向传播后的模型，损失函数值得到减少。

对于逻辑值向量，首先计算损失函数的梯度,该梯度通过模型的最后一层（通常是投影层）反向传播，计算该层权重和输入的梯度。然后，通过Transformer 的每一层（如自注意力、前馈网络）继续反向传播，利用链式法则计算每一层内部参数：

### 2.2 参数更新

在训练过程中，如果每次反向传播都更新大模型的整体参数，即全参数微调，这种方式通常能获得最好的任务适配能力，但这种训练很容易被参数规模巨大（如百亿、千亿量级）掣肘，从而显著增加显存开销与训练时间，且容易发生过拟合。

因此，在大模型训练中往往不直接采用全参数微调，而是引入 参数高效方法。 参数高效微调（Parameter-Efficient Fine-Tuning）方法通过 冻结大部分预训练参数，仅在有限的可训练模块上进行更新，从而减少训练成本并保持原模型的通用能力。

典型代表包括 LoRA 与 P-Tuning v2：

(a) **LoRA** ：低秩适配Low-Rank Adaptation <sup>[4]</sup> LoRA 的核心思想是：对于某些权重矩阵，不直接更新，而是在其上插入一个可训练的低秩分解：

通过仅训练A，B，其他参数全部冻结，可以大幅减少显存开销和训练时间，且性能接近甚至优于全参数微调。

(b) **P-Tuning v2** ：深度连续提示微调 <sup>[5]</sup> P-Tuning v2的核心思想是：冻结整个预训练模型的所有参数，仅在输入层和模型的每一层（即深度）前添加少量可训练的连续提示向量（Continuous Prompt Vectors），通过优化这些提示向量来指导模型适应下游任务。

对于某一层 l的输入序列 （包含原始的 个 token 嵌入），P-Tuning v2 会为其添加 个连续的提示向量 ：

：第 l 层的可训练提示矩阵，包含 m 个 d 维向量。 ：该层原始的输入表示（token embeddings 或上一层的输出）。 ：拼接后送入第 层 Transformer 块的新输入。

训练时：只有所有 （共 L+1 组，L 为模型层数）是可训练参数，模型主体完全冻结。 推理时：这些学习到的提示向量与输入一起构成新的上下文，引导模型生成符合任务要求的输出。

### 2.3 梯度优化

在 SFT（Supervised Fine-Tuning，监督微调）中，大模型通常具有数十亿到数千亿参数，并且训练数据来源多样——指令、问答、代码、对话等。

传统的 SGD（随机梯度下降）或者BGD（批量梯度下降） 在这种场景下表现差，主要问题包括：

- • 梯度变化巨大，易振荡，难以收敛；
- • 大量稀疏参数（例如词向量、注意力矩阵某些维度）更新效率低；
- • 学习率难以统一设定；

基于以上问题，使用梯度优化器可以很好地解决，现有的主流优化器主要有AdaGrad, Momentum和Adam等。

(a) **AdaGrad** —— 自适应学习率Adaptive Gradient <sup>[6]</sup> AdaGrad为每个参数维护一个累积的梯度平方和，使频繁更新的参数学习率减小，稀疏参数学习率增大，特别适合处理稀疏特征。 参数 在时间步 的更新过程如下： 累计梯度平方和：

参数更新：

：累计梯度平方（二阶矩），维度与 相同，初始为0。 ：全局基础学习率。 ：平滑项（通常为 10^{-8} 量级），防止分母为零。

(b) **Momentum** —— 动量梯度Gradient Momentum <sup>[7]</sup> 动量法引入“速度”变量，将历史梯度以指数衰减形式累积，帮助加速收敛并抑制震荡。 动量更新：

参数更新：

：当前时刻的动量（速度），维度与 相同，初始为0。 ：动量衰减系数（通常取0.9），控制历史梯度的影响程度。 ：学习率。

(c) **Adam** —— 自适应动量估计Adaptive Moment Estimation <sup>[8]</sup> Adam结合了Momentum（一阶矩估计）和AdaGrad（二阶矩估计）的优点，并引入了偏差校正，是大模型训练中应用最广泛的优化器。 更新一阶矩（动量）和二阶矩估计:

计算偏差校正后的一阶矩和二阶矩（针对初始时刻的估计偏差）：

参数更新：

, ：分别为一阶矩（梯度均值）和二阶矩（梯度未中心化的方差）估计，初始为0。, ：矩估计的指数衰减率，通常取 。, ：偏差校正后的矩估计。 ：学习率。 ：数值稳定项，通常为 。

## 3、Agentic SFT

Agentic后训练通常有两种范式：

- • 第一种是基于人类反馈的SFT（SFT from Human Feedback）：将人类标注的“最优”轨迹作为监督数据，使用标准SFT损失进行训练。
- • 第二种是基于强化学习的微调（如RLHF中的PPO阶段）：使用策略梯度方法最大化期望奖励。这是更纯粹的“Agentic”训练。

我们这篇文章主要关注的是第一种范式（SFT），第二种范式（强化学习,RL）将会在之后的系列文章中详细介绍。

广义上的LLM SFT和Agentic SFT在数学原理和技术实现上基本是一致的，然而在实现细节上，两者有很大的区别：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

总体而言，在Agent能力优化上，Agentic SFT 把监督学习的稳定性与可控性带入“工具使用/行动决策 <sup>[9]</sup> ”场景：它是构建可靠、可解释且高效的 LLM agent 的核心第一步——先学会“怎样规范地行动”，再用更昂贵/不稳定的方法（如 RL）去优化长期回报。

## 4、Agentic SFT的发展前景

未来，大模型驱动的智能体应用会逐渐加速落地到生活的方方面面，Agentic后训练，尤其是Agentic后训练的第一步Agentic SFT，将会在赋能Agent落地中发挥越来越重要的作用。在作者看来，在Agentic SFT的未来发展上，有以下几点值得关注的地方：

- • **训练数据的效率与泛化** ：现有高质量专家轨迹数据稀缺、获取、合成成本高昂，需要探索高效获取训练数据的方法；
- • **多模态与复杂环境理解** ：现实任务常涉及视觉、物理环境等多模态信息，当前文本SFT存在局限，具身智能的应用有很大的发展空间；
- • **长程规划与复杂工具调用** ：任务步骤增多时，规划一致性、工具组合的可靠性急剧下降，需要通过加强Agent框架设计，配合SFT和RL来提升Agent的规划调用能力；
- • **评估体系的标准化与复杂化** ：现有基准中，缺乏超越简单任务完成率的、针对复杂Agent能力的评估benchmark，针对Agent能力，训练效果的评测，亟需一个通用的框架来进行标准化和统一化。

希望这篇文章能够在SFT，尤其是Agentic SFT方面给各位读者一定的启发，后续我们会针对Agentic SFT的下一个训练步骤–Agentic RL进行详细介绍，来帮助大家更好地掌握Agentic后训练的全流程。

## 参考文献

```
[1] https://medium.com/data-science-collective/supervised-fine-tuning-step-by-step-aefe6fbe5e09
```

#### 引用链接

`[1]` Deepanalyze-8B论文: *https://arxiv.org/pdf/2510.16872*  
`[2]` Qwen3-SFT最佳实践数据格式模板: *https://swift.readthedocs.io/zh-cn/latest/BestPractices/Qwen3-Best-Practice.html#id3*  
`[3]` 通过人类反馈来构建和精炼数据: *https://proceedings.neurips.cc/paper\_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf*  
`[4]` Low-Rank Adaptation: *https://arxiv.org/abs/2106.09685*  
`[5]` 微调: *https://arxiv.org/abs/2110.07602*  
`[6]` Adaptive Gradient: *https://www.learningtheory.org/colt2010/papers/023Duchi.pdf*  
`[7]` Gradient Momentum: *https://papers.baulab.info/papers/also/Polyak-1964.pdf*  
`[8]` Adaptive Moment Estimation: *https://arxiv.org/abs/1412.6980*  
`[9]` “工具使用/行动决策: *https://arxiv.org/pdf/2302.04761*  

继续滑动看下一个

吃果冻不吐果冻皮

向上滑动看下一个