---
source_type: web
title: "amazon-science/chronos-forecasting: Chronos: Pretrained Models for Time Series Forecasting"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://github.com/amazon-science/chronos-forecasting"
published: 
created: 2026-04-06
description: "Chronos: Pretrained Models for Time Series Forecasting - amazon-science/chronos-forecasting"
tags:
  - 
  - "clippings"
---

## 🚀 News

- **30 Dec 2025**: ☁️ Deploy Chronos-2 to AWS with Amazon SageMaker: new guide covers real-time inference (GPU/CPU), serverless endpoints with automatic scaling, and batch transform for large-scale forecasting. See the [deployment tutorial](https://github.com/amazon-science/chronos-forecasting/blob/main/notebooks/deploy-chronos-to-amazon-sagemaker.ipynb).
- **20 Oct 2025**: 🚀 [Chronos-2](https://huggingface.co/amazon/chronos-2) released. It offers *zero-shot* support for univariate, multivariate, and covariate-informed forecasting tasks. Chronos-2 achieves the best performance on fev-bench, GIFT-Eval and Chronos Benchmark II amongst pretrained models. Check out [this notebook](https://github.com/amazon-science/chronos-forecasting/blob/main/notebooks/chronos-2-quickstart.ipynb) to get started with Chronos-2.
- **12 Dec 2024**: 📊 We released [`fev`](https://github.com/autogluon/fev), a lightweight package for benchmarking time series forecasting models based on the [Hugging Face `datasets`](https://huggingface.co/docs/datasets/en/index) library.
- **26 Nov 2024**: ⚡️ Chronos-Bolt models released [on HuggingFace](https://huggingface.co/collections/amazon/chronos-models-65f1791d630a8d57cb718444). Chronos-Bolt models are more accurate (5% lower error), up to 250x faster and 20x more memory efficient than the original Chronos models of the same size!
- **13 Mar 2024**: 🚀 Chronos [paper](https://arxiv.org/abs/2403.07815) and inference code released.

## ✨ Introduction

This package provides an interface to the Chronos family of **pretrained time series forecasting models**. The following model types are supported.

- **Chronos-2**: Our latest model with significantly enhanced capabilities. It offers zero-shot support for univariate, multivariate, and covariate-informed forecasting tasks. Chronos-2 delivers state-of-the-art zero-shot performance across multiple benchmarks (including fev-bench and GIFT-Eval), with the largest improvements observed on tasks that include exogenous features. It also achieves a win rate of over 90% against Chronos-Bolt in head-to-head comparisons. To learn more about Chronos, check out the [technical report](https://arxiv.org/abs/2510.15821).
- **Chronos-Bolt**: A patch-based variant of Chronos. It chunks the historical time series context into patches of multiple observations, which are then input into the encoder. The decoder then uses these representations to directly generate quantile forecasts across multiple future steps—a method known as direct multi-step forecasting. Chronos-Bolt models are up to 250 times faster and 20 times more memory-efficient than the original Chronos models of the same size. To learn more about Chronos-Bolt, check out this [blog post](https://aws.amazon.com/blogs/machine-learning/fast-and-accurate-zero-shot-forecasting-with-chronos-bolt-and-autogluon/).
- **Chronos**: The original Chronos family which is based on language model architectures. A time series is transformed into a sequence of tokens via scaling and quantization, and a language model is trained on these tokens using the cross-entropy loss. Once trained, probabilistic forecasts are obtained by sampling multiple future trajectories given the historical context. To learn more about Chronos, check out the [publication](https://openreview.net/forum?id=gerNCVqqtR).

### Available Models

| Model ID | Parameters |
| --- | --- |
| [`amazon/chronos-2`](https://huggingface.co/amazon/chronos-2) | 120M |
| [`autogluon/chronos-2-synth`](https://huggingface.co/autogluon/chronos-2-synth) | 120M |
| [`autogluon/chronos-2-small`](https://huggingface.co/autogluon/chronos-2-small) | 28M |
| [`amazon/chronos-bolt-tiny`](https://huggingface.co/amazon/chronos-bolt-tiny) | 9M |
| [`amazon/chronos-bolt-mini`](https://huggingface.co/amazon/chronos-bolt-mini) | 21M |
| [`amazon/chronos-bolt-small`](https://huggingface.co/amazon/chronos-bolt-small) | 48M |
| [`amazon/chronos-bolt-base`](https://huggingface.co/amazon/chronos-bolt-base) | 205M |
| [`amazon/chronos-t5-tiny`](https://huggingface.co/amazon/chronos-t5-tiny) | 8M |
| [`amazon/chronos-t5-mini`](https://huggingface.co/amazon/chronos-t5-mini) | 20M |
| [`amazon/chronos-t5-small`](https://huggingface.co/amazon/chronos-t5-small) | 46M |
| [`amazon/chronos-t5-base`](https://huggingface.co/amazon/chronos-t5-base) | 200M |
| [`amazon/chronos-t5-large`](https://huggingface.co/amazon/chronos-t5-large) | 710M |

## 📈 Usage

To perform inference with Chronos, the easiest way is to install this package through `pip`:

```
pip install chronos-forecasting
```

> [!tip] Tip
> For reliable production use, we recommend using Chronos-2 models through [Amazon SageMaker JumpStart](https://aws.amazon.com/sagemaker/ai/jumpstart/). Check out [this tutorial](https://github.com/amazon-science/chronos-forecasting/blob/main/notebooks/deploy-chronos-to-amazon-sagemaker.ipynb) to learn how to deploy Chronos-2 inference endpoints to AWS with just a few lines of code.

### Forecasting

A minimal example showing how to perform forecasting using Chronos-2:

```
import pandas as pd  # requires: pip install 'pandas[pyarrow]'
from chronos import Chronos2Pipeline

pipeline = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cuda")

# Load historical target values and past values of covariates
context_df = pd.read_parquet("https://autogluon.s3.amazonaws.com/datasets/timeseries/electricity_price/train.parquet")

# (Optional) Load future values of covariates
test_df = pd.read_parquet("https://autogluon.s3.amazonaws.com/datasets/timeseries/electricity_price/test.parquet")
future_df = test_df.drop(columns="target")

# Generate predictions with covariates
pred_df = pipeline.predict_df(
    context_df,
    future_df=future_df,
    prediction_length=24,  # Number of steps to forecast
    quantile_levels=[0.1, 0.5, 0.9],  # Quantile for probabilistic forecast
    id_column="id",  # Column identifying different time series
    timestamp_column="timestamp",  # Column with datetime information
    target="target",  # Column(s) with time series values to predict
)
```

We can now visualize the forecast:

```
import matplotlib.pyplot as plt  # requires: pip install matplotlib

ts_context = context_df.set_index("timestamp")["target"].tail(256)
ts_pred = pred_df.set_index("timestamp")
ts_ground_truth = test_df.set_index("timestamp")["target"]

ts_context.plot(label="historical data", color="xkcd:azure", figsize=(12, 3))
ts_ground_truth.plot(label="future data (ground truth)", color="xkcd:grass green")
ts_pred["predictions"].plot(label="forecast", color="xkcd:violet")
plt.fill_between(
    ts_pred.index,
    ts_pred["0.1"],
    ts_pred["0.9"],
    alpha=0.7,
    label="prediction interval",
    color="xkcd:light lavender",
)
plt.legend()
```

## Example Notebooks

- [Chronos-2 Quick Start](https://github.com/amazon-science/chronos-forecasting/blob/main/notebooks/chronos-2-quickstart.ipynb)
- [Deploy Chronos-2 on Amazon SageMaker](https://github.com/amazon-science/chronos-forecasting/blob/main/notebooks/deploy-chronos-to-amazon-sagemaker.ipynb)

## 📝 Citation

If you find Chronos models useful for your research, please consider citing the associated papers:

```
@article{ansari2024chronos,
  title={Chronos: Learning the Language of Time Series},
  author={Ansari, Abdul Fatir and Stella, Lorenzo and Turkmen, Caner and Zhang, Xiyuan, and Mercado, Pedro and Shen, Huibin and Shchur, Oleksandr and Rangapuram, Syama Syndar and Pineda Arango, Sebastian and Kapoor, Shubham and Zschiegner, Jasper and Maddix, Danielle C. and Mahoney, Michael W. and Torkkola, Kari and Gordon Wilson, Andrew and Bohlke-Schneider, Michael and Wang, Yuyang},
  journal={Transactions on Machine Learning Research},
  issn={2835-8856},
  year={2024},
  url={https://openreview.net/forum?id=gerNCVqqtR}
}

@article{ansari2025chronos2,
  title        = {Chronos-2: From Univariate to Universal Forecasting},
  author       = {Abdul Fatir Ansari and Oleksandr Shchur and Jaris Küken and Andreas Auer and Boran Han and Pedro Mercado and Syama Sundar Rangapuram and Huibin Shen and Lorenzo Stella and Xiyuan Zhang and Mononito Goswami and Shubham Kapoor and Danielle C. Maddix and Pablo Guerron and Tony Hu and Junming Yin and Nick Erickson and Prateek Mutalik Desai and Hao Wang and Huzefa Rangwala and George Karypis and Yuyang Wang and Michael Bohlke-Schneider},
  journal      = {arXiv preprint arXiv:2510.15821},
  year         = {2025},
  url          = {https://arxiv.org/abs/2510.15821}
}
```