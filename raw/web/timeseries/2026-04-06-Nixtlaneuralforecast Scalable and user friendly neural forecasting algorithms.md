---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: 'Scalable and user friendly neural :brain: forecasting algorithms. -
  Nixtla/neuralforecast: Scalable and user friendly neural forecasting algorithms.'
published: null
source: https://github.com/Nixtla/neuralforecast
source_type: web
status: inbox
tags:
- null
- clippings
title: 'Nixtla/neuralforecast: Scalable and user friendly neural forecasting algorithms.'
topics:
- 时间序列
- 深度学习
---

## Nixtla

[![[raw/assets/attachments/timeseries/logo_new.png]]](https://raw.githubusercontent.com/Nixtla/neuralforecast/main/nbs/imgs_indx/logo_new.png)

## Neural 🧠 Forecast

### User friendly state-of-the-art neural forecasting models

**NeuralForecast** offers a large collection of neural forecasting models focusing on their performance, usability, and robustness. The models range from classic networks like RNNs to the latest transformers: `MLP`, `LSTM`, `GRU`, `RNN`, `TCN`, `TimesNet`, `BiTCN`, `DeepAR`, `NBEATS`, `NBEATSx`, `NHITS`, `TiDE`, `DeepNPTS`, `TSMixer`, `TSMixerx`, `MLPMultivariate`, `DLinear`, `NLinear`, `TFT`, `Informer`, `AutoFormer`, `FedFormer`, `PatchTST`, `iTransformer`, `StemGNN`, and `TimeLLM`.

## Installation

You can install `NeuralForecast` with:

```
pip install neuralforecast
```

or

```
conda install -c conda-forge neuralforecast
```

Vist our [Installation Guide](https://nixtlaverse.nixtla.io/neuralforecast/docs/getting-started/installation.html) for further details.

## Quick Start

**Minimal Example**

```
from neuralforecast import NeuralForecast
from neuralforecast.models import NBEATS
from neuralforecast.utils import AirPassengersDF

nf = NeuralForecast(
    models = [NBEATS(input_size=24, h=12, max_steps=100)],
    freq = 'ME'
)

nf.fit(df=AirPassengersDF)
nf.predict()
```

**Get Started with this [quick guide](https://nixtlaverse.nixtla.io/neuralforecast/docs/getting-started/quickstart.html).**

## Why?

There is a shared belief in Neural forecasting methods' capacity to improve forecasting pipeline's accuracy and efficiency.

Unfortunately, available implementations and published research are yet to realize neural networks' potential. They are hard to use and continuously fail to improve over statistical methods while being computationally prohibitive. For this reason, we created `NeuralForecast`, a library favoring proven accurate and efficient models focusing on their usability.

## Features

- Fast and accurate implementations of more than 30 state-of-the-art models. See the entire [collection here](https://nixtlaverse.nixtla.io/neuralforecast/docs/capabilities/overview.html).
- Support for exogenous variables and static covariates.
- Interpretability methods for trend, seasonality and exogenous components.
- Probabilistic Forecasting with adapters for quantile losses and parametric distributions.
- Train and Evaluation Losses with scale-dependent, percentage and scale independent errors, and parametric likelihoods.
- Automatic Model Selection with distributed automatic hyperparameter tuning.
- Familiar sklearn syntax: `.fit` and `.predict`.

## Highlights

- Official `NHITS` implementation, published at AAAI 2023. See [paper](https://ojs.aaai.org/index.php/AAAI/article/view/25854) and [experiments](https://github.com/Nixtla/neuralforecast/tree/main/experiments).
- Official `NBEATSx` implementation, published at the International Journal of Forecasting. See [paper](https://www.sciencedirect.com/science/article/pii/S0169207022000413).
- Unified with `StatsForecast`, `MLForecast`, and `HierarchicalForecast` interface `NeuralForecast().fit(Y_df).predict()`, inputs and outputs.
- Built-in integrations with `utilsforecast` and `coreforecast` for visualization and data-wrangling efficient methods.
- Integrations with `Ray` and `Optuna` for automatic hyperparameter optimization.
- Predict with little to no history using Transfer learning. Check the experiments [here](https://github.com/Nixtla/transfer-learning-time-series).

Missing something? Please open an issue or write us in

## Examples and Guides

The [documentation page](https://nixtlaverse.nixtla.io/neuralforecast/docs/getting-started/introduction.html) contains all the examples and tutorials.

📈 [Automatic Hyperparameter Optimization](https://nixtlaverse.nixtla.io/neuralforecast/docs/capabilities/hyperparameter_tuning.html): Easy and Scalable Automatic Hyperparameter Optimization with `Auto` models on `Ray` or `Optuna`.

🌡️ [Exogenous Regressors](https://nixtlaverse.nixtla.io/neuralforecast/docs/capabilities/exogenous_variables.html): How to incorporate static or temporal exogenous covariates like weather or prices.

🔌 [Transformer Models](https://nixtlaverse.nixtla.io/neuralforecast/docs/tutorials/longhorizon_transformers.html): Learn how to forecast with many state-of-the-art Transformers models.

👑 [Hierarchical Forecasting](https://nixtlaverse.nixtla.io/neuralforecast/docs/tutorials/hierarchical_forecasting.html): forecast series with very few non-zero observations.

👩🔬 [Add Your Own Model](https://nixtlaverse.nixtla.io/neuralforecast/docs/tutorials/adding_models.html): Learn how to add a new model to the library.

## Models

See the entire [collection here](https://nixtlaverse.nixtla.io/neuralforecast/docs/capabilities/overview.html).

Missing a model? Please open an issue or write us in

## How to contribute

If you wish to contribute to the project, please refer to our [contribution guidelines](https://github.com/Nixtla/neuralforecast/blob/main/CONTRIBUTING.md).

## References

This work is highly influenced by the fantastic work of previous contributors and other scholars on the neural forecasting methods presented here. We want to highlight the work of [Boris Oreshkin](https://arxiv.org/abs/1905.10437), [Slawek Smyl](https://www.sciencedirect.com/science/article/pii/S0169207019301153), [Bryan Lim](https://www.sciencedirect.com/science/article/pii/S0169207021000637), and [David Salinas](https://arxiv.org/abs/1704.04110). We refer to [Benidis et al.](https://arxiv.org/abs/2004.10240) for a comprehensive survey of neural forecasting methods.

## 🙏 How to cite

If you enjoy or benefit from using these Python implementations, a citation to the repository will be greatly appreciated.

```
@misc{olivares2022library_neuralforecast,
    author={Kin G. Olivares and
            Cristian Challú and
            Azul Garza and
            Max Mergenthaler Canseco and
            Artur Dubrawski},
    title = {{NeuralForecast}: User friendly state-of-the-art neural forecasting models.},
    year={2022},
    howpublished={{PyCon} Salt Lake City, Utah, US 2022},
    url={https://github.com/Nixtla/neuralforecast}
}
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

| [![[Image 11.jpg|azul]]   <sub><b>azul</b></sub>](https://github.com/AzulGarza)   [💻](https://github.com/Nixtla/neuralforecast/commits?author=AzulGarza "Code") | [![[Image 12.jpg|Cristian Challu]]   <sub><b>Cristian Challu</b></sub>](https://github.com/cchallu)   [💻](https://github.com/Nixtla/neuralforecast/commits?author=cchallu "Code") | [![[Image 25.png|José Morales]]   <sub><b>José Morales</b></sub>](https://github.com/jmoralez)   [💻](https://github.com/Nixtla/neuralforecast/commits?author=jmoralez "Code") | [![[Image 13.jpg|mergenthaler]]   <sub><b>mergenthaler</b></sub>](https://github.com/mergenthaler)   [📖](https://github.com/Nixtla/neuralforecast/commits?author=mergenthaler "Documentation") [💻](https://github.com/Nixtla/neuralforecast/commits?author=mergenthaler "Code") | [![[Image 26.png|Kin]]   <sub><b>Kin</b></sub>](https://github.com/kdgutier)   [💻](https://github.com/Nixtla/neuralforecast/commits?author=kdgutier "Code") [🐛](https://github.com/Nixtla/neuralforecast/issues?q=author%3Akdgutier "Bug reports") [🔣](#data-kdgutier "Data") | [![[Image 14.jpg|Greg DeVos]]   <sub><b>Greg DeVos</b></sub>](https://github.com/gdevos010)   [🤔](#ideas-gdevos010 "Ideas, Planning, & Feedback") | [![[Image 15.jpg|Alejandro]]   <sub><b>Alejandro</b></sub>](https://github.com/alejandroxag)   [💻](https://github.com/Nixtla/neuralforecast/commits?author=alejandroxag "Code") |
| --- | --- | --- | --- | --- | --- | --- |
| [![[Image 16.jpg|stefanialvs]]   <sub><b>stefanialvs</b></sub>](http://lavattiata.com/)   [🎨](#design-stefanialvs "Design") | [![[Image 17.jpg|Ikko Ashimine]]   <sub><b>Ikko Ashimine</b></sub>](https://bandism.net/)   [🐛](https://github.com/Nixtla/neuralforecast/issues?q=author%3Aeltociear "Bug reports") | [![[Image 27.png|vglaucus]]   <sub><b>vglaucus</b></sub>](https://github.com/vglaucus)   [🐛](https://github.com/Nixtla/neuralforecast/issues?q=author%3Avglaucus "Bug reports") | [![[Image 28.png|Pietro Monticone]]   <sub><b>Pietro Monticone</b></sub>](https://github.com/pitmonticone)   [🐛](https://github.com/Nixtla/neuralforecast/issues?q=author%3Apitmonticone "Bug reports") |

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!