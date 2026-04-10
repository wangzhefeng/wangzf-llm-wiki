---
source_type: web
title: "DeepSeek 背后的数学原理：深入探究群体相对策略优化 (GRPO)"
author:
  - 
  - "[[致Great]]"
created_at: 2026-04-06
topics:
  - 强化学习
status: inbox
source: "https://mp.weixin.qq.com/s/Z-wRuqsQTF_6TeV7ao_9Yw"
published: 
created: 2026-04-06
description: "DeepSeek 背后的数学原理：深入探究群体相对策略优化 (GRPO)"
tags:
  - 
  - "clippings"
---

致Great *2025年2月11日 18:07*

> 原文译自：https://medium.com/@sahin.samia/the-math-behind-deepseek-a-deep-dive-into-group-relative-policy-optimization-grpo-8a75007491ba

## GRPO动机

### 什么是 GRPO？

群体相对策略优化 (**GRPO，Group Relative Policy Optimization)** 是一种强化学习 (RL) 算法，专门用于增强大型语言模型 (LLM) 中的推理能力。与严重依赖外部评估模型（价值函数）指导学习的传统 RL 方法不同，GRPO 通过评估彼此相关的响应组来优化模型。这种方法可以提高训练效率，使 GRPO 成为需要复杂问题解决和长链思维的推理任务的理想选择。

> **GRPO 的本质思路：通过在同一个问题上生成多条回答，把它们彼此之间做“相对比较”，来代替传统 PPO 中的“价值模型”**

### 为什么选择 GRPO？

近端策略优化 (PPO) 等传统 RL 方法在应用于 LLM 中的推理任务时面临着重大挑战：

**对价值模型（** Critic Model **）的依赖：**

- PPO 需要单独的价值模型来估计每个响应的值，这会使内存和计算要求加倍。
- 训练价值模型很复杂，而且容易出错，尤其是对于具有主观或细微评价的任务。

**计算成本高：**

- RL 管道通常需要大量计算资源来迭代评估和优化响应。
- 将这些方法扩展到大型 LLM 会加剧这些成本。

**可扩展性问题：**

- 绝对奖励评估难以适应各种任务，因此很难在推理领域中进行推广。

### GRPO 如何应对这些挑战：

- **无价值模型优化** ：GRPO 通过比较组内的响应消除了对评论模型的需求，从而显著减少了计算开销。
- **相对评估** ：GRPO 不依赖外部评估者，而是使用群体动力学来评估某个响应相对于同一批次中其他响应的表现如何。
- **高效训练** ：通过关注基于群体的优势，GRPO 简化了奖励估计过程，使其更快、更适用于大型模型。

> 图片来自：DeepSeekMath,https://arxiv.org/pdf/2402.03300

## 了解 GRPO 目标函数

群体相对策略优化 (GRPO) 中的目标函数定义了模型如何学习改进其策略，从而提高其生成高质量响应的能力。让我们一步一步地分解它。

### GRPO 目标函数

我们可以一步步解析 GRPO (Group Relative Policy Optimization) 目标函数，以理解它如何指导模型学习改进策略，从而提高生成高质量响应的能力。

