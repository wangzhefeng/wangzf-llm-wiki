---
source_type: web
title: "Annotated Research Paper Implementations: Transformers, StyleGAN, Stable Diffusion, DDPM/DDIM, LayerNorm, Nucleus Sampling and more"
author: 
created_at: 2026-04-06
topics:
  - 大语言模型
status: inbox
source: "https://nn.labml.ai/"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

This is a collection of simple PyTorch implementations of neural networks and related algorithms. [These implementations](https://github.com/labmlai/annotated_deep_learning_paper_implementations) are documented with explanations, and the [website](https://nn.labml.ai/index.html) renders these as side-by-side formatted notes. We believe these would help you understand these algorithms better.

![[dqn-light.png|Screenshot]]

We are actively maintaining this repo and adding new implementations. for updates.

## Translations

### English (original)

### Chinese (translated)

### Japanese (translated)

## Paper Implementations

#### ✨ Transformers

- [JAX implementation](https://nn.labml.ai/transformers/jax_transformer/index.html)
- [Multi-headed attention](https://nn.labml.ai/transformers/mha.html)
- [Triton Flash Attention](https://nn.labml.ai/transformers/flash/index.html)
- [Transformer building blocks](https://nn.labml.ai/transformers/models.html)
- [Transformer XL](https://nn.labml.ai/transformers/xl/index.html)
- [Relative multi-headed attention](https://nn.labml.ai/transformers/xl/relative_mha.html)
- [Rotary Positional Embeddings (RoPE)](https://nn.labml.ai/transformers/rope/index.html)
- [Attention with Linear Biases (ALiBi)](https://nn.labml.ai/transformers/alibi/index.html)
- [RETRO](https://nn.labml.ai/transformers/retro/index.html)
- [Compressive Transformer](https://nn.labml.ai/transformers/compressive/index.html)
- [GPT Architecture](https://nn.labml.ai/transformers/gpt/index.html)
- [GLU Variants](https://nn.labml.ai/transformers/glu_variants/simple.html)
- [kNN-LM: Generalization through Memorization](https://nn.labml.ai/transformers/knn/index.html)
- [Feedback Transformer](https://nn.labml.ai/transformers/feedback/index.html)
- [Switch Transformer](https://nn.labml.ai/transformers/switch/index.html)
- [Fast Weights Transformer](https://nn.labml.ai/transformers/fast_weights/index.html)
- [FNet](https://nn.labml.ai/transformers/fnet/index.html)
- [Attention Free Transformer](https://nn.labml.ai/transformers/aft/index.html)
- [Masked Language Model](https://nn.labml.ai/transformers/mlm/index.html)
- [MLP-Mixer: An all-MLP Architecture for Vision](https://nn.labml.ai/transformers/mlp_mixer/index.html)
- [Pay Attention to MLPs (gMLP)](https://nn.labml.ai/transformers/gmlp/index.html)
- [Vision Transformer (ViT)](https://nn.labml.ai/transformers/vit/index.html)
- [Primer EZ](https://nn.labml.ai/transformers/primer_ez/index.html)
- [Hourglass](https://nn.labml.ai/transformers/hour_glass/index.html)

#### ✨ Low-Rank Adaptation (LoRA)

#### ✨ Eleuther GPT-NeoX

- [Generate on a 48GB GPU](https://nn.labml.ai/neox/samples/generate.html)
- [Finetune on two 48GB GPUs](https://nn.labml.ai/neox/samples/finetune.html)
- [LLM.int8()](https://nn.labml.ai/neox/utils/llm_int8.html)

#### ✨ Diffusion models

- [Denoising Diffusion Probabilistic Models (DDPM)](https://nn.labml.ai/diffusion/ddpm/index.html)
- [Denoising Diffusion Implicit Models (DDIM)](https://nn.labml.ai/diffusion/stable_diffusion/sampler/ddim.html)
- [Latent Diffusion Models](https://nn.labml.ai/diffusion/stable_diffusion/latent_diffusion.html)
- [Stable Diffusion](https://nn.labml.ai/diffusion/stable_diffusion/index.html)

#### ✨ Generative Adversarial Networks

- [Original GAN](https://nn.labml.ai/gan/original/index.html)
- [GAN with deep convolutional network](https://nn.labml.ai/gan/dcgan/index.html)
- [Cycle GAN](https://nn.labml.ai/gan/cycle_gan/index.html)
- [Wasserstein GAN](https://nn.labml.ai/gan/wasserstein/index.html)
- [Wasserstein GAN with Gradient Penalty](https://nn.labml.ai/gan/wasserstein/gradient_penalty/index.html)
- [StyleGAN 2](https://nn.labml.ai/gan/stylegan/index.html)

#### ✨ Recurrent Highway Networks

#### ✨ LSTM

#### ✨ HyperNetworks - HyperLSTM

#### ✨ ResNet

#### ✨ ConvMixer

#### ✨ Capsule Networks

#### ✨ U-Net

#### ✨ Sketch RNN

#### ✨ Graph Neural Networks

- [Graph Attention Networks (GAT)](https://nn.labml.ai/graphs/gat/index.html)
- [Graph Attention Networks v2 (GATv2)](https://nn.labml.ai/graphs/gatv2/index.html)

#### ✨ Reinforcement Learning

- [Proximal Policy Optimization](https://nn.labml.ai/rl/ppo/index.html) with [Generalized Advantage Estimation](https://nn.labml.ai/rl/ppo/gae.html)
- [Deep Q Networks](https://nn.labml.ai/rl/dqn/index.html) with with [Dueling Network](https://nn.labml.ai/rl/dqn/model.html), [Prioritized Replay](https://nn.labml.ai/rl/dqn/replay_buffer.html) and Double Q Network.

#### ✨ Counterfactual Regret Minimization (CFR)

Solving games with incomplete information such as poker with CFR.

- [Kuhn Poker](https://nn.labml.ai/cfr/kuhn/index.html)

#### ✨ Optimizers

- [Adam](https://nn.labml.ai/optimizers/adam.html)
- [AMSGrad](https://nn.labml.ai/optimizers/amsgrad.html)
- [Adam Optimizer with warmup](https://nn.labml.ai/optimizers/adam_warmup.html)
- [Noam Optimizer](https://nn.labml.ai/optimizers/noam.html)
- [Rectified Adam Optimizer](https://nn.labml.ai/optimizers/radam.html)
- [AdaBelief Optimizer](https://nn.labml.ai/optimizers/ada_belief.html)
- [Sophia-G Optimizer](https://nn.labml.ai/optimizers/sophia.html)

#### ✨ Normalization Layers

#### ✨ Distillation

#### ✨ Adaptive Computation

- [PonderNet](https://nn.labml.ai/adaptive_computation/ponder_net/index.html)

#### ✨ Uncertainty

- [Evidential Deep Learning to Quantify Classification Uncertainty](https://nn.labml.ai/uncertainty/evidence/index.html)

#### ✨ Activations

- [Fuzzy Tiling Activations](https://nn.labml.ai/activations/fta/index.html)

#### ✨ Language Model Sampling Techniques

#### ✨ Scalable Training/Inference

- [Zero3 memory optimizations](https://nn.labml.ai/scaling/zero3/index.html)

### Installation

```bash
pip install labml-nn
```