---
source_type: web
title: "Multinode Training"
author:
  - 
  - "[[PyTorch Contributors]]"
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://docs.pytorch.org/tutorials/intermediate/ddp_series_multinode.html#multinode-training"
published: 2023-01-01
created: 2026-04-06
description: "PyTorch Documentation. Explore PyTorch, an open-source machine learning library that accelerates the path from research prototyping to production deployment."
tags:
  - 
  - "clippings"
---

[Introduction](https://docs.pytorch.org/tutorials/beginner/ddp_series_intro.html) || [What is DDP](https://docs.pytorch.org/tutorials/beginner/ddp_series_theory.html) || [Single-Node Multi-GPU Training](https://docs.pytorch.org/tutorials/beginner/ddp_series_multigpu.html) || [Fault Tolerance](https://docs.pytorch.org/tutorials/beginner/ddp_series_fault_tolerance.html) || **Multi-Node training** || [minGPT Training](https://docs.pytorch.org/tutorials/intermediate/ddp_series_minGPT.html)

## Multinode Training

Authors: [Suraj Subramanian](https://github.com/subramen)

What you will learn

Prerequisites

Follow along with the video below or on [youtube](https://www.youtube.com/watch/KaAJtI1T2x4).

![[Image 10.jpg]]

Multinode training involves deploying a training job across several machines. There are two ways to do this:

- running a `torchrun` command on each machine with identical rendezvous arguments, or
- deploying it on a compute cluster using a workload manager (like SLURM)

In this video we will go over the (minimal) code changes required to move from single-node multigpu to multinode training, and run our training script in both of the above ways.

Note that multinode training is bottlenecked by inter-node communication latencies. Running a training job on 4 GPUs on a single node will be faster than running it on 4 nodes with 1 GPU each.

## Local and Global ranks

In single-node settings, we were tracking the `gpu_id` of each device running our training process. `torchrun` tracks this value in an environment variable `LOCAL_RANK` which uniquely identifies each GPU-process on a node. For a unique identifier across all the nodes, `torchrun` provides another variable `RANK` which refers to the global rank of a process.

Warning

Do not use `RANK` for critical logic in your training job. When `torchrun` restarts processes after a failure or membership changes, there is no guarantee that the processes will hold the same `LOCAL_RANK` and `RANKS`.

## Heteregeneous Scaling

Torchrun supports *heteregenous scaling* i.e. each of your multinode machines can have different number of GPUs participating in the training job. In the video, I deployed the code on 2 machines where one machine has 4 GPUs and the other used only 2 GPUs.

## Troubleshooting

- Ensure that your nodes are able to communicate with each other over TCP.
- Set env variable `NCCL_DEBUG` to `INFO` (using `export NCCL_DEBUG=INFO`) to print verbose logs that can help diagnose the issue.
- Sometimes you might need to explicitly set the network interface for the distributed backend (`export NCCL_SOCKET_IFNAME=eth0`). Read more about this [here](https://pytorch.org/docs/stable/distributed.html#choosing-the-network-interface-to-use).