GRPO 目标函数如下： ![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这个函数主要由三部分组成：

1. \*\*重要性采样比 (Policy Ratio)\*\*：衡量新旧策略之间的变化。
2. \*\*裁剪的目标函数 (Clipped Objective)\*\*：限制策略更新幅度，以避免剧烈变化导致模型崩溃。
3. \*\*KL 散度正则项 (KL Divergence Regularization)\*\*：确保新策略不会偏离参考策略太远，以保持稳定性。

### 细分关键组件

GRPO 目标函数如下：

该目标函数主要由三部分组成：

1. \*\*策略比值 (Policy Ratio)\*\*：衡量新旧策略的变化幅度。
2. \*\*裁剪目标 (Clipped Objective)\*\*：防止策略更新过大，确保稳定性。
3. \*\*KL 散度正则化 (KL Divergence Regularization)\*\*：防止新策略偏离参考策略过远。

#### (1) 期望值计算 (Expected Value)

- ：对所有输入查询进行期望计算，查询来自训练数据分布。
- ：对于每个查询，从旧策略采样个候选响应。

GRPO 目标函数对多个候选响应进行优化，使训练过程更加稳定。

#### (2) 策略比值 (Policy Ratio)

- 该比值衡量新策略生成的概率相较于旧策略的变化。
- 如果比值远离，说明策略更新过大，可能导致不稳定。

---

#### (3) 裁剪目标 (Clipped Objective)

- 该机制源自 PPO（Proximal Policy Optimization）。
- 通过限制策略变动范围，防止剧烈变化导致模型崩溃。
- 这样可以确保新策略逐步改进，而不是进行激进的更新。

---

#### (4) 优势估计 (Advantage Estimate)

- 衡量在同一组候选响应中的相对质量。
- 计算方式：

- ：对响应计算的奖励。
- ：该组响应的平均奖励。
- ：该组奖励的标准差。

这种 **归一化优势估计** 可以减少奖励尺度的影响，提高训练稳定性。

#### (5) KL 散度正则项 (KL Divergence Regularization)

- 这里的 KL 散度计算新策略与参考策略之间的距离。
- 控制 KL 正则项的影响力度。
- 这有助于防止模型过度更新，保持策略的平稳过渡。

## 通过例子理解 GRPO 目标函数

GRPO（群体相对策略优化）目标函数就像一个配方，通过比较模型自身的响应并逐步改进，让模型能够更好地生成答案。让我们将其分解成一个易于理解的解释：

### 目标

想象一下，你正在教一群学生解决一道数学题。你不会直接告诉他们谁答对了谁答错了，而是比较所有学生的答案，找出谁答得最好（以及原因）。然后，你通过奖励更好的方法和改进较弱的方法来帮助学生学习。这正是 GRPO 所做的——只不过它教的是 AI 模型，而不是学生。

### 详细步骤

### 步骤 1：从查询开始

从训练数据集 P(Q) 中选择一个查询 (q)

> 示例：假设查询是“8 + 5 的总和是多少？”

### 步骤 2：生成一组响应

该模型针对该查询生成一组 GGG 响应。

> 示例：该模型生成以下响应：o1：“答案是13。” o2：“十三。” o3：“是12。” o4：“总数是 13。”

### 步骤 3：计算每个响应的奖励

什么是奖励？：

> 奖励通过量化模型的响应质量来指导模型的学习。

GRPO 中的奖励类型：

- 准确性奖励：基于响应的正确性（例如，解决数学问题）。
- 格式奖励：确保响应符合结构指南（例如， 标签中包含的推理）。
- 语言一致性奖励：惩罚语言混合或不连贯的格式。

根据每个回复的优劣程度为其分配奖励 (ri) 。例如，奖励可能取决于：

- 准确性：答案正确吗？
- 格式：回复是否结构良好？

> 例如：r1=1.0（正确且格式良好）。r2=0.9（正确但不太正式）。r3=0.0（错误答案）。r4=1.0（正确且格式良好）。

### 步骤 4：比较答案（团体优势）

计算每个响应相对于该组的优势 (Ai) ：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) 简单来说你可以这样理解

- 回答优于小组平均水平的，将获得正分，而回答较差的，将获得负分。
- 鼓励群体内部竞争，推动模型产生更好的反应。

### 步骤 5：使用裁剪更新策略

- 调整模型（）以偏好具有较高优势值（）的响应，同时避免大幅度的不稳定更新：

- 如果新策略与旧策略的比率超出范围，则会被裁剪以防止过度修正。

### 步骤 6：使用 KL 散度惩罚偏差

- 添加一个惩罚项 以确保更新后的策略不会偏离参考策略太远。
	**示例** ：如果模型开始生成格式差异极大的输出，KL 散度项会对其进行抑制。

## GRPO实现

