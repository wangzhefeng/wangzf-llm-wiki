---
source_type: web
title: "LoRA: Low-Rank Adaptation of Large Language Models"
author:
  - 
  - "[[Edward J. Hu]]"
  - "[[Yelong Shen]]"
  - "[[Phillip Wallis]]"
  - "[[Zeyuan Allen-Zhu]]"
  - "[[Yuanzhi Li]]"
  - "[[Shean Wang]]"
  - "[[Lu Wang]]"
  - "[[Weizhu Chen]]"
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://www.alphaxiv.org/overview/2106.09685v2"
published: 2021-10-17
created: 2026-04-06
description: "This paper introduces LoRA, a parameter-efficient method for adapting large language models to downstream tasks. LoRA significantly reduces the number of t"
tags:
  - 
  - "clippings"
---

## Introduction

Large language models (LLMs) like GPT-3 have demonstrated remarkable capabilities across diverse natural language processing tasks. However, adapting these massive models to specific downstream tasks through traditional fine-tuning presents significant challenges. Full fine-tuning requires updating all parameters, leading to prohibitive computational costs, enormous storage requirements, and complex deployment scenarios when serving multiple task-specific models.

![[img-0 1.jpeg|LoRA Architecture]] *Figure 1: LoRA architecture showing how low-rank matrices A and B are used to approximate weight updates while keeping the original pretrained weights W frozen.*

This paper introduces LoRA (Low-Rank Adaptation), a parameter-efficient fine-tuning method that addresses these limitations by constraining weight updates to a low-rank subspace. Rather than updating all model parameters, LoRA learns low-rank decomposition matrices that approximate the necessary weight changes, dramatically reducing the number of trainable parameters while maintaining competitive performance.

## Core Methodology

LoRA is based on the hypothesis that weight updates during adaptation have a low "intrinsic rank." For any pretrained weight matrix $W_0 \in \mathbb{R}^{d \times k}$, LoRA represents the weight update $\Delta W$ as a low-rank decomposition:

$$
W = W_0 + \Delta W = W_0 + BA
$$

where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with rank $r \ll \min(d,k)$.

During training, the original weights $W_0$ remain frozen, and only the much smaller matrices $A$ and $B$ are trained. The forward pass becomes:

$$
h = W_0x + \Delta Wx = W_0x + BAx
$$

The method includes several key design choices:

- Matrix $A$ is initialized with random Gaussian values while $B$ is initialized to zero, ensuring $\Delta W = 0$ at the start of training
- A scaling factor $\alpha/r$ is applied to $BAx$ to reduce hyperparameter sensitivity when varying rank $r$
- For Transformer models, LoRA is typically applied to attention weight matrices ($W_q$, $W_k$, $W_v$, $W_o$), with experiments focusing on query and value projections

A crucial advantage is that after training, the low-rank matrices can be merged with the original weights ($W = W_0 + BA$) for deployment, introducing zero additional inference latency compared to the original model.

## Experimental Results and Analysis

The authors evaluated LoRA across multiple model scales and tasks, demonstrating consistent effectiveness:

### Performance Across Model Scales

- **RoBERTa/DeBERTa on GLUE**: LoRA matches or exceeds full fine-tuning performance while using orders of magnitude fewer parameters (0.3M vs 125M for RoBERTa-base)
- **GPT-2 on generation tasks**: Competitive results on E2E NLG, WebNLG, and DART benchmarks
- **GPT-3 175B**: Most impressively, LoRA achieves comparable performance to full fine-tuning using only 4.7M trainable parameters (0.003% of the original model)

![[img-1 1.jpeg|Performance Comparison]] *Figure 2: LoRA performance on GPT-3 175B compared to other parameter-efficient methods across different parameter budgets on WikiSQL and MultiNLI tasks.*

### Efficiency Gains

The method delivers substantial practical benefits:

- **Parameter reduction**: Up to 10,000× fewer trainable parameters
- **Memory reduction**: 3× reduction in GPU memory during training by eliminating optimizer states for frozen parameters
- **Training speedup**: 25% faster training on GPT-3 175B
- **Storage efficiency**: Task-specific checkpoints are 10,000× smaller

### Understanding the Low-Rank Structure

The paper provides valuable insights into why LoRA works through detailed analysis of the learned weight updates:

![[img-2.jpeg|Singular Value Analysis]] *Figure 3: Analysis of singular vectors in LoRA weight updates, showing overlap between different rank configurations and comparison with random matrices.*

