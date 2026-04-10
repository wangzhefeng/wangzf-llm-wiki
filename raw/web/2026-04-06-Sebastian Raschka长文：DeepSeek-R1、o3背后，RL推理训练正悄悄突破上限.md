---
source_type: web
title: "Sebastian Raschka长文：DeepSeek-R1、o3背后，RL推理训练正悄悄突破上限"
author: 
created_at: 2026-04-06
topics:
  - 强化学习
status: inbox
source: "https://mp.weixin.qq.com/s/Bmiimack-HEzlsgu-WiHKg"
published: 
created: 2026-04-06
description: "推理模型的「后训练时代」你准备好了吗？"
tags:
  - 
  - "clippings"
---

*2025年4月21日 15:02*

选自Sebastian Raschka博客

**机器之心编译**

**机器之心编辑部**

> 只靠模型尺寸变大已经不行了？大语言模型（LLM）推理需要强化学习（RL）来「加 buff」。

著名 AI 研究者和博主 Sebastian Raschka 又双叒叕更新博客了。

这次的主题是《LLM 推理的强化学习现状》。

![[Image 106.webp|image.png]]

博客地址：https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training

这个月 AI 社区很热闹，尤其是 Llama 4 和 GPT-4.5 等新旗舰模型的发布。但你可能已经注意到，人们对这些新模型的反应相对平淡。原因之一可能是 Llama 4 和 GPT-4.5 仍然是传统的模型，这意味着它们的训练没有使用明确的强化学习进行推理。

与此同时，xAI 和 Anthropic 等强劲对手在其模型中增加了更多推理能力和功能。例如，Grok 和 Claude 的界面现在都为某些模型添加了一个「思考」（或扩展思考）按钮，可以明确切换推理功能。

无论如何，Llama 4 和 GPT-4.5（非推理）模型的低迷反响表明，我们正接近仅靠扩展模型规模和数据所能达到的极限。

然而，OpenAI 近期发布的 o3 推理模型表明，在战略性投入计算资源方面，特别是通过针对推理任务量身定制的强化学习方法仍有相当大的改进空间。据 OpenAI 员工在直播中介绍，o3 使用的训练计算资源是 o1 的 10 倍。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图源：OpenAI o3 与 o1 的性能与算力比较。

虽然单靠推理并非灵丹妙药，但确实能提升模型在挑战性任务上的准确率和解决问题的能力（目前为止）。因此，Sebastian 预计以推理为重点的后训练将成为未来 LLM 流程的标准做法。 本文将探讨强化学习在推理方面的最新进展。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图源：本文重点介绍用于开发和改进推理模型的强化学习训练方法。

本文主要内容包括以下几部分：

- 理解推理模型；
- RLHF（Reinforcement Learning from Human Feedback）基础：一切从何而来；
- PPO（Proximal Policy Optimization）简介：强化学习的核心算法；
- RL 算法：从 PPO 到 GRPO（Generalized Return and Policy Optimization）；
- RL 奖励模型：从 RLHF 到 RLVR（Reinforcement Learning with Verifiable Rewards）；
- DeepSeek-R1 推理模型的训练方法；
- 从最近关于训练推理模型的 RL 论文中汲取的教训；
- 值得关注的推理模型训练研究论文。

下文以作者第一人称口吻陈述。

理解推理模型

我们首先来了解推理的定义。简而言之，推理（reasoning）是指使 LLM 能够更好地处理复杂任务的推理（inference）和训练技巧。为了更详细地解释如何实现这一点（目前为止），我定义如下：在 LLM 的语境中，推理是指模型在提供最终答案之前生成中间步骤的能力。

这个过程通常被称为思维链 (CoT) 推理。在思维链推理中，LLM 会明确生成一个结构化的语句或计算序列，以说明其如何得出结论。具体如下图所示：

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

LLM 如何处理多步骤推理任务的简单图例。模型并非仅仅回忆一个事实，而是需要结合多个中间推理步骤才能得出正确的结论。根据具体实现方式，中间推理步骤可能会显示给用户，也可能不会显示。

如果你对推理模型还不熟悉，希望看到更全面的介绍，推荐我之前的文章：

