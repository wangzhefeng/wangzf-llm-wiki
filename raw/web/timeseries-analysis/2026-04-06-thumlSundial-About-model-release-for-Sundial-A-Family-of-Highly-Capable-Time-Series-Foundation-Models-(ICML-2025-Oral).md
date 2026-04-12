---
source_type: web
title: "thuml/Sundial: About model release for \"Sundial: A Family of Highly Capable Time Series Foundation Models\" (ICML 2025 Oral)"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: "About model release for \"Sundial: A Family of Highly Capable Time Series Foundation Models\" (ICML 2025 Oral) - thuml/Sundial"
tags:
  - 
  - "clippings"
source_url: "https://github.com/thuml/Sundial/tree/main"
published_at: null
related_concepts: []
---

## Sundial

This is the official repository of [Sundial: A Family of Highly Capable Time Series Foundation Models](https://arxiv.org/abs/2502.00816) [\[Slides\]](https://cloud.tsinghua.edu.cn/f/8d526337afde465e87c9/) [\[Poster\]](https://cloud.tsinghua.edu.cn/f/cc2a156315e9453f99b3/) [\[Intro (CN)\]](https://mp.weixin.qq.com/s/y3sc2e2lmW1sqfnoK-ZdDA).

[![[raw/assets/attachments/timeseries/cover 1.png]]](https://github.com/thuml/Sundial/blob/main/figures/cover.png)

## Updates

🚩 **News** (2025.06) Sundial has been accepted as **ICML 2025 Oral** (Top 1%). See you at Vancouver:)

🚩 **News** (2025.05) Get **1st MASE** on the [GIFT-Eval](https://huggingface.co/spaces/Salesforce/GIFT-Eval) Benchmark.

🚩 **News** (2025.05) Released a **trillion-scale** pre-trained model on [HuggingFace](https://huggingface.co/thuml/sundial-base-128m). A quickstart is provided [here](https://github.com/thuml/Sundial/blob/main/examples/quickstart_zero_shot_generation.ipynb).

🚩 **News** (2025.02) Get **1st MSE/MAE** zero-shot performance on [Time-Series-Library](https://github.com/thuml/Time-Series-Library) datasets.

## Introduction

Sundial is a family of **generative** time series foundation models, which is pre-trained on TimeBench (**10^12** time points). The model can be applied for both **point** / **probabilistic** **zero-shot** forecasting.

Not only the mean or quantiles, you can get any statistical predictions with a set of generated samples.

We propose **TimeFlow Loss** to predict next-patch’s distribution, allowing Transformers to be trained **without discrete tokenization** and make **non-deterministic predictions**.

[![[compare.png]]](https://github.com/thuml/Sundial/blob/main/figures/compare.png)

## Quickstart

We release a [HuggingFace model](https://huggingface.co/thuml/sundial-base-128m), which can make zero-shot predictions on CPU within seconds! 🚀

> Inference Time on Apple M1 Pro CPU (16 GB)

| Lookback | Forcast | \# Generated | Wall-Clock Time | Accelerate By |
| --- | --- | --- | --- | --- |
| 672 | 16 | 1 | 249ms | \- |
| 2880 | 16 | 1 | 510ms | FlashAttention |
| 2880 | 720 | 1 | 510ms | Multi-Patch Prediction |
| 2880 | 1440 | 1 | 789ms | KV Cache |
| 2880 | 720 | 20 | 949ms | Shared Condition |

All you need is a network and a HuggingFace account!

```
pip install transformers==4.40.1
```

```
import torch
from transformers import AutoModelForCausalLM

# load pretrain model
# supports different lookback/forecast lengths
model = AutoModelForCausalLM.from_pretrained('thuml/sundial-base-128m', trust_remote_code=True) 

# prepare input
batch_size, lookback_length = 1, 2880 
seqs = torch.randn(batch_size, lookback_length)

# Note that Sundial can generate multiple probable predictions
forecast_length = 96 
num_samples = 20

output = model.generate(seqs, max_new_tokens=forecast_length, num_samples=num_samples)

# use raw predictions for mean/quantiles/confidence-interval estimation
print(output.shape)
```

More examples of predicting quantiles or confidence intervals are provided in this [notebook](https://github.com/thuml/Sundial/blob/main/examples/quickstart_zero_shot_generation.ipynb). Please raise your valuable suggestions [here](https://huggingface.co/thuml/sundial-base-128m/discussions/new), we 'd like to solve it ASAP 🤗.

## Architecture

![arch.png](https://github.com/thuml/Sundial/blob/main/figures/arch.png)

> Intuitively, Sundial can be viewed as an **ARMA** model (Auto-Regression and Moving-Average). Transformer learns auto-regressive token representations. Conditioned on them, TimeFlow transforms random noises into non-deterministic predictions.

## Model Configurations

We have currently built three different sizes of Sundial. Model configurations are provided here:

[![[config.png]]](https://github.com/thuml/Sundial/blob/main/figures/config.png)

## Evaluation

We evaluate Sundial (Base) with advanced time series foundation models on well-recognized benchmarks:

- [GIFT-Eval (1st MASE)](https://cdn-uploads.huggingface.co/production/uploads/64fbe24a2d20ced4e91de38a/3BxatwayhK5GAoqMf1oHv.png) [\[Leaderboard\]](https://huggingface.co/spaces/Salesforce/GIFT-Eval).
- [Time-Series-Library (1st MSE/MAE)](https://cdn-uploads.huggingface.co/production/uploads/64fbe24a2d20ced4e91de38a/5VqnFwWTWoYz877Zkluiw.png).
- [FEV Leaderboard](https://cdn-uploads.huggingface.co/production/uploads/64fbe24a2d20ced4e91de38a/mrKL9QmX-aX8rCiwxKgmA.png).

## Exciting News ✨

Code for fine-tuning is on its way and will be available soon! Stay tuned for updates!

## Citation

If you find this repo helpful, please cite our paper.

```
@article{liu2025sundial,
  title={Sundial: A Family of Highly Capable Time Series Foundation Models},
  author={Liu, Yong and Qin, Guo and Shi, Zhiyuan and Chen, Zhi and Yang, Caiyin and Huang, Xiangdong and Wang, Jianmin and Long, Mingsheng},
  journal={arXiv preprint arXiv:2502.00816},
  year={2025}
}
```