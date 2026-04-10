---
source_type: web
title: "Training a 1 Trillion Parameter Model With PyTorch Fully Sharded Data Parallel on AWS"
author:
  - 
  - "[[PyTorch]]"
created_at: 2026-04-06
topics:
  - 深度学习
status: inbox
source: "https://medium.com/pytorch/training-a-1-trillion-parameter-model-with-pytorch-fully-sharded-data-parallel-on-aws-3ac13aa96cff"
published: 2022-03-16
created: 2026-04-06
description: "Training a 1 Trillion Parameter Model With PyTorch Fully Sharded Data Parallel on AWS Authors: Pavel Belevich (Meta AI), Yanli Zhao (Meta AI), Shen Li (Meta AI), Jessica Choi (Meta AI), Rohan Varma …"
tags:
  - 
  - "clippings"
---

[Sitemap](https://medium.com/sitemap/sitemap.xml)

Get unlimited access to the best of Medium for less than $1/week.[Become a member](https://medium.com/plans?source=upgrade_membership---post_top_nav_upsell-----------------------------------------)

[

Become a member

](https://medium.com/plans?source=upgrade_membership---post_top_nav_upsell-----------------------------------------)

## [PyTorch](https://medium.com/pytorch?source=post_page---publication_nav-512b8efdf2e7-3ac13aa96cff---------------------------------------)

[![PyTorch](https://miro.medium.com/v2/resize:fill:76:76/1*z0grEcFmF5wUdY8JGVOmiw.png)](https://medium.com/pytorch?source=post_page---post_publication_sidebar-512b8efdf2e7-3ac13aa96cff---------------------------------------)

An open source machine learning framework that accelerates the path from research prototyping to production deployment

Authors: Pavel Belevich (Meta AI), Yanli Zhao (Meta AI), Shen Li (Meta AI), Jessica Choi (Meta AI), Rohan Varma (Meta AI), Pritam Damania (Meta AI), Geeta Chauhan (Meta AI), Mahesh Yadav (Meta AI), Pierre-Yves Aquilanti (Amazon AWS), Sundar Ranganathan (Amazon AWS)

We demonstrate the feasibility of training 175B- and 1T-parameter models using FullyShardedDataParallel (FSDP) on AWS. Based on our experiments, we provide guidelines on configuring FSDP and cloud GPU clusters to maximize throughput and minimize cost.

## Introduction

Numerous studies ¹ ² ³ ⁴ ⁵ ⁶ have shown that the accuracy of deep learning models improves smoothly with increasing model size, dataset size and amount of compute used for training. During the last 3 years, model size grew 10,000 times from [BERT](https://arxiv.org/abs/1810.04805) ⁴ with 110M parameters to [Megatron-2](https://arxiv.org/abs/2104.04473) ⁷ with one trillion (Fig. 1). ==Even with the most advanced compute hardware, training models with 10B+ parameters require multiple GPUs, and training models with 100B+ parameters require several multi-GPU nodes.== Although training large models is a hot topic in the deep learning community, it is still largely unaffordable for most researchers and companies.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*jadWR1gSlevnD-Cy)

Figure 1: Trend of sizes of state-of-the-art NLP models with time

To make large model training accessible to all PyTorch users, we focused on developing a scalable architecture with key PyTorch libraries and AWS services to showcase large model training. We leveraged [FullyShardedDataParallel](https://pytorch.org/blog/introducing-pytorch-fully-sharded-data-parallel-api/) (FSDP), a recent prototype API added to [PyTorch Distributed](https://pytorch.org/docs/stable/distributed.html) which enables the training of models orders of magnitude larger than is feasible with non-sharded data parallel methods, in a more efficient manner and using fewer GPUs. This architecture is not limited to language models.

The [original FairScale FSDP](https://engineering.fb.com/2021/07/15/open-source/fsdp/) ⁸ implementation showed great results for training a 13B-parameter model on 8 GPUs. We expanded this experimentation to 175B-parameters, and up to 1T-parameters using the PyTorch FSDP implementation.

This note presents our experiment design and results for training large models on AWS, achieving 159 teraFLOP/s per GPU for a 175B model and 84 teraFLOP/s per GPU for a 1T model on [NVIDIA A100-SXM4–40GB](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf) ⁹ GPUs. Linear scaling efficiency is observed when the number of GPUs is increased from 8 GPUs to 512 GPUs.

We would like to emphasize that our goal was not to train the network till convergence, but to measure performance and scalability and give practical advice on how to use it for training large models.

## About FSDP

FSDP is a type of data-parallel training which, unlike traditional data-parallel processing, shards the model’s parameters, gradients and optimizer states across data-parallel workers and can optionally offload the sharded model parameters to the CPUs. Please see more details about [PyTorch FSDP in this doc](https://pytorch.org/blog/introducing-pytorch-fully-sharded-data-parallel-api/).

## Experiment Setup

We used [AWS ParallelCluster](https://aws.amazon.com/hpc/parallelcluster/) ¹⁰ 3.1.0 to provision automatically an HPC system (Fig. 2) with 64 [p4d.24xlarge](https://aws.amazon.com/ec2/instance-types/p4/) instances for a total of 512 NVIDIA A100-SXM4–40GB GPUs and used a shared parallel file-system of 4.8TiB using [Amazon FSx for Lustre](https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html).

The p4d.24xlarge¹¹ instances were all placed in the same [Amazon EC2 UltraCluster](https://pages.awscloud.com/amazon-ec2-p4d.html) and used a [placement group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html) to optimize their physical placement in the [Availability Zone](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html). Each instance has 4 [Elastic Fabric Adapter](https://aws.amazon.com/hpc/efa/) ¹² (EFA) network interfaces.

[EFA](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html) uses the [scalable reliable datagram](https://www.amazon.science/publications/a-cloud-optimized-transport-protocol-for-elastic-and-scalable-hpc) (SRD) protocol, designed by AWS. It offers lower and more consistent latency and higher throughput than the TCP transport, which benefits to high-performance computing (HPC) applications and distributed machine learning (ML) workloads ¹³.

For storage, we used a volume shared by NFS based on an Amazon EBS GP3 volume of 200GiB for **/** *apps* and a Lustre file-system of 4.8 TiB mounted on **/** *scratch* providing 960MiB/s of throughput.

On the software side, we used the default configuration provided with our cluster, such as CUDA 11.4, the NVIDIA Driver 470 and the EFA plugin for NCCL used for PyTorch FSDP collective communications. We installed PyTorch 1.10 to run our experiments and used the [Slurm](https://slurm.schedmd.com/) Workload Manager to serve as a distributed job scheduler. It’s a well-known and popular tool among machine learners who work on distributed training.

The cluster configuration of our cluster is set through a YAML template that ParallelCluster uses to create the requested resources in the AWS Cloud. The cluster properties can be customized to the workload requirements, such as the file-system size, throughput or the number and types of instances.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*Rxe3rlXiijc3YbFu)

Figure 2: Cluster architecture

## Models

We chose two variants of GPT architecture for our experiments. The famous GPT-3 ⁶ with 175B parameters and a 1T-parameters model with hyper-parameters introduced in the Megatron-2 paper⁷. Both models use a vocabulary size *V* of 50k. All experiments were run with fp16, including SGD optimizer. The models were implemented based on [minGPT](https://github.com/karpathy/minGPT) ¹⁴. For end-to-end time/cost estimation, we assumed the model would converge after consuming 300B tokens as mentioned in the GPT-3 paper.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8SnGN8iAhrbpD-MyNFiiFA.png)

## Experiment Design and Optimizations

Our experiments were optimized for teraFLOP/s per GPU. To train a 1T model with a large batch size with a smaller number of GPUs, we took advantage of CPU memory and applied different kinds of memory-saving techniques, like FSDP, CPU offloading and activation of checkpointing. Combining these memory-saving techniques allowed the 1T model to be trained with just 32 GPUs.

Specifically, the decoder’s linear layers were wrapped using FSDP, checkpointing inner activations of each decoder layer. During computation, only the shards of linear layers in a single FSDP instance were loaded into GPUs, while the shards of other layers in other FSDP instances were offloaded into CPU memory. To further increase batch size, we also offloaded outer activations of transformer layers to CPUs.

In addition to applying these memory-saving techniques, we also optimized communication and improved model initialization.

Figure 3 shows our overall experiment design.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*KoYStd4sCOBkGO1F)

Figure 3: Experiment design, H is the hidden dimension

## Model Initialization

At the beginning of our experiment, 1T model initialization time took 3 hours. It initialized the full modules on CPUs and then passed CPU modules to the FSDP constructor for modules to be flattened and sharded on CPUs.

We reduced the initialization time from 3 hours to less than 1 minute by initializing the to-be-wrapped layers on GPUs directly and then passing these layers to the FSDP constructor to be flattened and sharded on GPUs. After this, the sharded layers are offloaded to CPUs.

## Wrapping Decoder’s Linear Layers With FSDP

In order to minimize the transient GPU memory needs, users need to wrap a model in a nested fashion. FSDP will “all-gather” those layers on a single GPU. There is a natural limitation that the most nested layer wrapped with FSDP must fit on a single GPU, which means that users need to be aware of the size of network layers. The common transformer-based language model like GPT-3 is a sequence of an embedding layer followed by L encoders or decoders followed by some “head.” Usually, the embedding layer and the “head” have a size of V\*H and encoders or decoders have a size of roughly 12H², where V is the vocabulary size and H is a hidden dimension. Starting with GPT-3 13B, the size of each decoder exceeds the size of the embedding or the “head,” which means that at least 12\*H² parameters with gradients must fit into a single GPU. A GPT-3 model with H=12,288 contains almost 2B parameters per decoder and a 1T 128-layers GPT-like network with H=25,600 contains almost 8B parameters per decoder. Depending on the floating-point precision, it almost hits the modern high-end GPU capacity. So the “CUDA out of memory” error won’t be a surprise in this case. For the decoder (or encoder) layer, the weights are distributed among 6 linear layers: four H2 and two 4\*H². By wrapping those internal linear layers, we can fit 4\*H² into a single GPU. This enables a hidden size of 12,288 or even 25,600 without having to worry about the “CUDA out of memory” error.

## Parameters CPU Offloading

[Offloading](https://en.wikipedia.org/wiki/External_memory_algorithm) is the general technique of moving data to the CPU in order to free up GPU memory, which can result in training larger models and the ability to use a larger batch size with a smaller number of GPUs. Parameter and gradient offloading is one such technique in which parameters or parameter gradients that are currently not in use are offloaded to the CPU in order to free up GPU memory.

CPU offloading parameters are implemented as part of [PyTorch FSDP API](https://pytorch.org/docs/stable/fsdp.html), and non-blocking data transfer on separated streams is implemented to improve performance. Please see **Trace1** at the end of this note; it demonstrates that the data transfer between host and device is small in 1T experiments.

## Activation Checkpointing Decoder Layer

Since inner activations as shown in Fig. 3 are larger, the whole decoder layer is checkpointed, this means these inner activations are discarded during forward computation to save GPU memory. The inner activations are recomputed when the decoder layer backward pass is computed.

We’ve implemented a [checkpoint\_wrapper](https://github.com/pytorch/pytorch/blob/master/torch/distributed/algorithms/_checkpoint/checkpoint_wrapper.py) API in PyTorch Distributed to conveniently checkpoint a module.

## Activations CPU Offloading

To further save GPU memory, the outer activations of each decoder layer are also offloaded to CPU during forward pass and are loaded back to GPUs during backward pass. This increased the batch size to 4X (or 2.5X per-GPU teraFLOP/s throughput) compared to CPU offloading without activations for the 1T experiments.Activations CPU Offloading is implemented as part of checkpoint\_wrapperAPI using [saved\_on\_cpu](https://pytorch.org/tutorials/intermediate/autograd_saved_tensors_hooks_tutorial.html) hooks. Data transfer between host and device is non-blocking and is relatively small compared to other bottlenecks in 1T experiments, please see **Trace2** at the end of the note.

## Communication Optimization in PyTorch FSDP

We applied backward communication and computation overlapping by prefetching full parameters before backward computation starts in the current FSDP instance. This resulted in a 10% teraFLOP/s increase for the 175B experiments. But this technique did not help in the case of 1T experiments as the largest bottleneck in the 1T case was caused by memory allocation through [cudaMalloc](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY.html#group__CUDART__MEMORY_1g37d37965bfb4803b6d4e59ff26856356), not communication.

## NCCL Parameter Tuning

We’ve also tried to tune NCCL parameters like NCCL\_MIN\_NCHANNELS, NCCL\_NSOCKS\_PERTHREAD, NCCL\_SOCKET\_NTHREADS, NCCL\_BUFFSIZE, NCCL\_PROTO and NCCL\_ALGO. This did not help improve performance, indicating that the AWS cluster already tuned these parameters to be optimal.

## Experiment Results

## Metrics

We chose per-GPU throughput measured in [teraFLOP/s](https://en.wikipedia.org/wiki/FLOPS) as the main performance metric as this is a model-agnostic metric measuring the number of floating-point operations performed by second. It can be used as a proxy for comparing effectiveness of distributed training approaches and can be used to estimate the total training time and cost of training. For language models, we used the formulas from the Megatron-2 paper⁷. *F* is the number of FLOPs per iteration. Dividing *F* by iteration time gives per-GPU throughput:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*r0eHF-uPtypMBKGnqeX6Hg.png)

Where *B* is batch size, *s* is sequence length, *l* is the number of decoders, *h* is hidden size, *V* is vocabulary size, *T* is the number of tokens in the training dataset, *P* is the total number of parameters, *n* is the number of GPUs and *X* is per-GPU throughput.

## GPT-3 175B Experiments

In order to reach maximum GPU throughput, it’s required to maximize GPU memory utilization and consequently batch size. For a sequence length of 512, maximum memory allocation was observed with a batch size of 21 (Fig. 4). However, as the PyTorch CUDA caching allocator may affect performance near the GPU memory boundary, we expected the actual maximum throughput with a batch size less than 21.

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*Xh5JTc-Cx5vTNA8G)

Figure 4: Maximum GPU memory allocation vs batch size (175B)

As expected, maximum per-GPU throughput was achieved with a batch size of 20 on 128 GPUs (Fig. 5). A further increase in the number of GPUs leads to per-GPU throughput degradation because of increased communication between the nodes. **The maximum per-GPU throughput of 159 teraFLOP/s/GPU is 51% of the NVIDIA A100 peak theoretical performance 312 teraFLOP/s/GPU.**

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*gC43lRCx2TR5MLbV)

Figure 5: Per-GPU throughput vs number of GPUs (175B)

The aggregate throughput of the whole cluster grows non-linearly after 128 GPUs because of increased communication between the nodes (Fig. 7). We also observe how EFA drastically improves per-GPU (Fig. 6) and aggregated (Fig. 7) throughput.

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*TyrjoMb14x4lBjaV)

Figure 6: EFA and no-EFA per-GPU throughput vs number of GPUs (175B)

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*U1qrzitLar9IYv15)

Figure 7: Aggregate throughput vs number of GPUs (175B)

Using the formula for estimating end-to-end training time, we drew the curve to show how many days it would take to train GPT-175B using FSDP depending on the number of GPUs (Fig. 8).

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*QBl5MHO0fBNvfaEO)

Figure 8: Total training time for 300B tokens (175B)

Based on the number of GPUs and current AWS pricing, we extrapolated the cost to train GPT-3 175B on 300B tokens using PyTorch FSDP (Fig. 9).

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*Ejnt_HkyfGtXyvpD)

Figure 9: Total training time for 300B tokens (175B)

**Per our estimate, it would take 128 NVIDIA A100 40GB GPUs running for about 240 days to train GPT-3 175B using FSDP. According to current AWS public pricing, the strategy we would pick is to reserve 16 p4d.24xlarge instances for a duration of 1 year.**

## GPT-3 1T Experiments

For the GPT-3 1T model, the sequence length was increased to 2048 and maximum GPU memory utilization was reached with a batch size of 4 (Fig. 10).

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*RT6hkyvhgY3kk1dA)

Figure 10: Maximum GPU memory allocation vs batch size (1T)

The maximum per-GPU throughput of 84 teraFLOP/s/GPU was achieved with a batch size of 4 on 128 GPUs. However, a further increase in the number of GPUs doesn’t affect the per-GPU throughput significantly; even with 512 GPUs, we observed 81 teraFLOP/s/GPU (Fig. 11).

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*tcRuHcF3aecYBEja)

Figure 11: Per-GPU throughput vs number of GPUs (1T)

Almost constant per-GPU throughput means the whole system is linearly scalable with regards to the number of GPUs, at least up to 512 GPUs (Fig. 12). This indicates that the largest bottleneck is not the result of communication (see **Trace3** at the end of the note), but is caused by cudaMalloc when the peak GPU memory reaches the limit.

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*5jVSNgmAIzSt-dm3)

Figure 12: Aggregate throughput vs number of GPUs (1T)

Linear horizontal scalability implies that total training time decreases linearly with increasing number of GPUs (Fig. 13).

![](https://miro.medium.com/v2/resize:fit:1200/format:webp/0*nuYxUVwl2hdb57DU)

Figure 13: Total training time for 300B tokens (1T)

**Based on the total training time curve and current AWS pricing for 1 year and 3 years reservation, we suggest 2 possible strategies for training 1T GPT-like neural networks using PyTorch FSDP. Fast: 1-year training across 128 p4d.24xlarge instances, and Long: 3 years training across 43 p4d.24xlarge instances.**

## Future Plans

The traces of the 1T experiments indicate that there is still room to improve the training performance. We plan to continue running large model experiments on AWS and drive new feature developments in PyTorch Distributed in the future. Our tentative plans include:

1. Test with Adam optimizer, optimize it by fusing optimizers with nested FSDP instances.
2. Test distributed model checkpointing efficiency for 175B and 1T models.
3. Reduce memory fragmentation and improve the cudaMalloc performance, as it is the largest bottleneck in 1T experiments; see **Trace3** in the end of the note.
4. Improve communication efficiency such as collective performance and lossless compression, as communication is the second-largest bottleneck in 1T experiments; see **Trace4** in the end of the note.

**Trace1**: Small data transfer time between host and device for Parameters CPU Offloading in 1T experiments: 256 GPUs, sequence length 2048, batch size 4, one HtoD op: 8ms; one DtoH op: 3ms.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*xxU8vYdqEeUsVwdx)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*JGlpOEZyD3CjeHAA)

**Trace2**: Data transfer time between host and device for Activations CPU Offloading in 1T experiments: 256 GPUs, sequence length 2048, batch size 4, one DtoH op: 66ms; one HtoD op: 68ms.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*AQO0agaWWdW_J6Za)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*taU0ce6g1q20nOtu)

**Trace3**: slowMalloc in 1T experiments, which is the largest bottleneck observed: 256 GPUs, sequence length 2048, batch size 4, one cudaMalloc could take hundreds of ms.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*soeA4ZWathPWwbYQ)

**Trace4**: all\_gather and reduce\_scatter bubbles in 1T experiments, which is the second-largest bottleneck observed in the forward (above) and backward pass (below) traces: 256 GPUs, sequence length 2048, batch size 4. One collective op could take hundreds of ms.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*syaQImlwK3V5nM0Y)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*qG-8H7sc8CZXjij_)

## References

\[1\] Sanjeev Arora, Nadav Cohen and Elad Hazan. “On the Optimization of Deep Networks: Implicit Acceleration by Overparameterization.” arXiv preprint arXiv:1802.06509, 2018.

\[2\] Jonathan Frankle and Michael Carbin. “The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks.” arXiv preprint arXiv:1803.03635, 2018.

\[3\] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu and Dario Amodei. “Scaling Laws for Neural Language Models.” arXiv preprint arXiv:2001.08361, 2020.

\[4\] Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova. “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.” arXiv preprint arXiv:1810.04805, 2018.

\[5\] Dhruv Mahajan, Ross Girshick, Vignesh Ramanathan, Kaiming He, Manohar Paluri, Yixuan Li, Ashwin Bharambe and Laurens van der Maaten. “Exploring the Limits of Weakly Supervised Pretraining.” In Proceedings of the European Conference on Computer Vision (ECCV), pages 181–196, 2018.

\[6\] Tom B Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. “Language Models Are Few-Shot Learners.” arXiv preprint arXiv:2005.14165, 2020.

\[7\] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.” arXiv preprint arXiv:1810.04805, 2018.

\[8\] Narayanan, Deepak, Mohammad Shoeybi, Jared Casper, Patrick LeGresley, Mostofa Patwary, Vijay Anand Korthikanti, Dmitri Vainbrand et al. “Efficient Large-Scale Language Model Training on GPU Clusters.” arXiv preprint arXiv:2104.04473, 2021.

\[9\] Fully Sharded Data Parallel: faster AI training with fewer GPUs

https://engineering.fb.com/2021/07/15/open-source/fsdp/

\[10\] NVIDIA A100 Tensor Core GPU https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf

\[11\] Amazon EC2 P4d Instances https://aws.amazon.com/ec2/instance-types/p4/

\[12\] Elastic Fabric Adapter https://aws.amazon.com/hpc/efa/

\[13\] A cloud-optimized transport protocol for elastic and scalable HPC https://www.amazon.science/publications/a-cloud-optimized-transport-protocol-for-elastic-and-scalable-hpc

\[14\] AWS ParallelCluster https://aws.amazon.com/hpc/parallelcluster/

\[15\] minGPT https://github.com/karpathy/minGPT

[![PyTorch](https://miro.medium.com/v2/resize:fill:96:96/1*z0grEcFmF5wUdY8JGVOmiw.png)](https://medium.com/pytorch?source=post_page---post_publication_info--3ac13aa96cff---------------------------------------)

[![PyTorch](https://miro.medium.com/v2/resize:fill:128:128/1*z0grEcFmF5wUdY8JGVOmiw.png)](https://medium.com/pytorch?source=post_page---post_publication_info--3ac13aa96cff---------------------------------------)

[Last published Feb 14, 2024](https://medium.com/pytorch/exploring-scientific-machine-learning-pipelines-through-the-simulai-toolkit-9fda42d6c6a0?source=post_page---post_publication_info--3ac13aa96cff---------------------------------------)

An open source machine learning framework that accelerates the path from research prototyping to production deployment

[![PyTorch](https://miro.medium.com/v2/resize:fill:96:96/1*8AaAYxLb-VOgGUW8V8JXQA.png)](https://medium.com/@pytorch?source=post_page---post_author_info--3ac13aa96cff---------------------------------------)

[![PyTorch](https://miro.medium.com/v2/resize:fill:128:128/1*8AaAYxLb-VOgGUW8V8JXQA.png)](https://medium.com/@pytorch?source=post_page---post_author_info--3ac13aa96cff---------------------------------------)

[9 following](https://medium.com/@pytorch/following?source=post_page---post_author_info--3ac13aa96cff---------------------------------------)

PyTorch is an open source machine learning platform that provides a seamless path from research prototyping to production deployment.

## Responses (2)

Wangzhefengr

What are your thoughts?  

==Even with the most advanced compute hardware, training models with 10B+ parameters require multiple GPUs, and training models with 100B+ parameters require several multi-GPU nodes.==

```c
My experience is that training even millions of parameters require multiple GPUs. This is of course taking into consideration a volta32 gpu. Not worked with more advanced specifications yet.
```

```c
Great post! It would be very useful if you keep a page where you summarize findings of this and future experiments to provide guidelines for getting the most out of distributed training for different modeling scenarios.
```