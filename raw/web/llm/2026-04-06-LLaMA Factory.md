---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: null
published: null
source: https://llamafactory.readthedocs.io/zh-cn/latest/
source_type: web
status: inbox
tags:
- null
- clippings
title: LLaMA Factory
topics:
- 大语言模型
---

## Welcome to LLaMA Factory!

![[logo.png|logo]]

LLaMA Factory 是一个简单易用且高效的大型语言模型（Large Language Model）训练与微调平台。通过 LLaMA Factory，可以在无需编写任何代码的前提下，在本地完成上百种预训练模型的微调，框架特性包括：

- 模型种类：LLaMA、LLaVA、Mistral、Mixtral-MoE、Qwen、Yi、Gemma、Baichuan、ChatGLM、Phi 等等。
- 训练算法：（增量）预训练、（多模态）指令监督微调、奖励模型训练、PPO 训练、DPO 训练、KTO 训练、ORPO 训练等等。
- 运算精度：16 比特全参数微调、冻结微调、LoRA 微调和基于 AQLM/AWQ/GPTQ/LLM.int8/HQQ/EETQ 的 2/3/4/5/6/8 比特 QLoRA 微调。
- 优化算法：GaLore、BAdam、DoRA、LongLoRA、LLaMA Pro、Mixture-of-Depths、LoRA+、LoftQ 和 PiSSA。
- 加速算子：FlashAttention-2 和 Unsloth。
- 推理引擎：Transformers 和 vLLM。
- 实验监控：LlamaBoard、TensorBoard、Wandb、MLflow、SwanLab 等等。

## Documentation

高级选项

- [加速](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/acceleration.html)
	- [FlashAttention](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/acceleration.html#flashattention)
		- [Unsloth](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/acceleration.html#unsloth)
		- [Liger Kernel](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/acceleration.html#liger-kernel)
- [调优算法](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html)
	- [Full Parameter Fine-tuning](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#full-parameter-fine-tuning)
		- [Freeze](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#freeze)
		- [LoRA](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#lora)
		- [LoRA+](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#id5)
				- [rsLoRA](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#rslora)
				- [DoRA](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#dora)
				- [PiSSA](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#pissa)
		- [Galore](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#galore)
		- [BAdam](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/tuning_algorithms.html#badam)
- [分布训练](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html)
	- [NativeDDP](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#nativeddp)
		- [单机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id4)
				- [多机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id7)
		- [DeepSpeed](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#deepspeed)
		- [单机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id12)
				- [多机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id16)
				- [DeepSpeed 配置文件](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id20)
		- [FSDP](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#fsdp)
		- [单机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id25)
				- [多机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id29)
		- [FSDP2](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#fsdp2)
		- [Ray](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#ray)
		- [单机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id33)
				- [多机多卡](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/distributed.html#id35)
- [量化](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html)
	- [PTQ](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#ptq)
		- [GPTQ](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#gptq)
		- [QAT](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#qat)
		- [AWQ](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#awq)
		- [AQLM](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#aqlm)
		- [OFTQ](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#oftq)
		- [bitsandbytes](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#bitsandbytes)
				- [HQQ](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#hqq)
				- [EETQ](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/quantization.html#eetq)
- [训练方法](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/trainers.html)
	- [Pre-training](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/trainers.html#pre-training)
		- [Post-training](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/trainers.html#post-training)
		- [Supervised Fine-Tuning](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/trainers.html#supervised-fine-tuning)
				- [RLHF](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/trainers.html#rlhf)
				- [DPO](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/trainers.html#dpo)
				- [KTO](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/trainers.html#kto)
- [实验监控](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/monitor.html)
	- [LlamaBoard](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/monitor.html#llamaboard)
		- [SwanLab](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/monitor.html#swanlab)
		- [TensorBoard](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/monitor.html#tensorboard)
		- [Wandb](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/monitor.html#wandb)
		- [MLflow](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/monitor.html#mlflow)
- [NPU安装及配置](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html)
	- [核心依赖说明](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#id1)
		- [方式一：手动安装环境](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#install-form-pip)
		- [1\. 版本及下载链接](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#id3)
				- [2\. 驱动及固件](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#id4)
				- [3\. CANN](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#cann)
				- [4\. torch-npu](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#torch-npu)
				- [5\. 验证安装](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#id5)
		- [方式二：Docker 预安装镜像](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#docker)
		- [方式三：Docker 本地构建](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_installation.html#install-form-docker)
- [NPU训练](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_training.html)
	- [支持设备](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_training.html#id1)
		- [支持功能](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_training.html#id2)
		- [快速开始](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_training.html#id3)
		- [分布式训练](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_training.html#id4)
		- [训练方式](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_training.html#id8)
		- [性能优化](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_training.html#id9)
- [NPU推理](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/npu_inference.html)
- [参数介绍](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html)
	- [微调参数](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#id2)
		- [数据参数](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#id4)
		- [模型参数](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#id5)
		- [评估参数](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#id10)
		- [生成参数](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#id11)
		- [SwanLab 参数](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#swanlab)
		- [训练参数](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#id12)
		- [RAY](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#ray)
		- [环境变量](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/arguments.html#id13)
- [模型支持](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/model_support.html)
- [额外选项](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/extras.html)
	- [LLaMA Pro](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/extras.html#llama-pro)
- [微调最佳实践](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/best_practice/index.html)
	- [GPT-OSS](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/best_practice/gpt-oss.html)
		- [3步实现 GPT-OSS 的 LoRA 微调](https://llamafactory.readthedocs.io/zh-cn/latest/advanced/best_practice/gpt-oss.html#gpt-oss-lora)