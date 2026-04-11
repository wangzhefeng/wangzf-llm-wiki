---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: We’re on a journey to advance and democratize artificial intelligence
  through open source and open science.
source_type: web
status: inbox
tags:
- null
- clippings
title: amazon/chronos-t5-large · Hugging Face
topics:
- 时间序列
source_url: https://huggingface.co/amazon/chronos-t5-large
published_at: 2025-12-04
related_concepts: []
---

[Edit model card](https://huggingface.co/amazon/chronos-t5-large/edit/main/README.md)

A newer version of this model is available: [amazon/chronos-2](https://huggingface.co/amazon/chronos-2)

## Chronos-T5 (Large)

🚀 **Update Feb 14, 2025**: Chronos-Bolt & original Chronos models are now available on Amazon SageMaker JumpStart! Check out the [tutorial notebook](https://github.com/amazon-science/chronos-forecasting/blob/main/notebooks/deploy-chronos-to-amazon-sagemaker.ipynb) to learn how to deploy Chronos endpoints for production use in a few lines of code.

🚀 **Update Nov 27, 2024**: We have released Chronos-Bolt⚡️ models that are more accurate (5% lower error), up to 250 times faster and 20 times more memory-efficient than the original Chronos models of the same size. Check out the new models [here](https://huggingface.co/amazon/chronos-bolt-base).

Chronos is a family of **pretrained time series forecasting models** based on language model architectures. A time series is transformed into a sequence of tokens via scaling and quantization, and a language model is trained on these tokens using the cross-entropy loss. Once trained, probabilistic forecasts are obtained by sampling multiple future trajectories given the historical context. Chronos models have been trained on a large corpus of publicly available time series data, as well as synthetic data generated using Gaussian processes.

For details on Chronos models, training data and procedures, and experimental results, please refer to the paper [Chronos: Learning the Language of Time Series](https://arxiv.org/abs/2403.07815).

![[raw/assets/attachments/timeseries/main-figure.png]]  
Fig. 1: High-level depiction of Chronos. (**Left**) The input time series is scaled and quantized to obtain a sequence of tokens. (**Center**) The tokens are fed into a language model which may either be an encoder-decoder or a decoder-only model. The model is trained using the cross-entropy loss. (**Right**) During inference, we autoregressively sample tokens from the model and map them back to numerical values. Multiple trajectories are sampled to obtain a predictive distribution.

---

## Architecture

The models in this repository are based on the [T5 architecture](https://arxiv.org/abs/1910.10683). The only difference is in the vocabulary size: Chronos-T5 models use 4096 different tokens, compared to 32128 of the original T5 models, resulting in fewer parameters.

| Model | Parameters | Based on |
| --- | --- | --- |
| [**chronos-t5-tiny**](https://huggingface.co/amazon/chronos-t5-tiny) | 8M | [t5-efficient-tiny](https://huggingface.co/google/t5-efficient-tiny) |
| [**chronos-t5-mini**](https://huggingface.co/amazon/chronos-t5-mini) | 20M | [t5-efficient-mini](https://huggingface.co/google/t5-efficient-mini) |
| [**chronos-t5-small**](https://huggingface.co/amazon/chronos-t5-small) | 46M | [t5-efficient-small](https://huggingface.co/google/t5-efficient-small) |
| [**chronos-t5-base**](https://huggingface.co/amazon/chronos-t5-base) | 200M | [t5-efficient-base](https://huggingface.co/google/t5-efficient-base) |
| [**chronos-t5-large**](https://huggingface.co/amazon/chronos-t5-large) | 710M | [t5-efficient-large](https://huggingface.co/google/t5-efficient-large) |

## Usage

To perform inference with Chronos models, install the package in the GitHub [companion repo](https://github.com/amazon-science/chronos-forecasting) by running:

```
pip install git+https://github.com/amazon-science/chronos-forecasting.git
```

A minimal example showing how to perform inference using Chronos models:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from chronos import ChronosPipeline

pipeline = ChronosPipeline.from_pretrained(
  "amazon/chronos-t5-large",
  device_map="cuda",
  torch_dtype=torch.bfloat16,
)

df = pd.read_csv("https://raw.githubusercontent.com/AileenNielsen/TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv")

# context must be either a 1D tensor, a list of 1D tensors,
# or a left-padded 2D tensor with batch as the first dimension
context = torch.tensor(df["#Passengers"])
prediction_length = 12
forecast = pipeline.predict(context, prediction_length)  # shape [num_series, num_samples, prediction_length]

# visualize the forecast
forecast_index = range(len(df), len(df) + prediction_length)
low, median, high = np.quantile(forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)

plt.figure(figsize=(8, 4))
plt.plot(df["#Passengers"], color="royalblue", label="historical data")
plt.plot(forecast_index, median, color="tomato", label="median forecast")
plt.fill_between(forecast_index, low, high, color="tomato", alpha=0.3, label="80% prediction interval")
plt.legend()
plt.grid()
plt.show()
```

## Citation

If you find Chronos models useful for your research, please consider citing the associated [paper](https://arxiv.org/abs/2403.07815):

```
@article{ansari2024chronos,
    title={Chronos: Learning the Language of Time Series},
    author={Ansari, Abdul Fatir and Stella, Lorenzo and Turkmen, Caner and Zhang, Xiyuan, and Mercado, Pedro and Shen, Huibin and Shchur, Oleksandr and Rangapuram, Syama Syndar and Pineda Arango, Sebastian and Kapoor, Shubham and Zschiegner, Jasper and Maddix, Danielle C. and Mahoney, Michael W. and Torkkola, Kari and Gordon Wilson, Andrew and Bohlke-Schneider, Michael and Wang, Yuyang},
    journal={Transactions on Machine Learning Research},
    issn={2835-8856},
    year={2024},
    url={https://openreview.net/forum?id=gerNCVqqtR}
}
```

## Security

See [CONTRIBUTING](https://huggingface.co/amazon/chronos-t5-large/blob/main/CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

Downloads last month

423,412

Safetensors

Model size

0.7B params

Tensor type

F32

Inference Providers [NEW](https://huggingface.co/docs/inference-providers)

Time Series Forecasting

This model isn't deployed by any Inference Provider. [🙋 Ask for provider support](https://huggingface.co/spaces/huggingface/InferenceSupport/discussions/new?title=amazon/chronos-t5-large&description=React%20to%20this%20comment%20with%20an%20emoji%20to%20vote%20for%20%5Bamazon%2Fchronos-t5-large%5D\(%2Famazon%2Fchronos-t5-large\)%20to%20be%20supported%20by%20Inference%20Providers.%0A%0A\(optional\)%20Which%20providers%20are%20you%20interested%20in%3F%20\(Novita%2C%20Hyperbolic%2C%20Together%E2%80%A6\)%0A)

## Model tree for amazon/chronos-t5-large

Adapters

[1 model](https://huggingface.co/models?other=base_model:adapter:amazon/chronos-t5-large)

## Spaces using amazon/chronos-t5-large 10

## Collection including amazon/chronos-t5-large[Collection of artifacts related to Chronos pretrained models for time series forecasting. • 16 items • Updated • 55](https://huggingface.co/collections/amazon/chronos-models-and-datasets)