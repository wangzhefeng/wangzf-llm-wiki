---
source_type: web
title: "Training “real-world” models with DDP"
author:
  - 
  - "[[PyTorch Contributors]]"
created_at: 2026-04-06
topics:
  - 强化学习
status: inbox
source: "https://docs.pytorch.org/tutorials/intermediate/ddp_series_minGPT.html"
published: 2023-01-01
created: 2026-04-06
description: "PyTorch Documentation. Explore PyTorch, an open-source machine learning library that accelerates the path from research prototyping to production deployment."
tags:
  - 
  - "clippings"
---

[Introduction](https://docs.pytorch.org/tutorials/beginner/ddp_series_intro.html) || [What is DDP](https://docs.pytorch.org/tutorials/beginner/ddp_series_theory.html) || [Single-Node Multi-GPU Training](https://docs.pytorch.org/tutorials/beginner/ddp_series_multigpu.html) || [Fault Tolerance](https://docs.pytorch.org/tutorials/beginner/ddp_series_fault_tolerance.html) || [Multi-Node training](https://docs.pytorch.org/tutorials/intermediate/ddp_series_multinode.html) || **minGPT Training**

## Training “real-world” models with DDP

Authors: [Suraj Subramanian](https://github.com/subramen)

What you will learn

Prerequisites

Follow along with the video below or on [youtube](https://www.youtube.com/watch/XFsFDGKZHh4).

![[assets/attachments/pytorch/ddp-mingpt-training.jpg]]

In this video, we will review the process of training a GPT model in multinode DDP. We first clone the [minGPT repo](https://github.com/karpathy/minGPT) and refactor the Trainer to resemble the structure we have used in this series. Watch the video for details on these changes.

We use [hydra](https://hydra.cc/) to centrally manage all the configurations for our training run. Once the code has been refactored, we run it first on a single-node with 4 GPUs, and then on a slurm cluster.

## Files used for training

- [trainer.py](https://github.com/pytorch/examples/blob/main/distributed/minGPT-ddp/mingpt/trainer.py) includes the Trainer class that runs the distributed training iterations on the model with the provided dataset.
- [model.py](https://github.com/pytorch/examples/blob/main/distributed/minGPT-ddp/mingpt/model.py) defines the model architecture.
- [char\_dataset.py](https://github.com/pytorch/examples/blob/main/distributed/minGPT-ddp/mingpt/char_dataset.py) contains the `Dataset` class for a character-level dataset.
- [gpt2\_train\_cfg.yaml](https://github.com/pytorch/examples/blob/main/distributed/minGPT-ddp/mingpt/gpt2_train_cfg.yaml) contains the configurations for data, model, optimizer, and training run.
- [main.py](https://github.com/pytorch/examples/blob/main/distributed/minGPT-ddp/mingpt/main.py) is the entry point to the training job. It sets up the DDP process group, reads all the configurations and runs the training job.

## Using Mixed Precision

To speed things up, you might be able to use [Mixed Precision](https://pytorch.org/docs/stable/amp.html) to train your models. In Mixed Precision, some parts of the training process are carried out in reduced precision, while other steps that are more sensitive to precision drops are maintained in FP32 precision.

## When is DDP not enough?

A typical training run’s memory footprint consists of model weights, activations, gradients, the input batch, and the optimizer state. Since DDP replicates the model on each GPU, it only works when GPUs have sufficient capacity to accomodate the full footprint. When models grow larger, more aggressive techniques might be useful:

- [Activation checkpointing](https://pytorch.org/docs/stable/checkpoint.html): Instead of saving intermediate activations during the forward pass, the activations are recomputed during the backward pass. In this approach, we run more compute but save on memory footprint.
- [Fully-Sharded Data Parallel](https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html): Here the model is not replicated but “sharded” across all the GPUs, and computation is overlapped with communication in the forward and backward passes. Read our [blog](https://medium.com/pytorch/training-a-1-trillion-parameter-model-with-pytorch-fully-sharded-data-parallel-on-aws-3ac13aa96cff) to learn how we trained a 1 Trillion parameter model with FSDP.
