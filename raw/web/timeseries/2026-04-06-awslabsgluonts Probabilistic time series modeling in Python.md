---
source_type: web
title: "awslabs/gluonts: Probabilistic time series modeling in Python"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://github.com/awslabs/gluonts"
published: 
created: 2026-04-06
description: "Probabilistic time series modeling in Python. Contribute to awslabs/gluonts development by creating an account on GitHub."
tags:
  - 
  - "clippings"
---

[![[raw/assets/attachments/timeseries/Image 3.svg]]](https://camo.githubusercontent.com/b3c638ce41cbff7d65a4e44e6ed98afec7d3d00945e6f7a7445489c51eef5e5f/68747470733a2f2f74732e676c756f6e2e61692f6465762f5f7374617469632f676c756f6e74732e737667)

## GluonTS - Probabilistic Time Series Modeling in Python

**📢 BREAKING NEWS**: We released **Chronos**, a suite of pretrained models for zero-shot time series forecasting. Chronos can generate accurate probabilistic predictions for new time series not seen during training. Check it out [here](https://github.com/amazon-science/chronos-forecasting)!

GluonTS is a Python package for probabilistic time series modeling, focusing on deep learning based models, based on [PyTorch](https://pytorch.org/) and [MXNet](https://mxnet.apache.org/).

## Installation

GluonTS requires Python 3.7 or newer, and the easiest way to install it is via `pip`:

```
# install with support for torch models
pip install "gluonts[torch]"

# install with support for mxnet models
pip install "gluonts[mxnet]"
```

See the [documentation](https://ts.gluon.ai/stable/getting_started/install.html) for more info on how GluonTS can be installed.

## Simple Example

To illustrate how to use GluonTS, we train a DeepAR-model and make predictions using the airpassengers dataset. The dataset consists of a single time series of monthly passenger numbers between 1949 and 1960. We train the model on the first nine years and make predictions for the remaining three years.

```
import pandas as pd
import matplotlib.pyplot as plt

from gluonts.dataset.pandas import PandasDataset
from gluonts.dataset.split import split
from gluonts.torch import DeepAREstimator

# Load data from a CSV file into a PandasDataset
df = pd.read_csv(
    "https://raw.githubusercontent.com/AileenNielsen/"
    "TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv",
    index_col=0,
    parse_dates=True,
)
dataset = PandasDataset(df, target="#Passengers")

# Split the data for training and testing
training_data, test_gen = split(dataset, offset=-36)
test_data = test_gen.generate_instances(prediction_length=12, windows=3)

# Train the model and make predictions
model = DeepAREstimator(
    prediction_length=12, freq="M", trainer_kwargs={"max_epochs": 5}
).train(training_data)

forecasts = list(model.predict(test_data.input))

# Plot predictions
plt.plot(df["1954":], color="black")
for forecast in forecasts:
  forecast.plot()
plt.legend(["True values"], loc="upper left", fontsize="xx-large")
plt.show()
```

[![[train-test]](https://camo.githubusercontent.com/7eb48dc80a3b10f9c6803165fb789ec9088f2b10af31a89fe161d2bc07918d4d/68747470733a2f2f74732e676c756f6e2e61692f7374617469632f524541444d452f666f726563617374732e706e67)](https://camo.githubusercontent.com/7eb48dc80a3b10f9c6803165fb789ec9088f2b10af31a89fe161d2bc07918d4d/68747470733a2f2f74732e676c756f6e2e61692f7374617469632f524541444d452f666f726563617374732e706e67)

Note, the forecasts are displayed in terms of a probability distribution and the shaded areas represent the 50% and 90% prediction intervals.

## Contributing

If you wish to contribute to the project, please refer to our [contribution guidelines](https://github.com/awslabs/gluonts/tree/dev/CONTRIBUTING.md).

## Citing

If you use GluonTS in a scientific publication, we encourage you to add the following references to the related papers, in addition to any model-specific references that are relevant for your work:

```
@article{gluonts_jmlr,
  author  = {Alexander Alexandrov and Konstantinos Benidis and Michael Bohlke-Schneider
    and Valentin Flunkert and Jan Gasthaus and Tim Januschowski and Danielle C. Maddix
    and Syama Rangapuram and David Salinas and Jasper Schulz and Lorenzo Stella and
    Ali Caner Türkmen and Yuyang Wang},
  title   = {{GluonTS: Probabilistic and Neural Time Series Modeling in Python}},
  journal = {Journal of Machine Learning Research},
  year    = {2020},
  volume  = {21},
  number  = {116},
  pages   = {1-6},
  url     = {http://jmlr.org/papers/v21/19-820.html}
}
```
```
@article{gluonts_arxiv,
  author  = {Alexandrov, A. and Benidis, K. and Bohlke-Schneider, M. and
    Flunkert, V. and Gasthaus, J. and Januschowski, T. and Maddix, D. C.
    and Rangapuram, S. and Salinas, D. and Schulz, J. and Stella, L. and
    Türkmen, A. C. and Wang, Y.},
  title   = {{GluonTS: Probabilistic Time Series Modeling in Python}},
  journal = {arXiv preprint arXiv:1906.05264},
  year    = {2019}
}
```

## Links

### Documentation

### References

- [JMLR MLOSS Paper](http://www.jmlr.org/papers/v21/19-820.html)
- [ArXiv Paper](https://arxiv.org/abs/1906.05264)
- [Collected Papers from the group behind GluonTS](https://github.com/awslabs/gluonts/tree/dev/REFERENCES.md): a bibliography.

### Tutorials and Workshops

- [Tutorial at IJCAI 2021 (with videos)](https://lovvge.github.io/Forecasting-Tutorial-IJCAI-2021/) with [YouTube link](https://youtu.be/AB3I9pdT46c).
- [Tutorial at WWW 2020 (with videos)](https://lovvge.github.io/Forecasting-Tutorial-WWW-2020/)
- [Tutorial at SIGMOD 2019](https://lovvge.github.io/Forecasting-Tutorials/SIGMOD-2019/)
- [Tutorial at KDD 2019](https://lovvge.github.io/Forecasting-Tutorial-KDD-2019/)
- [Tutorial at VLDB 2018](https://lovvge.github.io/Forecasting-Tutorial-VLDB-2018/)
- [Neural Time Series with GluonTS](https://youtu.be/beEJMIt9xJ8)
- [International Symposium of Forecasting: Deep Learning for Forecasting workshop](https://lostella.github.io/ISF-2020-Deep-Learning-Workshop/)