- 文章 1：https://magazine.sebastianraschka.com/p/first-look-at-reasoning-from-scratch
- [Sebastian Raschka：关于DeepSeek R1和推理模型，我有几点看法》](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650954131&idx=2&sn=1d90cf8ef42ebe40d91b27f5ceca4b47&scene=21#wechat_redirect) https://magazine.sebastianraschka.com/p/understanding-reasoning-llms

LLM 的推理能力可以通过两种方式得到提高，OpenAI 博客文章中的一张图很好地说明了这一点：

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

准确率的提升可以通过增加训练或测试时计算来实现，其中测试时计算与推理时计算、推理时扩展是同义词。图源：https://openai.com/index/learning-to-reason-with-llms/

我此前介绍过测试时计算方法，本文想深入探讨一下训练方法。

RLHF 基础：一切从何而来

用于构建和改进推理模型的强化学习训练方法，或多或少与用于开发和对齐传统 LLM 的 RLHF 方法论相关。因此，在讨论基于强化学习训练的特定推理修改（modification）之前，我想先简单回顾一下 RLHF 的工作原理。

传统 LLM 通常经历以下三个步骤的训练过程：

- 预训练；
- 监督微调；
- 对齐（通常通过 RLHF 进行）。

「原始」的 LLM 对齐方法是 RLHF，它是遵循 InstructGPT 论文开发 LLM 时的标准方法之一，该论文描述了用于开发第一个 ChatGPT 模型的方法。

RLHF 的最初目标是使 LLM 与人类偏好保持一致。例如，假设你多次使用 LLM，并且 LLM 会针对给定的提示词生成多个答案。RLHF 会引导 LLM 生成更多你偏好的答案风格。RLHF 通常也用于对 LLM 进行安全调整：避免共享敏感信息、使用脏话等等。

具体来讲，RLHF 流程采用预训练模型，并以监督方式对其进行微调。这种微调尚未成为强化学习的一部分，但它主要是一种先决条件。

然后，RLHF 使用一种称为近端策略优化 (PPO) 的算法进一步对齐 LLM。请注意，除了 PPO 之外，还有其他算法可以替代。我特意提到 PPO，是因为它是 RLHF 最初使用的算法，并且至今仍是最流行的算法。）

为简单起见，我们可以分三个步骤来了解 RLHF 流程：

- RLHF 步骤 1（先决条件）：对预训练模型进行监督微调（SFT）；
- RLHF 步骤 2：创建奖励模型（RM）；
- RLHF 步骤 3：通过 PPO 进行微调。

RLHF 步骤 1（如下图所示）是一个监督微调步骤，用于创建基础模型，以便进一步进行 RLHF 微调。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图源：InstructGPT 论文。arXiv：https://arxiv.org/abs/2203.02155

在 RLHF 步骤 1 中，我们创建或采样提示词（例如从数据库中获取），并要求人类用户撰写高质量的回复。然后，我们使用该数据集以监督方式微调预训练的基础模型。如前所述，这在技术上并非 RL 训练的一部分，而仅仅是一个先决条件。

在 RLHF 步骤 2 中，我们使用监督微调得到的模型来创建奖励模型，如下图所示。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

如上图所示，对于每个提示词，我们会根据上一步创建的微调后的 LLM 生成四个回复。然后，人工标注员会根据他们的偏好对这些回复进行排序。虽然这个排序过程比较耗时，但与创建用于监督微调的数据集相比，它可能耗费更少的人力。这是因为对回复进行排序可能比编写回复更简单。

在编译包含这些排序的数据集后，我们可以设计一个奖励模型，该模型会输出奖励分数，用于 RLHF 步骤 3 中的后续优化阶段。这里的思路是：奖励模型可以取代并自动化耗费人力的人工排序，从而使大型数据集上的训练变得可行。

奖励模型通常源自上一步监督微调步骤中创建的 LLM。为了将 RLHF 步骤 1 中的模型转换为奖励模型，其输出层（下一个 token 分类层）将被替换为一个具有单个输出节点的回归层。

RLHF 流程的第三步是使用奖励模型对之前的监督微调模型进行微调，如下图所示。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在 RLHF 步骤 3（最后阶段）中，我们根据在 RLHF 步骤 2 中所创建奖励模型的奖励分数，使用 PPO 来更新 SFT 模型。

PPO 简介：强化学习的核心算法

如前所述，原始 RLHF 方法使用了强化学习算法 PPO。PPO 的开发是为了提高策略训练的稳定性和效率。在强化学习中，策略仅指我们想要训练的模型；在本例中，策略 = LLM。

PPO 背后的一个关键思想是：它限制了策略在每个更新步骤中允许的更改量。这是通过截断损失函数来实现的，有助于防止模型进行过大的更新，从而避免破坏训练的稳定性。

此外，PPO 还在损失函数中包含了 KL 散度惩罚。该惩罚项将当前策略（正在训练的模型）与原始 SFT 模型进行比较，鼓励更新结果保持合理的接近。毕竟，这样做的目的是根据偏好调整模型，而不是完全重新训练。

这就是 PPO 中「proximal」（近端）一词的由来：该算法试图使更新结果接近现有模型，同时仍允许改进。为鼓励探索，PPO 还添加了熵奖励，从而鼓励模型在训练期间改变输出。

接下来，我想介绍一些术语，以便在相对较高的层次上解释 PPO。这里涉及很多专业术语，因此在继续之前，我尝试在下图中总结一下关键术语。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

RLHF 中关键术语的说明。

下面我将通过伪代码来说明 PPO 中的关键步骤。此外，为了更直观地说明，我还将使用一个比喻：假设你是一位经营小型外卖服务的厨师。你不断尝试新的菜谱变化以提高客户满意度。你的总体目标是根据客户反馈（奖励）调整菜谱（策略）。

1、计算新旧策略中下一个 token 概率的比率：

```ini
ratio = new_policy_prob /old_policy_prob
```

简而言之，这会检查新旧策略的差异。 附注：关于「new\_policy\_prob」，我们尚未使用最终更新后的策略。我们使用的是当前的策略版本（即我们正在训练的模型）。不过，按照惯例，我们将其称为「新」。因此，即使你仍在进行实验，我们也会按照惯例将你当前的草稿称为「新策略」。

2、将该比率乘以行动（action）的优劣程度（称为优势）：

```ini
raw_score = ratio * advantage
```

这里，为了简单起见，我们可以假设优势是根据奖励信号计算的：

```ini
advantage = actual_reward - expected_reward
```

在厨师的类比中，我们可以将优势视为新菜的表现如何：

```ini
advantage = customer_rating - expected_rating
```

例如，如果一位顾客给新菜品打了 9 分（满分 10 分），而顾客通常给我们 7 分（满分 10 分），那么这就是 +2 的优势。

需要注意，这只是一个简化的描述。实际上，这涉及到广义优势估计（Generalized advantage estimation，GAE），这里不再赘述。然而，需要提及的一个重要细节是：预期奖励是由所谓的「评价者」（有时也称为价值模型）计算的，而奖励模型则计算实际奖励。也就是说，优势计算涉及另外两个模型，这些模型的规模通常与我们正在微调的原始模型相同。

举个例子，我们可以把这个评价者或价值模型想象成一位朋友，在将新菜品端上桌之前，我们会邀请他品尝。我们还会请这位朋友估计顾客会如何评价这道菜（这就是预期奖励）。奖励模型就是给出反馈（即实际奖励）的实际顾客。

3、计算截断分数：

如果新策略变化过大（例如比例 > 1.2 或 < 0.8），我们会按如下方式截断该比例：

```apache
clipped_ratio = clamp (ratio, 0.8, 1.2)clipped_score = clipped_ratio * advantage
```

举个例子，假设新菜谱的评价特别好（或特别差），我们可能会忍不住马上就彻底修改整个菜单。但这样做风险很大，因此我们暂时限制菜谱可以修改的范围。比如，我们可能把菜做得更辣了，而那位顾客碰巧喜欢吃辣，但这并不意味着其他人也喜欢。

4、然后，我们取原始得分和裁剪得分中较小的一个：

```python
if advantage >= 0:    final_score = min (raw_score, clipped_score)else:    final_score = max (raw_score, clipped_score)
```

这同样与保持谨慎有关。例如，如果优势是正的（新行为更好），我们限制奖励。这是因为我们不想过分信任一个可能只是巧合或运气的好结果。

如果优势是负的（新行为更差），我们限制惩罚。其理念是相似的。也就是说，除非我们非常确定，否则我们不想对一个不好的结果反应过度。

简而言之，如果优势是正的，我们取两个得分中较小的一个（以避免过度奖励），而如果优势是负的，则取较大的一个（以避免过度惩罚）。

在这个比喻中，这可以确保如果一个菜谱的表现好于预期，我们不会在不自信的情况下过度奖励它。如果表现不佳，除非它一直不好，否则我们也不会过度惩罚它。

5、计算损失：

这个最终得分就是我们在训练过程中要最大化的（通过梯度下降来最小化这个得分的符号反转值）。此外，我们还添加了一个 KL 惩罚项，其中 β 是惩罚强度的超参数：

```ini
loss = -final_score + β * KL (new_policy || reference_policy)
```

在这个比喻中，我们添加惩罚项是为了确保新菜谱与我们原来的风格不会差别太大。这可以防止你每周都「彻底改造厨房」。例如，我们不希望突然把一家意大利餐厅改造成烧烤店。

这些信息量很大，因此我通过下面的图，用一个具体的、数值化的例子在大型语言模型（LLM）的背景下进行了总结。但如果这太复杂了，你可以直接跳过；即使不看，也不会影响你理解文章的其他部分。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

我承认我在介绍 PPO 时可能有点过于详细了。但既然已经写出来了，删掉也挺难的。希望你们中的一些人会觉得它有用！

话虽如此，下一节中相关的要点是 PPO 中涉及多个模型：

1\. 策略模型：这是我们希望通过监督微调（SFT）进行训练并进一步对齐的大型语言模型（LLM）。

2\. 奖励模型：这是一个经过训练以预测奖励的模型（参见强化学习与人类反馈（RLHF）的第 2 步）。

3\. 评论家模型：这是一个可训练的模型，用于估计奖励。

4\. 参考模型（原始策略）：我们使用它来确保策略不会偏离太远。

顺便说一下，你可能会好奇为什么我们需要奖励模型和评论家模型。奖励模型通常是在使用 PPO 训练策略之前训练的。它通过自动化人类裁判的偏好标记来给策略 LLM 生成的完整响应打分。相比之下，评论家模型则用于评判部分响应。我们用它来创建最终响应。虽然奖励模型通常保持冻结状态，但评论家模型在训练期间会不断更新，以更好地估计奖励模型所创建的奖励。

PPO 的更多细节超出了本文的范围，但有兴趣的读者可以在以下四篇早于 InstructGPT 论文的文章中找到数学细节：

1\. 《异步深度强化学习方法（2016）》：由 Mnih、Badia、Mirza、Graves、Lillicrap、Harley、Silver 和 Kavukcuoglu 撰写，介绍了策略梯度方法，作为基于深度学习的强化学习（RL）中 Q 学习的替代方案。

2\. 《近端策略优化算法（2017）》：由 Schulman、Wolski、Dhariwal、Radford 和 Klimov 撰写，提出了一种改进的近端策略强化学习方法，该方法比普通的策略优化算法更具数据效率和可扩展性。

3\. 《从人类偏好微调语言模型（2020）》：由 Ziegler、Stiennon、Wu、Brown、Radford、Amodei、Christiano 和 Irving 撰写，阐述了 PPO 和奖励学习的概念，并将其应用于预训练语言模型，包括 KL 正则化，以防止策略与自然语言偏差过大。

4\. 《从人类反馈学习总结（2022）》：由 Stiennon、Ouyang、Wu、Ziegler、Lowe、Voss、Radford、Amodei 和 Christiano 撰写，介绍了后来在 InstructGPT 论文中也使用的流行的 RLHF 三步流程。

RL 算法：从 PPO 到 GRPO

如前所述，PPO 是 RLHF 最初使用的算法。从技术角度看，它在用于开发推理模型的 RL pipeline 中运行得非常好。不过，DeepSeek-R1 在他们的 RL pipeline 中使用的是一种名为「组相对策略优化（GRPO）」的算法，该算法在他们早期的一篇论文中已有介绍：

《DeepSeekMath： 突破开放语言模型中数学推理的极限》（2024 年）https://arxiv.org/abs/2402.03300

> DeepSeek 团队引入了 GRPO，这是近端策略优化（PPO）算法的一个变体，旨在增强数学推理能力，同时优化 PPO 的内存使用。

因此，这里的主要研究动机是提高计算效率。效率的提升是通过放弃「批评家」（价值模型）即计算价值函数（预期未来奖励）的大型语言模型（LLM）来实现的。与其依赖这个额外的模型来计算估计奖励以确定优势，GRPO 采取了一种更简单的方法：它从策略模型本身采样多个答案，并使用它们的相对质量来计算优势。

为了说明 PPO 和 GRPO 之间的差异，从 DeepSeekMath 论文中借用了一张很有用的图表：

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

RL 奖励建模：从 RLHF 到 RLVR

到目前为止，我们将 RLHF 视为一种程序，并介绍了两种常用的强化学习算法：PPO 和 GRPO。

但是，如果 RLHF 已是大型语言模型（LLM）对齐工具包的核心部分，那么这与推理有何关联呢？

DeepSeek 团队将类似的基于 RL 的方法（搭配 GRPO）应用于训练其 R1 和 R1-Zero 模型的推理能力，由此建立了 RLHF 与推理之间的联系。

不同之处在于，与依赖人类偏好并训练奖励模型不同，DeepSeek-R1 团队采用了可验证奖励。这种方法被称为带有可验证奖励的强化学习（RLVR）。

需要再次强调的是：与标准的 RLHF 相比，RLVR 规避了对奖励模型的需求。

因此，模型并非从人类标注样本中学习何为「优质」答案，而是从确定性工具（如符号验证器或基于规则的工具）处获取直接的二元反馈（正确或错误）。可将之理解为用计算器解决数学问题或用编译器来生成代码。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

具有可验证奖励（RLVR）的强化学习示例：模型接收提示以解决数学问题并生成答案。此时不使用学习奖励模型，而是由符号验证器（例如计算器）检查输出，并基于正确性提供二元反馈。

这样做的一个动机是，在强化学习期间，通过自动正确性检查作为监督信号，从而避免使用噪声大或成本高昂的人类反馈或 学习奖励。另一个动机是，借助计算器这类「廉价」工具，我们可以替代成本高昂的奖励模型训练以及奖励模型本身。由于奖励模型通常是整个预训练模型（只是带有回归头部），因此 RLVR 的效率要高得多。

总之，DeepSeek-R1 结合了 RLVR 与 GRPO，从而在训练过程中淘汰了两个成本高昂的模型：奖励模型和价值模型（评论家），如下图所示。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

大型语言模型（LLM）训练中强化学习设置的比较。传统的基于人类反馈的强化学习（RLHF）与近端策略优化（PPO）结合时，会同时使用基于人类偏好的奖励模型和评论家（价值模型）来指导学习。而广义策略优化（GRPO）则淘汰了评论家模型。更有甚者，当 GRPO 与带有可验证奖励的强化学习（RLVR）结合时，还去掉了奖励模型，转而依靠来自符号工具（如计算器或编译器）的可验证奖励。

在下一节中，我打算简要介绍 DeepSeek-R1 的训练流程，并探讨 DeepSeek 团队所使用的不同可验证奖励方法。

DeepSeek-R1 推理模型的训练方法

现在我们已经阐明了 RLHF 和 RLVR 以及 PPO 和 GRPO 的概念，接下来将简要回顾 DeepSeek-R1 论文中关于强化学习和推理的主要见解。

首先，存在三种类型的模型：

1\. 仅通过纯强化学习（RL）训练的 DeepSeek-R1-Zero。

2\. 通过指令微调（SFT）和强化学习（RL）共同训练的 DeepSeek-R1。

3\. 通过指令微调（SFT）且未使用强化学习（RL）创建的 DeepSeek-Distill 变体。

我绘制了一个 DeepSeek-R1 流程图，用以展示这些模型之间的关系，如下所示。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

DeepSeek-R1 系列的训练 pipeline

DeepSeek-R1-Zero 是使用可验证奖励（RLVR）与 GRPO 训练的，事实证明，这足以使模型通过生成中间步骤展现推理能力，也证明了跳过监督微调（SFT）阶段是可能的。该模型通过探索而非从示例中学习来提升推理能力。

DeepSeek-R1 是旗舰型号，性能最佳的主力模型，与 DeepSeek-R1-Zero 的区别在于，它交替使用了指令微调、RLVR 和 RLHF。

DeepSeek-Distill 变体旨在成为更小且更易部署的模型，它们是通过使用 DeepSeek-R1 模型的指令数据对 Llama 3 和 Qwen 2.5 模型进行指令微调生成的。这种做法在推理部分未使用任何强化学习（不过，Llama 3 和 Qwen 2.5 基础模型的创建用了 RLHF）。

关于 DeepSeek-R1 流程的更多讲解，可参阅我之前的《Understanding Reasoning LLMs》一文：

(https://magazine.sebastianraschka.com/p/understanding-reasoning-llms)

需要强调的是，DeepSeek 团队训练 DeepSeek-R1-Zero 时未使用基于 LLM 的奖励模型，而是对 DeepSeek-R1-Zero 和 DeepSeek-R1 的推理训练采用了基于规则的奖励：

在开发 DeepSeek-R1-Zero 时，我们没有应用结果或过程神经奖励模型，因为我们发现，在大规模强化学习过程中，神经奖励模型可能会出现奖励劫持问题。

为了训练 DeepSeek-R1-Zero，我们采用了一个主要由两种奖励组成的基于规则的奖励系统：

（1）准确性奖励：准确性奖励模型用于评估回答是否正确。例如，在数学问题有确定性结果的情况下，模型需要以指定格式（例如，在方框内）提供最终答案，以便可靠地进行基于规则的正确性验证。同样，对于 LeetCode 问题，可以使用编译器根据预定义的测试用例生成反馈。

（2）格式奖励：除了准确性奖励模型外，我们还采用了格式奖励模型，要求模型将其思考过程置于『<think>』和 『</think>』标签之间。

从最近关于训练推理模型的 RL 论文中汲取的教训

我意识到引言（即到此为止的所有内容）比我预想的要长得多。尽管如此，我还是认为有必要用这么长的篇幅来介绍下面的经验教训。

上个月，我阅读了大量有关推理模型的最新论文，并将其中最有趣的观点和见解归纳在本节中。

1、强化学习进一步改进蒸馏模型

DeepSeek-R1 论文清楚地表明，监督微调（SFT）后的强化学习（RL）优于单独的强化学习。

鉴于这一观察，直观地说，额外的强化学习应能进一步改进蒸馏模型（因为蒸馏模型本质上代表了通过使用大模型生成的推理样本进行 SFT 训练的模型）。

事实上，DeepSeek 团队明确观察到了这一现象：

> 此外，我们还发现，将 RL 应用于这些经过蒸馏的模型还能产生显著的进一步收益。我们认为这值得进一步探讨，因此在此仅介绍简单的 SFT 蒸馏模型的结果。

多个团队独立已验证了这些观察结果：

- \[8\] 研究人员使用 1.5B 的 DeepSeek-R1-Distill-Qwen 模型，仅用 7,000 个样本和 42 美元的计算预算，就证明了 RL 微调带来的性能大幅提升。令人印象深刻的是，这个小模型在 AIME24 数学基准测试中超过了 OpenAI 的 o1-preview。
- \[15\] 不过，另一个研究小组提醒说，这些收益在统计学上并不总是显著的。这表明，尽管 RL 可以改进较小的蒸馏模型，但基准结果有时可能夸大了改进效果。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

注释图来自《冷静看待语言模型推理的进展： 陷阱与复现之路》，https://arxiv.org/abs/2504.07086

2、冗长错误答案的问题

我之前提到过，有可验证奖励的推理（RLVR）并不严格要求使用 GRPO 算法；DeepSeek 的 GRPO 只是碰巧效率高、性能好而已。

然而，文献 \[12\] 表明，普通 PPO 搭配基本的二进制正确性奖励足以扩展模型的推理能力和响应长度。

更有趣的是，PPO 和 GRPO 都存在长度偏差。有几篇论文探讨了处理过长错误答案的方法：

\[14\] 提供了一项分析，说明了由于损失计算中的数学偏差，PPO 如何无意中偏向于较长的回答；GRPO 可能也存在同样的问题。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

摘自《通过强化学习进行简明推理》，https://arxiv.org/abs/2504.05185

作为上述声明的后续，\[7\] \[10\] 特别指出了 GRPO 中的长度和难度偏差。修改后的变体「Dr. GRPO」通过去除长度和标准差归一化，简化了优势计算，提供了更清晰的训练信号。

- \[1\] GRPO 中明确惩罚冗长的错误答案，同时奖励简洁正确的答案。
- \[3\] \[6\] 在 GRPO 中没有直接控制答案长度，但发现 token 级奖励是有益的，可以让模型更好地专注于关键推理步骤。
- \[5\] 在 GRPO 中对超过特定长度的回答引入明确的惩罚措施，从而在推理过程中实现精确的长度控制。

3、从 RL 中产生的能力

除了 DeepSeek-R1 论文中提到的顿悟时刻，RL 还被证明能够在模型中诱导出宝贵的自我验证和反思推理能力 \[2\]\[9\]。有趣的是，与顿悟时刻类似，这些能力是在没有明确指令的训练过程中自然出现的。

\[1\] 表明，扩展上下文长度（最多 128k tokens）可进一步提高模型的自我反省和自我修正能力。

4、超越特定领域的泛化

迄今为止，大多数研究工作都集中在数学或编码情境中的推理任务上。然而，\[4\] 通过在逻辑谜题上训练模型，证明了成功的泛化。在逻辑谜题上训练的模型在数学推理任务中也取得了很好的表现。这证明了 RL 能够诱导出独立于特定领域知识的通用推理行为。

5、扩展到更广泛的领域

作为上述部分的后续，另一个有趣的见解 \[11\] 是，推理能力可以自然地扩展到数学、代码和逻辑等结构化领域之外。模型已经成功地应用于医学、化学、心理学、经济学和教育等领域，利用生成式 soft-scoring 方法有效地处理自由形式的答案。

推理模型下一步的重要工作包括：

- 将现有的推理模型（如 o1、DeepSeek-R1）与外部工具使用和检索增强生成（RAG）等功能相结合；OpenAI 刚刚实现的 o3 模型在这方面铺平了道路；
- 说到工具使用和搜索，\[9\] 研究表明，赋予推理模型搜索能力，可诱导出自我修正和跨基准强泛化等行为，尽管训练数据集极少；
- 基于 DeepSeek-R1 团队在保持基于知识的任务性能方面所经历的艰辛，我认为为推理模型添加搜索能力几乎是不费吹灰之力的事。

6、推理是否完全归功于 RL？

DeepSeek-R1（和 R1-Zero）背后的基本观点是，RLVR 明确诱导推理能力。然而，最近的研究结果 \[10\] 表明，推理行为（包括 「顿悟时刻」）可能已经存在于基础模型中，这是因为对大量思维链数据进行了预训练。

我最近对 DeepSeek V3 基础模型和 R1 模型进行的比较强化了这一观点，因为更新后的基础模型也表现出了类似推理的行为。例如，原始 V3 模型和 R1 模型之间的比较清楚地显示了非推理模型和推理模型之间的区别：

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

不过，如果将更新后的 V3 基本型号与 R1 进行比较，情况就不一样了：

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

此外，\[13\] 还发现，在不同领域和模型大小的预训练中，自我反思和自我纠正行为会逐渐出现。这使得将推理能力完全归因于 RL 方法变得更加复杂。

也许结论是，RL 绝对能将简单的基础模型转化为推理模型。然而，这并不是诱导或提高推理能力的唯一方法。正如 DeepSeek-R1 团队所展示的，蒸馏也能提高推理能力。由于本文中的蒸馏指的是在思维链数据上进行指令微调，因此在包含思维链数据的数据上进行预训练很可能也会诱发这些能力。

（正如我在书中通过实践代码所解释的，预训练和指令微调毕竟是基于相同的下一个 token 预测任务和损失函数）。

值得关注的推理模型训练研究论文

在上个月阅读了大量推理论文之后，我试图在上一节中总结出最有趣的收获。不过，对于那些对更详细的资料来源感到好奇的人，我还在本节下面列出了 15 篇相关论文，作为选读。(为简单起见，以下摘要按日期排序）。

请注意，这份清单并不全面（我的上限是 15 篇），因为本文已经太长了！

\[1\] 扩展强化学习（和上下文长度）

22 Jan, Kimi k1.5: Scaling Reinforcement Learning with LLMs, https://arxiv.org/abs/2501.12599

有趣的是，这篇论文与 DeepSeek-R1 论文在同一天发表！在这里，作者展示了用 RL 训练的多模态 LLM。与 DeepSeek-R1 类似，他们没有使用过程奖励模型（PRM），而是采用了可验证奖励。PRM 是 RL 中使用的一种奖励模型（尤其是在 LLM 训练中），它不仅评估最终答案，还评估得出答案的推理步骤。

这里的另一个关键 idea 是，扩展上下文长度（最多 128k 个 token）有助于模型在推理过程中进行规划、反思和自我修正。因此，除了与 DeepSeek-R1 类似的正确性奖励外，它们还有长度奖励。具体来说，他们提倡较短的正确答案，而不正确的长答案则会受到更多惩罚。

他们还提出了一种名为 long2short 的方法，用于将这些长思维链技能提炼为更高效的 short-CoT 模型。(它通过使用模型合并、最短拒绝采样、DPO 和第二轮具有更强长度惩罚的 RL 等方法，从 long-CoT 模型中提炼出更短的正确答案）。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[2\] 大型推理模型的竞争性编程

3 Feb, Competitive Programming with Large Reasoning Models, https://arxiv.org/abs/2502.06807

这篇 OpenAI 的论文评估了他们的 o 系列模型（如 o1、o1-ioi 和 o3）在竞争性编程任务中的表现。虽然没有深入探讨如何应用 RL 的技术细节，但它仍然提供了一些有趣的启示。

首先，这些模型是使用基于结果的 RL 训练出来的，而不是基于过程的奖励模型。这与 DeepSeek-R1 和 Kimi 等方法类似。

其中一个有趣的发现是，o3 可以学习自己的测试时间（即推理时间扩展）策略。例如，它经常编写一个问题的简单粗暴版本（用效率换取正确性），然后用它来验证更优化解决方案的输出。这种策略不是手工编码的，而是模型自己想出来的。

总的来说，论文讨论了扩展通用 RL 允许模型开发自己的推理和验证方法，而不需要任何人类启发式方法或特定领域的推理 pipeline。相比之下，o1-ioi 等其他（早期）模型则依赖于手工制作的测试时间策略，例如对成千上万的样本进行聚类和重排，这需要大量的人工设计和调整。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[3\] 探索结果奖励的极限

10 Feb, Exploring the Limit of Outcome Reward for Learning Mathematical Reasoning, https://arxiv.org/abs/2502.06781

这篇论文探讨了仅有二进制「正确」或「错误」反馈的 RL（如 DeepSeek-R1 中的 RL）在解决数学问题方面能走多远。为此，他们首先使用 Best-of-N 采样来收集正面样本，并对这些样本应用行为克隆，结果表明理论上这足以优化策略。

为了应对奖励稀疏的挑战（尤其是当长思维链包含部分正确步骤时），他们添加了一个 token 级奖励模型，该模型可学习为推理的不同部分分配重要性权重。这有助于模型在学习时专注于最关键的步骤，并提高整体性能。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[4\] 基于规则强化的 LLM 推理（关于逻辑数据）

20 Feb, Logic-RL: Unleashing LLM Reasoning with Rule-Based Reinforcement Learning, https://arxiv.org/abs/2502.14768

DeepSeek-R1 专注于数学和代码任务。本文使用逻辑谜题作为主要训练数据，训练了一个 7B 模型。

研究人员采用了与 DeepSeek-R1 类似的基于规则的 RL 设置，但做了一些调整：

1\. 他们引入了严格的格式奖励，惩罚走捷径的行为，并确保模型使用 <think> 和 <answer> 标记将推理与最终答案分开。

2\. 他们还使用了系统提示，明确告诉模型在给出最终答案之前要先一步一步地思考问题。

即使只有 5K 个合成逻辑问题，模型也能发展出良好的推理能力，并能很好地推广到 AIME 和 AMC 等更难的数学基准测试中。

这一点特别有趣，因为它表明基于逻辑的 RL 训练可以教会模型推理的方式，并将其应用到原始领域之外。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[5\] 控制推理模型的思考时间

6 Mar, L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning, https://arxiv.org/abs/2503.04697

推理模型的一个特点是，由于思维链式推理，它们往往会产生较长的输出。但默认情况下，没有明确的方法来控制响应的长度。

这篇论文介绍了长度控制策略优化（LCPO），这是一种简单的强化学习方法，可帮助模型在优化准确性的同时遵守用户指定的长度限制。

简而言之，LCPO 类似于 GRPO，即「GRPO + 长度控制自定义奖励」，其实现方式为

```ini
reward = reward_correctness - α * |target_length - actual_length|
```

其中目标长度是用户提示的一部分。上述 LCPO 方法鼓励模型完全遵守所提供的目标长度。

此外，他们还引入了一个 LCPO-Max 变体，它不是鼓励模型完全匹配目标长度，而是鼓励模型保持低于最大 token 长度：

```apache
reward = reward_correctness * clip (α * (target_length - actual_length) + δ, 0, 1)
```

作者使用 LCPO 训练了一个名为 L1 的 1.5B 模型，它可以根据 prompt 调整输出长度。这样，用户就可以根据任务在准确性和计算量之间进行权衡。有趣的是，论文还发现，这些长链模型在短推理方面的表现也出人意料地好，在相同的 token 长度下，甚至超过了 GPT-4o 等更大的模型。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[6\] 在 LLM 中激励搜索能力

10 Mar, R1-Searcher: Incentivizing the Search Capability in LLMs via Reinforcement Learning, https://arxiv.org/abs/2503.05592

像 DeepSeek-R1 这样的推理模型是通过 RL 训练出来的，它们依赖于自己的内部知识。本文作者的研究重点是通过增加外部搜索系统的访问权限，在需要更多时间敏感信息或最新信息的知识型任务中改进这些模型。

因此，本文通过教这些模型在推理过程中使用外部搜索系统来改进它们。作者没有依赖测试时间策略或监督训练，而是采用了两阶段强化学习法，帮助模型学习如何以及何时自行搜索。模型首先学习搜索格式，然后学习如何使用搜索结果找到正确答案。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[7\] 开源 LLM 大规模强化学习

18 Mar, DAPO: An Open-Source LLM Reinforcement Learning System at Scale, https://arxiv.org/abs/2503.14476

虽然本文主要讨论开发类似 DeepSeek-R1 的训练流程并将其开源，但它也对 DeepSeek-R1 训练中使用的 GRPO 算法提出了有趣的改进。

1\. Clip-higher：增加 PPO 剪枝范围的上限，以鼓励探索并防止训练期间熵崩溃。

2\. 动态采样：通过过滤掉所有采样响应始终正确或始终错误的 prompt 来提高训练效率。

3\. token 级策略梯度损失：从样本级转移到 token 级梯度损失计算，以便更长的响应能够对梯度更新产生更大的影响。

4\. 过长奖励塑造：对因过长而被截断的响应添加软惩罚，以减少奖励噪音并有助于稳定训练。

标准 GRPO 采用样本级损失计算。这首先需要对每个样本的 token 损失求平均值，然后再对所有样本的损失求平均值。由于样本的权重相等，因此响应较长的样本中的 token 对整体损失的贡献可能会不成比例地较小。同时，研究人员观察到，较长的响应通常在最终答案之前包含一些乱码，而这些乱码在原始 GRPO 样本级损失计算中不会受到足够的惩罚。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[8\] 强化学习在小型 LLM 中的推理

20 Mar, Reinforcement Learning for Reasoning in Small LLMs: What Works and What Doesn't, https://arxiv.org/abs/2503.16219

DeepSeek-R1 的原始论文表明，在开发小型（较小）推理模型时，蒸馏比纯强化学习能取得更好的结果。在本文中，研究人员对此进行了跟进研究，并探索了如何利用强化学习进一步改进小型蒸馏推理模型。

因此，他们使用 1.5B 的 DeepSeek-R1-Distill-Qwen 模型，发现仅需 7000 个训练样本和 42 美元的计算预算，强化学习微调就能带来显著的提升。例如，在 AIME24 数学基准测试中，这些改进足以超越 OpenAI 的 o1-preview。

此外，该论文还有 3 个有趣的发现：

1\. 小型 LLM 可以在使用紧凑、高质量数据集的前 50-100 个训练步内实现快速推理提升。但是，如果训练时间过长，性能会迅速下降，这主要是由于长度限制和输出不稳定；

2\. 将较易和较难的问题混合在一起，有助于模型在训练早期产生更短、更稳定的响应。然而，随着时间的推移，性能仍然会下降；

3\. 使用余弦形奖励函数有助于更有效地控制输出长度，并提高训练一致性。但与基于准确率的标准奖励相比，这会略微降低峰值性能。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[9\] 学习通过搜索进行推理

25 Mar, ReSearch: Learning to Reason with Search for LLMs via Reinforcement Learning, https://arxiv.org/abs/2503.19470

本文提出的 ReSearch 框架扩展了 DeepSeek-R1 论文中的强化学习方法，将搜索结果纳入推理过程。该模型会根据其正在进行的推理链学习何时以及如何进行搜索，然后将检索到的信息用于后续的推理步骤。

这一切都是在推理步骤中无需监督数据的情况下完成的。研究人员还表明，这种方法可以产生诸如自我修正和反思等有用的行为，并且尽管只在一个数据集上进行训练，但它在多个基准测试中表现出色。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

PS：这个方法和之前讨论的 R1-Searcher 有什么不同？

R1-Searcher 采用两阶段、基于结果的强化学习方法。在第一阶段，它教会模型如何调用外部检索；在第二阶段，它学习如何利用检索到的信息来回答问题。

相比之下，ReSearch 将搜索直接集成到推理过程中。它使用强化学习对模型进行端到端训练，而无需对推理步骤进行任何监督。诸如反思错误查询并进行纠正等行为在训练过程中自然而然地出现。

\[10\] 理解 R1-Zero 类训练

26 Mar, Understanding R1-Zero-Like Training: A Critical Perspective, https://arxiv.org/abs/2503.20783

本文旨在探究 DeepSeek-R1-Zero 模型采用纯强化学习方法（pure RL）为何能够提升语言模型的推理能力。

作者发现，一些基础模型（如 Qwen2.5）在未经任何强化学习的情况下，便已经表现出较强的推理能力，甚至能够呈现出所谓的「顿悟时刻」（Aha moment）。因此，这种「顿悟」可能并非强化学习所诱发，而是源于预训练过程中的继承。这一发现对「深层推理行为是由强化学习单独引导形成」的观点提出了质疑。

此外，本文还揭示了 GRPO 方法中存在的两个偏差问题：

- 回答长度偏差（Response-length bias）：GRPO 在计算优势值（advantage）时对回答长度进行了归一化。这导致较长的错误答案所受到的惩罚变小，从而促使模型倾向于生成冗长但错误的回答。
- 题目难度偏差（Difficulty-level bias）：GRPO 同时依据每道题对应奖励的标准差进行归一化。这样一来，无论题目本身是简单还是困难，只要其对应的奖励方差较小，就容易在优化中被赋予较高权重。

为了解决上述问题，作者提出了一种改进的 GRPO 变体 ——Dr. GRPO。该方法在优势函数计算中取消了对回答长度的归一化处理，同时也不再在题目级别上对奖励标准差进行归一化。这样一来，训练过程变得更高效，同时也可以有效避免生成冗长但错误的答案。特别是在模型给出错误回答时，该方法不再鼓励其生成长篇幅的低质量文本。

\[11\] 在多样化领域中扩展基于可验证奖励的强化学习

31 Mar, Crossing the Reward Bridge: Expanding RL with Verifiable Rewards Across Diverse Domains, https://arxiv.org/abs/2503.23829

DeepSeek-R1 及后续多数推理模型主要关注易于验证领域（如编程和数学）的奖励信号。本文则探讨了如何将这些方法拓展至更复杂的领域，如医学、化学、心理学、经济学及教育学等 —— 这些领域的回答通常为自由形式，难以简单地用「正确 / 错误」二元标准进行判断。

研究发现，即便在上述复杂领域中，若采用专家撰写的参考答案，评估可行性仍超出预期。为构建奖励信号，本文提出了一种无需密集领域标注的「生成式软评分方法」（generative, soft-scoring method），从而显著降低对特定领域标注数据的依赖。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[12\] 在简化设定下扩展强化学习规模

31 Mar, Open-Reasoner-Zero: An Open Source Approach to Scaling Up Reinforcement Learning on the Base Model, https://arxiv.org/abs/2503.24290

在本文中，作者探索了一种用于语言模型推理任务训练的极简强化学习设置。他们采用了基础版本的概率策略优化算法（vanilla PPO），而非 DeepSeek-R1-Zero 中所使用的广义随机策略优化算法（GRPO），并省略了强化学习对人类反馈（RLHF）流程中常见的 Kullback-Leibler 正则化项（KL regularization）。

有趣的是，研究发现，该简化设置（即 vanilla PPO 训练器加上基于答案正确性的简单二元奖励函数）对于训练出在推理性能和生成长度两方面都有所提升的模型而言，已足够有效。

在使用与 DeepSeek-R1-Zero 相同的 Qwen-32B 基座模型的前提下，作者所构建的模型在多个推理基准任务上实现了超越后者的性能表现，同时训练步骤仅为其十分之一。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[13\] 重新审视预训练阶段中的反思机制

5 Apr, Rethinking Reflection in Pre-Training, https://arxiv.org/abs/2504.04022

基于 DeepSeek-R1 论文提出的重要发现 —— 即在基础模型上直接应用纯强化学习（pure RL）以激发推理能力 —— 我们曾推测大型语言模型的推理能力主要源自强化学习训练。然而，本论文给出了一个出人意料的转折：研究发现，自我纠正（self-correction）能力实际上在预训练（pre-training）阶段就已开始显现。

具体来说，作者通过在任务中引入人为设计的错误思维链，来衡量模型是否具备识别并修正这些错误的能力。实验结果显示，无论是显式反思（explicit reflection）还是隐式修正（implicit correction），这些能力都会在预训练过程中逐步自然涌现。这一现象在多种任务领域和不同模型规模中均有体现，甚至在预训练早期的模型检查点（checkpoint）上也可观察到初步的自我纠正迹象，且随着预训练计算量的增加，该能力持续增强。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[14\] 通过强化学习进行简洁推理

7 Apr, Concise Reasoning via Reinforcement Learning, https://arxiv.org/abs/2504.05185

众所周知，具备推理能力的语言模型通常会生成更长的输出文本，这无疑提高了计算成本。最新这篇论文指出，这种行为并非源于更长回答本身对于提高准确性有所帮助，而是在于强化学习训练过程中的内在偏向所致。

研究表明，在 RL 过程中，当智能体（Agent）因错误回答而获得负奖励时，策略优化算法 —— 特别是近端策略优化算法（PPO）—— 倾向于鼓励模型生成更长的回答。具体而言，PPO 的损失计算机制使得在负奖励的情形下，随着生成文本长度的增加，平均每个 token 的损失会逐渐变小。因此，即便模型依旧给出错误答案，但生成更长的回复形式会在数学上「稀释」每个 token 所承受的惩罚。

换句话说，长文本的结构掩盖了整体错误，从而在损失函数上表现为优化方向上的「改进」，即使这些额外 token 对实际推理结果没有帮助。于是模型「学会」了通过拉长输出长度来减轻惩罚，而非真正提升答案的正确性。

不过需要强调的是，这一现象仅在使用 PPO 的训练流程下被观察到： 「值得注意的是，当前的分析并不适用于 GRPO，对该类方法的严格分析将在未来展开。」

此外，研究者还发现，通过引入第二阶段的强化学习训练（即对部分可解答的问题进行少量 RL 微调），不仅可以缩短输出长度，而且有时还能维持甚至提升模型的准确率。这一发现对于模型部署的效率优化具有重要意义。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

\[15\] 冷静看待语言模型推理的进展

9 Apr, A Sober Look at Progress in Language Model Reasoning: Pitfalls and Paths to Reproducibility, https://arxiv.org/abs/2504.07086

本论文对近期关于强化学习可提升蒸馏语言模型（distilled language models）性能的主张进行了更为审慎的审视，尤其聚焦于基于 DeepSeek-R1 模型的研究。

例如，我曾讨论过 2024 年 3 月 20 日发布的《Reinforcement Learning for Reasoning in Small LLMs: What Works and What Doesn't》一文，其发现 RL 对蒸馏模型具有良好效果。此外，在 DeepSeek-R1 的相关论文中也指出，采用 RL 方法可以进一步显著提升这些蒸馏模型的性能。因此，该研究倾向于进一步探索相关机制，并在本文中仅展示通过简单的监督微调（SFT）训练得到的蒸馏模型结果。

然而，与早期研究报告的 RL 效果大幅提升结论不同，本论文指出，部分性能提升可能只是随机波动带来的假象。作者通过实验证明，在小型基准测试任务（如 AIME24）中，仅随机种子的改变就可能导致性能分数出现几个百分点的波动，说明结果存在极高的不稳定性。

当使用更为受控与标准化的实验设置来评估 RL 模型时，其性能提升通常显著小于原先报道，且多数情况下缺乏统计学显著性。尽管某些采用 RL 训练的模型确实在特定任务上表现出适度提升，但这些提升通常不如监督微调强效，且往往缺乏跨基准迁移泛化能力。

综上所述，尽管 RL 在某些情形下可能对小型蒸馏语言模型有所助益，本文主张其实际益处被过度渲染，研究界亟需更为严谨的评估标准，以厘清真正有效的手段与改进路径。

![image.png](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

© THE END

转载请联系本公众号获得授权

投稿或寻求报道：liyazhou@jiqizhixin.com

继续滑动看下一个

机器之心

向上滑动看下一个