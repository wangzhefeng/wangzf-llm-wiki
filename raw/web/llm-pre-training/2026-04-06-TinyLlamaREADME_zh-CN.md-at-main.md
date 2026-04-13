---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: The TinyLlama project is an open endeavor to pretrain a 1.1B Llama model
  on 3 trillion tokens. - TinyLlama/README_zh-CN.md at main · jzhang38/TinyLlama
source_type: web
status: inbox
tags:
- null
- clippings
title: TinyLlama/README_zh-CN.md at main
source_url: https://github.com/jzhang38/TinyLlama/blob/main/README_zh-CN.md
published_at: null
related_concepts: []
topics:
  - llm-pre-training
  - 大语言模型预训练
---

## TinyLlama-1.1B

[English](https://github.com/jzhang38/TinyLlama/blob/main/README.md) | 中文

[Chat Demo](https://huggingface.co/spaces/TinyLlama/tinyllama-chat)

TinyLlama项目旨在在3万亿tokens上进行预训练，构建一个拥有11亿参数的Llama模型。经过精心优化，我们"仅"需16块A100-40G的GPU，便可在90天内完成这个任务🚀🚀。训练已于2023-09-01开始。

[![[raw/assets/attachments/llm/TinyLlama_logo.png]]](https://github.com/jzhang38/TinyLlama/blob/main/.github/TinyLlama_logo.png)

我们采用了与Llama 2完全相同的架构和分词器。这意味着TinyLlama可以在许多基于Llama的开源项目中即插即用。此外，TinyLlama只有1.1B的参数，体积小巧，适用于需要限制计算和内存占用的多种应用。

#### 新闻

- 2023-12-18：
	- 添加两个文档 [1](https://whimsical-aphid-86d.notion.site/Release-of-TinyLlama-1-5T-Checkpoints-Postponed-01b266998c1c47f78f5ae1520196d194?pvs=4), [2](https://whimsical-aphid-86d.notion.site/Latest-Updates-from-TinyLlama-Team-7d30c01fff794da28ccc952f327c8d4f?pvs=4) 说明训练曲线、项目时间表和错误修复的变化。
- 2023-10-03:
	- 在speculative decoding中添加llama.cpp的代码示例。具体请查看 [speculative\_decoding/README.md](https://github.com/jzhang38/TinyLlama/blob/main/speculative_decoding/README.md) 。
		- 2023-10-02: 1. 1T-token检查点刚发布。2. 我们在 [huggingface](https://huggingface.co/TinyLlama/tinyLlama-intermediate-checkpoints/tree/step-480k-token-1007B) 上记录了 **所有** 中间检查点。
		- 2023-09-28: 启用 [Discord](https://discord.gg/74Wcx4j5Nb) 服务器。
- 2023-09-18:
	- 发布了一个 [chat demo](https://huggingface.co/spaces/TinyLlama/tinyllama-chat) ，欢迎点击链接来尝试我们的模型。
- 2023-09-16:
	- 发布了目前已经训练了 5.03 亿个 token 的 [checkpoints 模型](https://huggingface.co/PY007/TinyLlama-1.1B-intermediate-step-240k-503b) 。
		- 基于 5.03 亿 token 的 [checkpoints 模型](https://huggingface.co/PY007/TinyLlama-1.1B-intermediate-step-240k-503b) 在 OpenAssistant 数据集上微调并开源了聊天模型 [TinyLlama-Chat-V0.1](https://huggingface.co/PY007/TinyLlama-1.1B-Chat-v0.1) ，并添加了我们的 [微调脚本](https://github.com/jzhang38/TinyLlama/blob/main/sft) 。
		- 添加了更多的评测数据集，您可以通过 [EVAL.md](https://github.com/jzhang38/TinyLlama/blob/main/EVAL.md) 文件来查看我们各模型的结果。

#### 发布时间表

我们会根据以下计划逐步发布中间checkpoint。我们也列了一些基线模型进行比较。

基座模型:

| Date | 模型权重 | Tokens | Step | Commonsense Avg |
| --- | --- | --- | --- | --- |
| 2023-09-01 | Pythia-1.0B | 300B | 143k | 48.30 |
| 2023-09-04 | [TinyLlama-1.1B-intermediate-step-50k-105b](https://huggingface.co/PY007/TinyLlama-1.1B-step-50K-105b) ([ModelScope](https://www.modelscope.cn/models/chaoscodes/TinyLlama-1.1B-step-50K-105b/files)) | 105B | 50k | 46.11 |
| 2023-09-16 | [TinyLlama-1.1B-intermediate-step-240k-503b](https://huggingface.co/PY007/TinyLlama-1.1B-intermediate-step-240k-503b) ([ModelScope](https://www.modelscope.cn/models/chaoscodes/TinyLlama-1.1B-intermediate-step-240k-503b/files)) | 503B | 240K | 48.28 |
| 2023-10-01 | [TinyLlama-1.1B-intermediate-step-480k-1T](https://huggingface.co/PY007/TinyLlama-1.1B-intermediate-step-480k-1T) | 1T | 480k | 50.22 |
| 2023-11-04 | [TinyLlama-1.1B-intermediate-step-715k-1.5T](https://huggingface.co/PY007/TinyLlama-1.1B-intermediate-step-715k-1.5T) | 1.5T | 715k | 51.28 |
| 2023-11-20 | [TinyLlama-1.1B-intermediate-step-955k-2T](https://huggingface.co/TinyLlama/TinyLlama-1.1B-intermediate-step-955k-token-2T) | 2T | 955k | 51.64 |
| 2023-12-11 | [TinyLlama-1.1B-intermediate-step-1195k-2.5T](https://huggingface.co/TinyLlama/TinyLlama-1.1B-intermediate-step-1195k-token-2.5T) | 2.5T | 1195k | 53.86 |
| 2023-12-28 | [TinyLlama-1.1B-intermediate-step-1431k-3T](https://huggingface.co/TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T) | 3T | 1431k | 52.99 |

对话模型:

| Date | 模型权重 | Tokens | Step | Commonsense Avg |
| --- | --- | --- | --- | --- |
| 2023-09-16 | [TinyLlama-1.1B-Chat-V0.1](https://huggingface.co/PY007/TinyLlama-1.1B-Chat-v0.1) ([ModelScope](https://www.modelscope.cn/models/chaoscodes/TinyLlama-1.1B-Chat-v0.1/files)) | 503B | 240K | 49.57 |
| 2023-10-1 | [TinyLlama-1.1B-Chat-V0.3](https://huggingface.co/PY007/TinyLlama-1.1B-Chat-v0.3) | 1T | 480K | 51.36 |
| 2023-11-04 | [TinyLlama-1.1B-Chat-V0.4](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v0.4) | 1.5T | 715K | 52.30 |

需要注意的是，由于我们的现在模型还处于训练初期，学习率并没有完全稳定下来，为了更好的体验我们的模型，您可以下载我们 [聊天模型](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) 或者通过 [chat demo](https://huggingface.co/spaces/TinyLlama/tinyllama-chat) 来尝试我们的模型。

你们也可以在 [这里](https://api.wandb.ai/links/lance777/pgvhrsny) 实时跟踪TinyLlama的训练损失。

## 潜在场景

小型但强大的语言模型对许多应用都很有用。以下是一些潜在的场景：

- 帮助对大型模型进行speculative decoding。
- 在边缘装置上运行，比如离线的实时机器翻译 (TinyLlama的4比特量化版本的模型权重只需要550MB的内存)。
- 在游戏中实现实时对话生成(因为还得给游戏本身留显存所以模型要小)。

此外，我们的代码可以给初学者做一个 **入门预训练的简洁参考** 。如果你要训练50亿以下参数的语言模型, 你其实不需要Megatron-LM。

## 训练细节

以下是我们训练设置的一些细节：

| Setting | Description |
| --- | --- |
| Parameters | 1.1B |
| Attention Variant | Grouped Query Attention |
| Model Size | Layers: 22, Heads: 32, Query Groups: 4, Embedding Size: 2048, Intermediate Size (Swiglu): 5632 |
| Sequence Length | 2048 |
| Batch Size | 2 million tokens (2048 \* 1024) |
| Learning Rate | 4e-4 |
| Learning Rate Schedule | Cosine with 2000 warmup steps |
| Training Data | [Slimpajama](https://huggingface.co/datasets/cerebras/slimpajama-627b) & [Starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata) |
| Data Preprocessing | Excluded GitHub subset of Slimpajama; Sampled all code from Starcoderdata |
| Combined Dataset Size | Around 950B tokens |
| Total Tokens During Training | 3 trillion (slightly more than 3 epochs/143k steps) |
| Natural Language to Code Ratio | 7:3 |
| Hardware | 16 A100-40G GPUs |

## 速度极快

我们的代码库支持以下特性：

- 使用FSDP进行多GPU和多节点分布式训练
- flash attention 2
- 融合层归一化 (fused layernorm)
- 融合swiglu (fused swiglu)
- 融合交叉熵损失 (fused cross entropy loss)
- 融合旋转位置嵌入 (fused rotary positional embedding)

致谢：flash attention 2、融合层归一化、融合交叉熵损失和融合旋转位置嵌入来自于 [FlashAttention](https://github.com/Dao-AILab/flash-attention/) 仓库；融合swiglu来自于 [xformers](https://github.com/facebookresearch/xformers) 。

有了这些优化, 我们可以达到 **24k tokens/秒/A100** 的训练速度，也就是56%的MFU（在A100-80G上的MFU会更高）。这个速度可以让你可以在 **8个A100上用32小时训练一个chinchilla-optimial的模型** (11亿参数，220亿token)。这些优化也大大减少了显存占用, 我们可以把11亿参数的模型塞入40GB的GPU里面还能同时维持16k tokens的per-gpu batch size。只需要把batch size改小一点， 你就可以在 **RTX 3090/4090** 上面训练TinyLlama。 下面是我们的代码库与Pythia和MPT的训练速度的比较。

| Model | A100 GPU hours taken on 300B tokens |
| --- | --- |
| TinyLlama-1.1B | 3456 |
| [Pythia-1.0B](https://huggingface.co/EleutherAI/pythia-1b) | 4830 |
| [MPT-1.3B](https://huggingface.co/mosaicml/mpt-1b-redpajama-200b) | 7920 |

Pythia的数字来自他们的论文。MPT的数字来自 [这里](https://huggingface.co/mosaicml/mpt-1b-redpajama-200b) ，作者说MPT-1.3B"was trained on 440 A100-40GBs for about half a day" on 200B tokens。

TinyLlama是一个相对较小的模型, 同时我们用了GQA, 这意味着它在推理期间也很快。以下是我们测量的一些推理速度：

| Framework | Device | Settings | Throughput (tokens/sec) |
| --- | --- | --- | --- |
| [Llama.cpp](https://github.com/ggerganov/llama.cpp) | Mac M2 16GB RAM | batch\_size=1; 4-bit inference | 71.8 |
| [vLLM](https://github.com/vllm-project/vllm) | A40 GPU | batch\_size=100, n=10 | 7094.5 |

## 开始预训练

请参考 [PRETRAIN.md](https://github.com/jzhang38/TinyLlama/blob/main/PRETRAIN.md) 。

## 微调

- 我们在 [sft](https://github.com/jzhang38/TinyLlama/blob/main/sft) 中添加了我们进行微调和推理的代码。并且基于这个代码我们在 [openassistant-guanaco](https://huggingface.co/datasets/timdettmers/openassistant-guanaco) 数据集上进行了微调，得到了我们的第一版 [聊天模型](https://huggingface.co/PY007/TinyLlama-1.1B-Chat-v0.1) 。
- 如果您希望在 RAM 小于 4GB 的 GPU 上对用我们的模型进行微调，可以参考并使用 [Qlora](https://github.com/artidoro/qlora) 和 [bitsandbytes](https://github.com/TimDettmers/bitsandbytes) 项目。
- 目前微调的时候我们并没有广泛对超参进行搜索，也没有选择潜在更优的 instruction 数据集。我们希望促进 NLP 社区对于我们的TinyLlama模型的开放研究，并开源更好的微调聊天模型。我们也会把这些模型放在这个项目中。

## TODO

该项目仍在积极开发中。我们团队很小，非常欢迎社区的反馈和贡献。以下是我们计划进行的一些工作：

- Add scripts for pretraining on other datasets.
- Sequence length extrapolation.
- Test out speculative decoding for Llama-2-7B.
- Test the throughput on RTX 3090/4090.
- Add fine-tuning scripts.
- Properly evaluate the model on downstream tasks.
- A demo running on mobile phones.
- Explore retrieval-augmentation.

## Star History

[![[Image 59.svg|Star History Chart]]](https://star-history.com/#jzhang38/TinyLlama&Date)

## Acknowledgements

这个仓库基于出色的开源项目 [lit-gpt](https://github.com/Lightning-AI/lit-gpt) 和 [flash-attention](https://github.com/Dao-AILab/flash-attention) 构建.

```
@online{lit-gpt,
  author    = {Lightning AI},
  title     = {Lit-GPT},
  url       = {https://github.com/Lightning-AI/lit-gpt},
  year      = {2023},
}
@article{dao2023flashattention2,
  title     ={Flash{A}ttention-2: Faster Attention with Better Parallelism and Work Partitioning},
  author    ={Dao, Tri},
  year      ={2023}
}
```

## Citation

此项目目前由 [Peiyuan Zhang](https://github.com/jzhang38) ， [Guangtao Zeng](https://github.com/ChaosCodes) ， [Tianduo Wang](https://github.com/TianduoWang) 和 [Wei Lu](https://istd.sutd.edu.sg/people/faculty/lu-wei/) 贡献。

如果您觉得我们的工作有价值， 可以引用:

```
@misc{zhang2024tinyllama,
      title={TinyLlama: An Open-Source Small Language Model}, 
      author={Peiyuan Zhang and Guangtao Zeng and Tianduo Wang and Wei Lu},
      year={2024},
      eprint={2401.02385},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```