> 来源:GRPO Trainer,https://huggingface.co/docs/trl/main/en/grpo\_trainer

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) 为了方便后人使用GRPO进行开发，DeepSeek团队开源了GRPO方法，并为此开发了名为 **GRPOTrainer** 的方法（囊括于trl包中），目前GRPO Trainer仍在积极开发当中。其导入方法如下：

```
from trl import GRPOTrainer
```

GRPO Trainer会记录以下指标：

- completion\_length：平均完成时长。
- reward/{reward\_func\_name}：每个 reward 函数计算的奖励。
- reward：平均奖励。
- reward\_std ：奖励组内的平均标准差。
- kl ：根据完成次数计算的模型和参考模型之间的平均 KL 散度。

GRPOTrainer支持使用自定义奖励函数，而不是密集的奖励模型。为确保兼容性，奖励函数必须满足以下要求：

**1\. 输入参数**

- 该函数必须接受以下内容作为关键字参数：

- prompts（包含提示）
- completions（包含生成的 completions）
- 数据集可能具有的所有列名称（但prompt）。例如，如果数据集包含名为 ground\_truth 的列，则将使用 ground\_truth 作为关键字参数来调用该函数。

- 符合此要求的最简单方法是在函数签名中使用 \*\*kwargs。
- 根据数据集格式，输入会有所不同：

- 对于 `标准格式` ，prompts 和 completions 将是字符串列表。
- 对于 `对话格式` ，prompts 和 completions 将是消息词典的列表。

**2\. 返回值** ：该函数必须返回浮点数列表。每个浮点数代表与单个完成对应的奖励。

官方给出了一下几个使用示例：

示例 1：奖励较长的completions

以下是奖励较长完成度的标准格式的奖励函数示例：

```
def reward_func(completions, **kwargs):
    """奖励功能：输出的completions越长，得分越高。"""
    return [float(len(completion)) for completion in completions]
```

可以按如下方式对其进行测试：

```
prompts = ["The sky is", "The sun is"]
completions = [" blue.", " in the sky."]
print(reward_func(prompts=prompts, completions=completions))
[6.0, 12.0]
```

示例 2：具有特定格式的奖励完成

下面是一个奖励函数示例，该函数检查完成是否具有特定格式。此示例的灵感来自论文 DeepSeek-R1 中使用的格式奖励函数。它专为对话格式而设计，其中提示和完成由结构化消息组成。

```
import re
 
def format_reward_func(completions, **kwargs):
    """奖励函数：检查完成是否具有特定格式"""
    pattern = r"^<think>.*?</think><answer>.*?</answer>$"
    completion_contents = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, content) for content in completion_contents]
    return [1.0 if match else 0.0 for match in matches]
```

可以按如下方式测试此函数：

```
prompts = [
    [{"role": "assistant", "content": "What is the result of (1 + 2) * 4?"}],
    [{"role": "assistant", "content": "What is the result of (3 + 1) * 2?"}],
]
completions = [
    [{"role": "assistant", "content": "<think>The sum of 1 and 2 is 3, which we multiply by 4 to get 12.</think><answer>(1 + 2) * 4 = 12</answer>"}],
    [{"role": "assistant", "content": "The sum of 3 and 1 is 4, which we multiply by 2 to get 8. So (3 + 1) * 2 = 8."}],
]
format_reward_func(prompts=prompts, completions=completions)
[1.0, 0.0]
```

示例 3：基于引用的奖励完成

下面是一个 reward 函数的示例，用于检查 the 是否正确。这个例子的灵感来自论文 DeepSeek-R1 中使用的准确率奖励函数。此示例专为标准格式设计，其中数据集包含名为 ground\_truth 的列。

```
import re
 
def reward_func(completions, ground_truth, **kwargs):
    # Regular expression to capture content inside \boxed{}
    matches = [re.search(r"\\boxed\{(.*?)\}", completion) for completion in completions]
    contents = [match.group(1) if match else "" for match in matches]
    # Reward 1 if the content is the same as the ground truth, 0 otherwise
    return [1.0 if c == gt else 0.0 for c, gt in zip(contents, ground_truth)]
```

