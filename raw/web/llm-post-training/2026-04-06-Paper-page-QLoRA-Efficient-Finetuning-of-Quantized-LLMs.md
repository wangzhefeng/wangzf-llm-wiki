---
source_type: web
title: "Paper page - QLoRA: Efficient Finetuning of Quantized LLMs"
author: 
created_at: 2026-04-06
status: inbox
created: 2026-04-06
description: "Join the discussion on this paper page"
tags:
  - 
  - "clippings"
source_url: "https://huggingface.co/papers/2305.14314"
published_at: 2023-05-24
related_concepts: []
topics:
  - llm-post-training
  - 大语言模型后训练
---

arxiv:2305.14314

## QLoRA: Efficient Finetuning of Quantized LLMs

Authors:

## Abstract

QLoRA enables efficient finetuning of large language models using 4-bit quantization and Low Rank Adapters, achieving high performance with reduced memory usage.

AI-generated summary

We present [QLoRA](https://huggingface.co/papers?q=QLoRA), an efficient finetuning approach that reduces memory usage enough to finetune a 65B parameter model on a single 48GB GPU while preserving full 16-bit finetuning task performance. [QLoRA](https://huggingface.co/papers?q=QLoRA) backpropagates gradients through a frozen, [4-bit quantized](https://huggingface.co/papers?q=4-bit%20quantized) pretrained language model into Low Rank Adapters~([LoRA](https://huggingface.co/papers?q=LoRA)). Our best model family, which we name [Guanaco](https://huggingface.co/papers?q=Guanaco), outperforms all previous openly released models on the [Vicuna benchmark](https://huggingface.co/papers?q=Vicuna%20benchmark), reaching 99.3% of the performance level of [ChatGPT](https://huggingface.co/papers?q=ChatGPT) while only requiring 24 hours of finetuning on a single GPU. [QLoRA](https://huggingface.co/papers?q=QLoRA) introduces a number of innovations to save memory without sacrificing performance: (a) 4-bit [NormalFloat (NF4)](https://huggingface.co/papers?q=NormalFloat%20\(NF4\)), a new data type that is information theoretically optimal for normally distributed weights (b) double quantization to reduce the average memory footprint by quantizing the quantization constants, and (c) paged optimziers to manage memory spikes. We use [QLoRA](https://huggingface.co/papers?q=QLoRA) to finetune more than 1,000 models, providing a detailed analysis of instruction following and chatbot performance across 8 instruction datasets, multiple model types ([LLaMA](https://huggingface.co/papers?q=LLaMA), [T5](https://huggingface.co/papers?q=T5)), and model scales that would be infeasible to run with regular finetuning (e.g. 33B and 65B parameter models). Our results show that [QLoRA](https://huggingface.co/papers?q=QLoRA) finetuning on a small high-quality dataset leads to state-of-the-art results, even when using smaller models than the previous SoTA. We provide a detailed analysis of chatbot performance based on both human and GPT-4 evaluations showing that GPT-4 evaluations are a cheap and reasonable alternative to human evaluation. Furthermore, we find that current chatbot benchmarks are not trustworthy to accurately evaluate the performance levels of chatbots. A lemon-picked analysis demonstrates where [Guanaco](https://huggingface.co/papers?q=Guanaco) fails compared to [ChatGPT](https://huggingface.co/papers?q=ChatGPT). We release all of our models and code, including [CUDA kernels](https://huggingface.co/papers?q=CUDA%20kernels) for 4-bit training.

### Community

[osanseviero](https://huggingface.co/osanseviero)

[May 24, 2023](#646e20345c3c0df5aefa34a7)

Super exciting paper!

[abtExp](https://huggingface.co/abtExp)

[May 24, 2023](#646e303c5c3c0df5aefc6b0e)

With the large embedding models driving the AI development, techniques like this will play a major role to make it feasible to train much larger models and open up new research frontiers. Very exciting🤗

[leandrobortolotto](https://huggingface.co/leandrobortolotto)

[May 31, 2023](#6476486657108da176fcbfe4)

Congratulations on this excellent paper. It gives not only the results of the study but also it's very informative. Thank you.

[maharmaybe](https://huggingface.co/maharmaybe)

[Feb 23, 2024](#65d77686935120e85fb3c624)

•

[edited Feb 23, 2024](#65d77686935120e85fb3c624 "Edited by maharmaybe")

(/◕ヮ◕)/

[m-ric](https://huggingface.co/m-ric)

[Feb 27, 2024](#65ddaaa07a14b83ee007402c)

Thank you, great read!  
Here are my main takeaways:

- **Innovations:**
	- 4-bit NormalFloat (NF4), a new datatype that is information theoretically optimal for normally distributed weights. This is used only for storage: the computation data type is still bf16, so for the forward and backward pass you de-quantize the storage data type.
		- Double quantization by quantizing the quantization constants: when quantizing, you need to rescale your values by a constant C to make them fit into a certain range. Double quantization quantizes C, thus saves an average 0.37b per parameter, which is quite significant!
		- Paged Optimizers to manage memory spikes, by using NVIDIA unified memory (transfers between GPU and CPU) to avoid gradient checkpointing memory spikes that occur when processing a mini-batch with a long sequence length.
- **Effect:**
	- On compute:
		- the memory cost is greatly reduced, at the cost of a small computational overhead
		- On model accuracy: no degradation of performance.
- About bf16: this data type is brain float16, introduced by Google brain type, that differently manage mantissa and exponent bits to get fp32-level performance with the size of fp16.
- **Hyperparameters used for finetuning experiments:**
	- “We find LoRA r is unrelated to final performance if LoRA is used on all layers”
		- LR: 1e-4 or 2e-4, constant schedule.
		- Batch size: 16 for models under 13B, 16 or 32 for 33B, 16-64 for 65B
		- NF4 with double quantization and bf16 computation datatype.
		- LoRA r = 64, α = 16
		- We also use Adam beta2 of 0.999, max grad norm of 0.3 and LoRA dropout of 0.1 for models up to 13B and 0.05 for 33B and 65B models.
		- Target modules: “all linear layers of the base model”
		- “use group-by-length to group examples of similar lengths in the same  
		batch (note this will produce a oscillating loss curve)”
- Question: the paper says “We find that LoRA dropout 0.05 is useful for small models (7B, 13B), but not for larger models (33B, 65B).” Then why use the opposite in the finetuning experiments?

[iKyalo](https://huggingface.co/iKyalo)

[Mar 21, 2024](#65fc33836529e3fcc2467290)

This comment has been hidden

[Eliedonda1234](https://huggingface.co/Eliedonda1234)

[Jul 20, 2025](#687cc5597a027369d6058ed4)

Hello

[Eliedonda1234](https://huggingface.co/Eliedonda1234)

[Jul 20, 2025](#687cc56889a9cd02639bbec6)

H

[grantsing](https://huggingface.co/grantsing)

[Sep 16, 2025](#68c928cd1107050cf22c4497)

arXiv explained breakdown of this paper 👇 [https://arxivexplained.com/papers/qlora-efficient-finetuning-of-quantized-llms](https://arxivexplained.com/papers/qlora-efficient-finetuning-of-quantized-llms)

## Models citing this paper 311

[Browse 311 models citing this paper](https://huggingface.co/models?other=arxiv:2305.14314)

## Datasets citing this paper 6

[Browse 6 datasets citing this paper](https://huggingface.co/datasets?other=arxiv:2305.14314)