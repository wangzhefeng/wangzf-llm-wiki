---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: null
source_type: web
status: inbox
tags:
- null
- clippings
title: 'Ray Tune: Hyperparameter Tuning — Ray 2.54.1'
source_url: https://docs.ray.io/en/latest/tune/index.html
published_at: null
related_concepts: []
topics:
  - machine-learning
  - 机器学习理论
---

## Ray Tune: Hyperparameter Tuning

[![[tune_overview.png|../_images/tune_overview.png]]](https://docs.ray.io/en/latest/_images/tune_overview.png)

Tune is a Python library for experiment execution and hyperparameter tuning at any scale. You can tune your favorite machine learning framework ([PyTorch](https://docs.ray.io/en/latest/tune/examples/tune-pytorch-cifar.html#tune-pytorch-cifar-ref), [XGBoost](https://docs.ray.io/en/latest/tune/examples/tune-xgboost.html#tune-xgboost-ref), [TensorFlow and Keras](https://docs.ray.io/en/latest/tune/examples/tune_mnist_keras.html), and [more](https://docs.ray.io/en/latest/tune/examples/index.html)) by running state of the art algorithms such as [Population Based Training (PBT)](https://docs.ray.io/en/latest/tune/api/schedulers.html#tune-scheduler-pbt) and [HyperBand/ASHA](https://docs.ray.io/en/latest/tune/api/schedulers.html#tune-scheduler-hyperband). Tune further integrates with a wide range of additional hyperparameter optimization tools, including [Ax](https://docs.ray.io/en/latest/tune/examples/ax_example.html), [BayesOpt](https://docs.ray.io/en/latest/tune/examples/bayesopt_example.html), [BOHB](https://docs.ray.io/en/latest/tune/examples/bohb_example.html), [Nevergrad](https://docs.ray.io/en/latest/tune/examples/nevergrad_example.html), and [Optuna](https://docs.ray.io/en/latest/tune/examples/optuna_example.html).

**Click on the following tabs to see code examples for various machine learning frameworks**:

To run this example, install the following: `pip install "ray[tune]"`.

In this quick-start example you `minimize` a simple function of the form `f(x) = a**2 + b`, our `objective` function. The closer `a` is to zero and the smaller `b` is, the smaller the total value of `f(x)`. We will define a so-called `search space` for `a` and `b` and let Ray Tune explore the space for good values.

```python
from ray import tune

def objective(config):  # ①
    score = config["a"] ** 2 + config["b"]
    return {"score": score}

search_space = {  # ②
    "a": tune.grid_search([0.001, 0.01, 0.1, 1.0]),
    "b": tune.choice([1, 2, 3]),
}

tuner = tune.Tuner(objective, param_space=search_space)  # ③

results = tuner.fit()
print(results.get_best_result(metric="score", mode="min").config)
```

① Define an objective function.

② Define a search space.

③ Start a Tune run and print the best result.

To tune your Keras models with Hyperopt, you wrap your model in an objective function whose `config` you can access for selecting hyperparameters. In the example below we only tune the `activation` parameter of the first layer of the model, but you can tune any parameter of the model you want. After defining the search space, you can simply initialize the `HyperOptSearch` object and pass it to `run`. It’s important to tell Ray Tune which metric you want to optimize and whether you want to maximize or minimize it.

```python
from ray import tune
from ray.tune.search.hyperopt import HyperOptSearch
import keras

def objective(config):  # ①
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(784, activation=config["activation"]))
    model.add(keras.layers.Dense(10, activation="softmax"))

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    # model.fit(...)
    # loss, accuracy = model.evaluate(...)
    return {"accuracy": accuracy}

search_space = {"activation": tune.choice(["relu", "tanh"])}  # ②
algo = HyperOptSearch()

tuner = tune.Tuner(  # ③
    objective,
    tune_config=tune.TuneConfig(
        metric="accuracy",
        mode="max",
        search_alg=algo,
    ),
    param_space=search_space,
)
results = tuner.fit()
```

① Wrap a Keras model in an objective function.

② Define a search space and initialize the search algorithm.

③ Start a Tune run that maximizes accuracy.

To tune your PyTorch models with Optuna, you wrap your model in an objective function whose `config` you can access for selecting hyperparameters. In the example below we only tune the `momentum` and learning rate (`lr`) parameters of the model’s optimizer, but you can tune any other model parameter you want. After defining the search space, you can simply initialize the `OptunaSearch` object and pass it to `run`. It’s important to tell Ray Tune which metric you want to optimize and whether you want to maximize or minimize it. We stop tuning this training run after `5` iterations, but you can easily define other stopping rules as well.

```python
import torch
from ray import tune
from ray.tune.search.optuna import OptunaSearch

def objective(config):  # ①
    train_loader, test_loader = load_data()  # Load some data
    model = ConvNet().to("cpu")  # Create a PyTorch conv net
    optimizer = torch.optim.SGD(  # Tune the optimizer
        model.parameters(), lr=config["lr"], momentum=config["momentum"]
    )

    while True:
        train_epoch(model, optimizer, train_loader)  # Train the model
        acc = test(model, test_loader)  # Compute test accuracy
        tune.report({"mean_accuracy": acc})  # Report to Tune

search_space = {"lr": tune.loguniform(1e-4, 1e-2), "momentum": tune.uniform(0.1, 0.9)}
algo = OptunaSearch()  # ②

tuner = tune.Tuner(  # ③
    objective,
    tune_config=tune.TuneConfig(
        metric="mean_accuracy",
        mode="max",
        search_alg=algo,
    ),
    run_config=tune.RunConfig(
        stop={"training_iteration": 5},
    ),
    param_space=search_space,
)
results = tuner.fit()
print("Best config is:", results.get_best_result().config)
```

① Wrap a PyTorch model in an objective function.

② Define a search space and initialize the search algorithm.

③ Start a Tune run that maximizes mean accuracy and stops after 5 iterations.

With Tune you can also launch a multi-node [distributed hyperparameter sweep](https://docs.ray.io/en/latest/tune/tutorials/tune-distributed.html#tune-distributed-ref) in less than 10 lines of code. And you can move your models from training to serving on the same infrastructure with [Ray Serve](https://docs.ray.io/en/latest/serve/index.html).

## Why choose Tune?

There are many other hyperparameter optimization libraries out there. If you’re new to Tune, you’re probably wondering, “what makes Tune different?”

## Projects using Tune

Here are some of the popular open source repositories and research projects that leverage Tune. Feel free to submit a pull-request adding (or requesting a removal!) of a listed project.

- [Softlearning](https://github.com/rail-berkeley/softlearning): Softlearning is a reinforcement learning framework for training maximum entropy policies in continuous domains. Includes the official implementation of the Soft Actor-Critic algorithm.
- [Flambe](https://github.com/asappresearch/flambe): An ML framework to accelerate research and its path to production. See [flambe.ai](https://flambe.ai/).
- [Population Based Augmentation](https://github.com/arcelien/pba): Population Based Augmentation (PBA) is an algorithm that quickly and efficiently learns data augmentation functions for neural network training. PBA matches state-of-the-art results on CIFAR with one thousand times less compute.
- [Fast AutoAugment by Kakao](https://github.com/kakaobrain/fast-autoaugment): Fast AutoAugment (Accepted at NeurIPS 2019) learns augmentation policies using a more efficient search strategy based on density matching.
- [Allentune](https://github.com/allenai/allentune): Hyperparameter Search for AllenNLP from AllenAI.
- [machinable](https://github.com/frthjf/machinable): A modular configuration system for machine learning research. See [machinable.org](https://machinable.org/).
- [NeuroCard](https://github.com/neurocard/neurocard): NeuroCard (Accepted at VLDB 2021) is a neural cardinality estimator for multi-table join queries. It uses state of the art deep density models to learn correlations across relational database tables.

## Citing Tune

If Tune helps you in your academic research, you are encouraged to cite [our paper](https://arxiv.org/abs/1807.05118). Here is an example bibtex:

```tex
@article{liaw2018tune,
    title={Tune: A Research Platform for Distributed Model Selection and Training},
    author={Liaw, Richard and Liang, Eric and Nishihara, Robert
            and Moritz, Philipp and Gonzalez, Joseph E and Stoica, Ion},
    journal={arXiv preprint arXiv:1807.05118},
    year={2018}
}
```