可以按如下方式测试此函数：

```
prompts = ["Problem: Solve the equation $2x + 3 = 7$. Solution:", "Problem: Solve the equation $3x - 5 = 10$."]
completions = [r" The solution is \boxed{2}.", r" The solution is \boxed{6}."]
ground_truth = ["2", "5"]
reward_func(prompts=prompts, completions=completions, ground_truth=ground_truth)
[1.0, 0.0]
```

将 reward 函数传递给 trainer

要使用自定义奖励函数，请将其传递给 GRPOTrainer，如下所示：

```
from trl import GRPOTrainer
 
trainer = GRPOTrainer(
    reward_funcs=reward_func, # 自定义奖励函数reward_func
    ...,
)
```

如果有多个奖励函数，则可以将它们作为列表传递：

```
from trl import GRPOTrainer
 
trainer = GRPOTrainer(
    reward_funcs=[reward_func1, reward_func2], # 将奖励函数写为列表形式
    ...,
)
```

## GRPO总结

GRPO 目标的工作原理如下：

- 为查询生成一组响应。
- 根据预定义的标准（例如准确性、格式）计算每个响应的奖励。
- 比较组内的反应以计算他们的相对优势（AiA\_iAi）。
- 更新策略以支持具有更高优势的响应，确保剪辑的稳定性。
- 规范更新以防止模型偏离基线太远。

> 图片来源：https://huggingface.co/docs/trl/main/en/grpo\_trainer

### 为什么 GRPO 有效

- 无需批评：GRPO 依靠群体比较避免了对单独评估者的需求，从而降低了计算成本。
- 稳定学习：剪辑和 KL 正则化确保模型稳步改进，不会出现剧烈波动。
- 高效训练：通过关注相对性能，GRPO 非常适合推理等绝对评分困难的任务。

### 现实生活中的类比

想象一下一群学生在解决一个问题。老师不再单独给每个学生打分，而是让学生自己比较答案。 **答案更好的学生会受到鼓励，而其他人则会从错误中吸取教训。随着时间的推移，整个团队会共同进步，变得更加准确和一致。GRPO 应用这一原则来训练 AI 模型，使它们能够有效、高效地学习。**

### GRPO效果：DeepSeek R1上的成功

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) GRPO 通过实现高效且可扩展的推理任务训练，推动了 DeepSeek 的卓越性能。以下是它如何转化为成功：

- **增强推理能力** ：GRPO 让DeepSeek-R1-Zero在 AIME 2024 上取得了71.0% 的 Pass@1 分数，通过多数投票后分数上升至86.7%。它在解决数学和逻辑问题方面可与 OpenAI 等专有模型相媲美。
- **顿悟时刻** ：通过 GRPO，DeepSeek 模型开发了高级推理行为，例如自我验证、反思和长链思维，这对于解决复杂任务至关重要。
- **可扩展性** ：GRPO 的基于组的优化消除了对评论模型的需求，从而减少了计算开销并实现了大规模训练。
- **提炼成功** ：从 GRPO 训练的检查点提炼出的较小模型保留了较高的推理能力，使 AI 更易于访问且更具成本效益。

通过关注群体内的相对表现，GRPO 使 DeepSeek 能够在推理、长上下文理解和一般 AI 任务中设定新的基准，同时保持效率和可扩展性

## 参考资料

- **聊聊GRPO算法——从Open R1来看如何训练DeepSeek R1模型**
- **The Math Behind DeepSeek: A Deep Dive into Group Relative Policy Optimization (GRPO)**
- **GRPO Trainer（深入了解GRPO）**
- **GRPO Trainer**

添加微信，回复”LLM“进入交流群

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

作者提示: 素材来源官方媒体/网络新闻

继续滑动看下一个

ChallengeHub

向上滑动看下一个