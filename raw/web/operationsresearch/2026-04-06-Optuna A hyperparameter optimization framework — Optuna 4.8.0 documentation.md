---
source_type: web
title: "Optuna: A hyperparameter optimization framework — Optuna 4.8.0 documentation"
author: 
created_at: 2026-04-06
topics:
  - 运筹优化
status: inbox
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://optuna.readthedocs.io/en/stable/index.html"
published_at: null
related_concepts: []
---

[![OPTUNA](https://raw.githubusercontent.com/optuna/optuna/master/docs/image/optuna-logo.png)](https://raw.githubusercontent.com/optuna/optuna/master/docs/image/optuna-logo.png)

## Optuna: A hyperparameter optimization framework

*Optuna* is an automatic hyperparameter optimization software framework, particularly designed for machine learning. It features an imperative, *define-by-run* style user API. Thanks to our *define-by-run* API, the code written with Optuna enjoys high modularity, and the user of Optuna can dynamically construct the search spaces for the hyperparameters.

## Key Features

Optuna has modern functionalities as follows:

- [Lightweight, versatile, and platform agnostic architecture](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/001_first.html)
	- Handle a wide variety of tasks with a simple installation that has few requirements.
- [Pythonic search spaces](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html)
	- Define search spaces using familiar Python syntax including conditionals and loops.
- [Efficient optimization algorithms](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/003_efficient_optimization_algorithms.html)
	- Adopt state-of-the-art algorithms for sampling hyperparameters and efficiently pruning unpromising trials.
- [Easy parallelization](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html)
	- Scale studies to tens or hundreds of workers with little or no changes to the code.
- [Quick visualization](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/005_visualization.html)
	- Inspect optimization histories from a variety of plotting functions.

## Basic Concepts

We use the terms *study* and *trial* as follows:

- Study: optimization based on an objective function
- Trial: a single execution of the objective function

Please refer to sample code below. The goal of a *study* is to find out the optimal set of hyperparameter values (e.g., `classifier` and `svm_c`) through multiple *trials* (e.g., `n_trials=100`). Optuna is a framework designed for the automation and the acceleration of the optimization *studies*.

```python
import ...

# Define an objective function to be minimized.
def objective(trial):

    # Invoke suggest methods of a Trial object to generate hyperparameters.
    regressor_name = trial.suggest_categorical('classifier', ['SVR', 'RandomForest'])
    if regressor_name == 'SVR':
        svr_c = trial.suggest_float('svr_c', 1e-10, 1e10, log=True)
        regressor_obj = sklearn.svm.SVR(C=svr_c)
    else:
        rf_max_depth = trial.suggest_int('rf_max_depth', 2, 32)
        regressor_obj = sklearn.ensemble.RandomForestRegressor(max_depth=rf_max_depth)

    X, y = sklearn.datasets.fetch_california_housing(return_X_y=True)
    X_train, X_val, y_train, y_val = sklearn.model_selection.train_test_split(X, y, random_state=0)

    regressor_obj.fit(X_train, y_train)
    y_pred = regressor_obj.predict(X_val)

    error = sklearn.metrics.mean_squared_error(y_val, y_pred)

    return error  # An objective value linked with the Trial object.

study = optuna.create_study()  # Create a new study.
study.optimize(objective, n_trials=100)  # Invoke optimization of the objective function.
```

## Web Dashboard

[Optuna Dashboard](https://github.com/optuna/optuna-dashboard) is a real-time web dashboard for Optuna. You can check the optimization history, hyperparameter importance, etc. in graphs and tables. You don’t need to create a Python script to call [Optuna’s visualization](https://optuna.readthedocs.io/en/stable/reference/visualization/index.html) functions. Feature requests and bug reports are welcome!

![https://user-images.githubusercontent.com/5564044/204975098-95c2cb8c-0fb5-4388-abc4-da32f56cb4e5.gif](https://user-images.githubusercontent.com/5564044/204975098-95c2cb8c-0fb5-4388-abc4-da32f56cb4e5.gif)

`optuna-dashboard` can be installed via pip:

```
$ pip install optuna-dashboard
```

Tip

Please check out the [getting started](https://optuna-dashboard.readthedocs.io/en/stable/getting-started.html) section of Optuna Dashboard’s official documentation.

## OptunaHub

[OptunaHub](https://hub.optuna.org/) is a feature-sharing platform for Optuna. You can use the registered features and publish your packages. For more details, please refer to [the official documentation](https://optuna.github.io/optunahub/).

[![_images/optunahub-introduction.png](https://optuna.readthedocs.io/en/stable/_images/optunahub-introduction.png)](https://hub.optuna.org/)

`optunahub` can be installed via pip:

```
$ pip install optunahub
```

## Communication

- [GitHub Discussions](https://github.com/optuna/optuna/discussions) for questions.
- [GitHub Issues](https://github.com/optuna/optuna/issues) for bug reports and feature requests.

## Contribution

Any contributions to Optuna are welcome! When you send a pull request, please follow the [contribution guide](https://github.com/optuna/optuna/blob/master/CONTRIBUTING.md).

## License

MIT License (see [LICENSE](https://github.com/optuna/optuna/blob/master/LICENSE)).

Optuna uses the codes from SciPy and fdlibm projects (see [Third-party License](https://optuna.readthedocs.io/en/stable/license_thirdparty.html)).

## Reference

Takuya Akiba, Shotaro Sano, Toshihiko Yanase, Takeru Ohta, and Masanori Koyama. 2019. Optuna: A Next-generation Hyperparameter Optimization Framework. In KDD ([arXiv](https://arxiv.org/abs/1907.10902)).

Contents:

- [Installation](https://optuna.readthedocs.io/en/stable/installation.html)
- [Tutorial](https://optuna.readthedocs.io/en/stable/tutorial/index.html)
	- [Key Features](https://optuna.readthedocs.io/en/stable/tutorial/index.html#key-features)
		- [Recipes](https://optuna.readthedocs.io/en/stable/tutorial/index.html#recipes)
- [API Reference](https://optuna.readthedocs.io/en/stable/reference/index.html)
	- [optuna](https://optuna.readthedocs.io/en/stable/reference/optuna.html)
		- [optuna.artifacts](https://optuna.readthedocs.io/en/stable/reference/artifacts.html)
		- [optuna.cli](https://optuna.readthedocs.io/en/stable/reference/cli.html)
		- [optuna.distributions](https://optuna.readthedocs.io/en/stable/reference/distributions.html)
		- [optuna.exceptions](https://optuna.readthedocs.io/en/stable/reference/exceptions.html)
		- [optuna.importance](https://optuna.readthedocs.io/en/stable/reference/importance.html)
		- [optuna.integration](https://optuna.readthedocs.io/en/stable/reference/integration.html)
		- [optuna.logging](https://optuna.readthedocs.io/en/stable/reference/logging.html)
		- [optuna.pruners](https://optuna.readthedocs.io/en/stable/reference/pruners.html)
		- [optuna.samplers](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html)
		- [optuna.search\_space](https://optuna.readthedocs.io/en/stable/reference/search_space.html)
		- [optuna.storages](https://optuna.readthedocs.io/en/stable/reference/storages.html)
		- [optuna.study](https://optuna.readthedocs.io/en/stable/reference/study.html)
		- [optuna.terminator](https://optuna.readthedocs.io/en/stable/reference/terminator.html)
		- [optuna.trial](https://optuna.readthedocs.io/en/stable/reference/trial.html)
		- [optuna.visualization](https://optuna.readthedocs.io/en/stable/reference/visualization/index.html)
- [FAQ](https://optuna.readthedocs.io/en/stable/faq.html)
	- [Can I use Optuna with X? (where X is your favorite ML library)](https://optuna.readthedocs.io/en/stable/faq.html#can-i-use-optuna-with-x-where-x-is-your-favorite-ml-library)
		- [How to define objective functions that have own arguments?](https://optuna.readthedocs.io/en/stable/faq.html#how-to-define-objective-functions-that-have-own-arguments)
		- [Can I use Optuna without remote RDB servers?](https://optuna.readthedocs.io/en/stable/faq.html#can-i-use-optuna-without-remote-rdb-servers)
		- [How can I save and resume studies?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-save-and-resume-studies)
		- [How to suppress log messages of Optuna?](https://optuna.readthedocs.io/en/stable/faq.html#how-to-suppress-log-messages-of-optuna)
		- [How to save machine learning models trained in objective functions?](https://optuna.readthedocs.io/en/stable/faq.html#how-to-save-machine-learning-models-trained-in-objective-functions)
		- [How can I obtain reproducible optimization results?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-obtain-reproducible-optimization-results)
		- [How are exceptions from trials handled?](https://optuna.readthedocs.io/en/stable/faq.html#how-are-exceptions-from-trials-handled)
		- [How are NaNs returned by trials handled?](https://optuna.readthedocs.io/en/stable/faq.html#how-are-nans-returned-by-trials-handled)
		- [What happens when I dynamically alter a search space?](https://optuna.readthedocs.io/en/stable/faq.html#what-happens-when-i-dynamically-alter-a-search-space)
		- [How can I use two GPUs for evaluating two trials simultaneously?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-use-two-gpus-for-evaluating-two-trials-simultaneously)
		- [How can I test my objective functions?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-test-my-objective-functions)
		- [How do I avoid running out of memory (OOM) when optimizing studies?](https://optuna.readthedocs.io/en/stable/faq.html#how-do-i-avoid-running-out-of-memory-oom-when-optimizing-studies)
		- [How can I output a log only when the best value is updated?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-output-a-log-only-when-the-best-value-is-updated)
		- [How do I suggest variables which represent the proportion, that is, are in accordance with Dirichlet distribution?](https://optuna.readthedocs.io/en/stable/faq.html#how-do-i-suggest-variables-which-represent-the-proportion-that-is-are-in-accordance-with-dirichlet-distribution)
		- [How can I optimize a model with some constraints?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-optimize-a-model-with-some-constraints)
		- [How can I parallelize optimization?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-parallelize-optimization)
		- [How can I solve the error that occurs when performing parallel optimization with SQLite3?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-solve-the-error-that-occurs-when-performing-parallel-optimization-with-sqlite3)
		- [Can I monitor trials and make them failed automatically when they are killed unexpectedly?](https://optuna.readthedocs.io/en/stable/faq.html#can-i-monitor-trials-and-make-them-failed-automatically-when-they-are-killed-unexpectedly)
		- [How can I deal with permutation as a parameter?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-deal-with-permutation-as-a-parameter)
		- [How can I ignore duplicated samples?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-ignore-duplicated-samples)
		- [How can I delete all the artifacts uploaded to a study?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-delete-all-the-artifacts-uploaded-to-a-study)
		- [Can I specify parameter starting points before optimization?](https://optuna.readthedocs.io/en/stable/faq.html#can-i-specify-parameter-starting-points-before-optimization)
		- [How can I resolve case sensitivity issues with MySQL?](https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-resolve-case-sensitivity-issues-with-mysql)