**Optimal rank selection**: Surprisingly small ranks ($r=1$ or $r=2$) often suffice, particularly when adapting both query and value projections simultaneously. This strongly supports the low intrinsic rank hypothesis.

**Subspace analysis**: The top singular directions learned by LoRA with small rank largely overlap with those learned at higher ranks, indicating that lower ranks capture the most meaningful adaptation directions.

**Relationship to pretrained weights**: The analysis reveals that $\Delta W$ doesn't simply amplify the top directions of the original weights $W_0$. Instead, LoRA appears to amplify task-specific directions that were latent but not emphasized in the pretrained model, with amplification factors reaching 20× for very low ranks.

## Deployment and Practical Considerations

LoRA's design enables efficient deployment scenarios that are particularly valuable for production systems:

- **Task switching**: Multiple task-specific LoRA modules can be stored alongside a single base model, enabling rapid switching between tasks by swapping small weight matrices
- **Batching efficiency**: The zero inference latency property allows seamless integration into existing serving infrastructure
- **Scalability**: Organizations can maintain hundreds of specialized models with minimal additional storage overhead

![[img-4 1.jpeg|Inference Latency]] *Figure 4: Inference latency comparison between different adaptation methods across various batch sizes and sequence lengths, showing LoRA maintains zero additional latency.*

## Theoretical Insights and Future Directions

The empirical analysis provides several theoretical insights that advance our understanding of adaptation in large language models:

The low-rank structure of weight updates suggests that the parameter space of effective adaptations is much smaller than the full parameter space, even for very large models. This finding has implications for future research into the geometry of neural network optimization and transfer learning.

The observation that LoRA amplifies task-specific directions orthogonal to the pretrained model's primary directions suggests a complementary relationship between general pretraining and task-specific adaptation, potentially informing future pretraining objectives.

## Significance and Impact

LoRA represents a significant advancement in making large language models practical for widespread deployment. By dramatically reducing the computational and storage barriers to adaptation while maintaining performance quality, it democratizes access to state-of-the-art language model capabilities.

The method's orthogonality to other techniques suggests potential for combination with approaches like prefix tuning or knowledge distillation. Its zero-latency property makes it particularly suitable for production environments where inference speed is critical.

Beyond its practical contributions, LoRA provides empirical evidence for fundamental questions about the nature of learning in overparameterized models, suggesting that effective adaptation occurs in low-dimensional subspaces even when full parameter spaces are available.

[Parameter-Efficient Transfer Learning for NLP](https://alphaxiv.org/abs/1902.00751)

This paper introduced adapter layers, a foundational parameter-efficient adaptation method that serves as a primary baseline and competitor to LoRA. The authors of LoRA frequently compare their method against adapters to highlight LoRA's key advantage of not introducing additional inference latency.

Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin de Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly. Parameter-Efficient Transfer Learning for NLP.arXiv:1902.00751 \[cs, stat\], June 2019. URLhttp://arxiv.org/abs/1902. 00751.

Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning

This work is cited as a direct inspiration for LoRA's core hypothesis. Its finding that pre-trained models have a low "intrinsic dimension" motivated the authors of LoRA to hypothesize that the weight updates during adaptation also have a low "intrinsic rank," providing the foundational concept for their method.

Armen Aghajanyan, Luke Zettlemoyer, and Sonal Gupta. Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning.arXiv:2012.13255 \[cs\], December 2020. URL http://arxiv.org/abs/2012.13255.

[Prefix-Tuning: Optimizing Continuous Prompts for Generation](https://alphaxiv.org/abs/2101.00190)

This paper introduced prefix-tuning, another prominent parameter-efficient adaptation technique against which LoRA is extensively benchmarked. The LoRA paper positions its method as an alternative that is easier to optimize and does not consume valuable input sequence length, making this a crucial point of comparison.

Xiang Lisa Li and Percy Liang. Prefix-Tuning: Optimizing Continuous Prompts for Generation. arXiv:2101.00190 \[cs\], January 2021. URLhttp://arxiv.org/abs/2101.00190.

[Language Models are Few-Shot Learners](https://alphaxiv.org/abs/2005.14165)

This paper introduced GPT-3, and the immense challenge of fine-tuning such a 175-billion-parameter model is the central motivation for LoRA. The prohibitive cost and hardware requirements of full fine-tuning for models of this scale are used to frame the necessity and benefits of a parameter-efficient approach like LoRA.

Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language Models are Few-Shot Learners.arXiv:2005.14165 \[cs\], July 2020. URLhttp://arxiv.org/abs/2005.14165.