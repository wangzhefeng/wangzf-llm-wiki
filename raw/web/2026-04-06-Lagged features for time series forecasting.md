---
source_type: web
title: "Lagged features for time series forecasting"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html#sphx-glr-auto-examples-applications-plot-time-series-lagged-features-py"
published: 
created: 2026-04-06
description: "This example demonstrates how Polars-engineered lagged features can be used for time series forecasting with HistGradientBoostingRegressor on the Bike Sharing Demand dataset. See the example on Tim..."
tags:
  - 
  - "clippings"
---

Note

to download the full example code or to run this example in your browser via JupyterLite or Binder.

## Lagged features for time series forecasting

This example demonstrates how Polars-engineered lagged features can be used for time series forecasting with [`HistGradientBoostingRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html#sklearn.ensemble.HistGradientBoostingRegressor "sklearn.ensemble.HistGradientBoostingRegressor") on the Bike Sharing Demand dataset.

See the example on [Time-related feature engineering](https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html#sphx-glr-auto-examples-applications-plot-cyclical-feature-engineering-py) for some data exploration on this dataset and a demo on periodic feature engineering.

```python
# Authors: The scikit-learn developers
# SPDX-License-Identifier: BSD-3-Clause
```

## Analyzing the Bike Sharing Demand dataset

We start by loading the data from the OpenML repository as a raw parquet file to illustrate how to work with an arbitrary parquet file instead of hiding this step in a convenience tool such as `sklearn.datasets.fetch_openml`.

The URL of the parquet file can be found in the JSON description of the Bike Sharing Demand dataset with id 44063 on openml.org ([https://openml.org/search?type=data&status=active&id=44063](https://openml.org/search?type=data&status=active&id=44063)).

The `sha256` hash of the file is also provided to ensure the integrity of the downloaded file.

```python
import numpy as np
import polars as pl

from sklearn.datasets import fetch_file

pl.Config.set_fmt_str_lengths(20)

bike_sharing_data_file = fetch_file(
    "https://data.openml.org/datasets/0004/44063/dataset_44063.pq",
    sha256="d120af76829af0d256338dc6dd4be5df4fd1f35bf3a283cab66a51c1c6abd06a",
)
bike_sharing_data_file
```

```
PosixPath('/home/circleci/scikit_learn_data/data.openml.org/datasets_0004_44063/dataset_44063.pq')
```

We load the parquet file with Polars for feature engineering. Polars automatically caches common subexpressions which are reused in multiple expressions (like `pl.col("count").shift(1)` below). See [https://docs.pola.rs/user-guide/lazy/optimizations/](https://docs.pola.rs/user-guide/lazy/optimizations/) for more information.

```python
df = pl.read_parquet(bike_sharing_data_file)
```

Next, we take a look at the statistical summary of the dataset so that we can better understand the data that we are working with.

```python
import polars.selectors as cs

summary = df.select(cs.numeric()).describe()
summary
```

shape: (9, 8)

| statistic | month | hour | temp | feel\_temp | humidity | windspeed | count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| str | f64 | f64 | f64 | f64 | f64 | f64 | f64 |
| "count" | 17379.0 | 17379.0 | 17379.0 | 17379.0 | 17379.0 | 17379.0 | 17379.0 |
| "null\_count" | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| "mean" | 6.537775 | 11.546752 | 20.376474 | 23.788755 | 0.627229 | 12.73654 | 189.463088 |
| "std" | 3.438776 | 6.914405 | 7.894801 | 8.592511 | 0.19293 | 8.196795 | 181.387599 |
| "min" | 1.0 | 0.0 | 0.82 | 0.0 | 0.0 | 0.0 | 1.0 |
| "25%" | 4.0 | 6.0 | 13.94 | 16.665 | 0.48 | 7.0015 | 40.0 |
| "50%" | 7.0 | 12.0 | 20.5 | 24.24 | 0.63 | 12.998 | 142.0 |
| "75%" | 10.0 | 18.0 | 27.06 | 31.06 | 0.78 | 16.9979 | 281.0 |
| "max" | 12.0 | 23.0 | 41.0 | 50.0 | 1.0 | 56.9969 | 977.0 |

  
  

Let us look at the count of the seasons `"fall"`, `"spring"`, `"summer"` and `"winter"` present in the dataset to confirm they are balanced.

```python
import matplotlib.pyplot as plt

df["season"].value_counts()
```

shape: (4, 2)

| season | count |
| --- | --- |
| cat | u32 |
| "0" | 4496 |
| "3" | 4232 |
| "1" | 4242 |
| "2" | 4409 |

  
  

## Generating Polars-engineered lagged features

Let’s consider the problem of predicting the demand at the next hour given past demands. Since the demand is a continuous variable, one could intuitively use any regression model. However, we do not have the usual `(X_train, y_train)` dataset. Instead, we just have the `y_train` demand data sequentially organized by time.

```python
lagged_df = df.select(
    "count",
    *[pl.col("count").shift(i).alias(f"lagged_count_{i}h") for i in [1, 2, 3]],
    lagged_count_1d=pl.col("count").shift(24),
    lagged_count_1d_1h=pl.col("count").shift(24 + 1),
    lagged_count_7d=pl.col("count").shift(7 * 24),
    lagged_count_7d_1h=pl.col("count").shift(7 * 24 + 1),
    lagged_mean_24h=pl.col("count").shift(1).rolling_mean(24),
    lagged_max_24h=pl.col("count").shift(1).rolling_max(24),
    lagged_min_24h=pl.col("count").shift(1).rolling_min(24),
    lagged_mean_7d=pl.col("count").shift(1).rolling_mean(7 * 24),
    lagged_max_7d=pl.col("count").shift(1).rolling_max(7 * 24),
    lagged_min_7d=pl.col("count").shift(1).rolling_min(7 * 24),
)
lagged_df.tail(10)
```

shape: (10, 14)

| count | lagged\_count\_1h | lagged\_count\_2h | lagged\_count\_3h | lagged\_count\_1d | lagged\_count\_1d\_1h | lagged\_count\_7d | lagged\_count\_7d\_1h | lagged\_mean\_24h | lagged\_max\_24h | lagged\_min\_24h | lagged\_mean\_7d | lagged\_max\_7d | lagged\_min\_7d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| i64 | i64 | i64 | i64 | i64 | i64 | i64 | i64 | f64 | i64 | i64 | f64 | i64 | i64 |
| 247 | 203 | 224 | 157 | 160 | 169 | 70 | 135 | 93.5 | 224 | 1 | 67.732143 | 271 | 1 |
| 315 | 247 | 203 | 224 | 138 | 160 | 46 | 70 | 97.125 | 247 | 1 | 68.785714 | 271 | 1 |
| 214 | 315 | 247 | 203 | 133 | 138 | 33 | 46 | 104.5 | 315 | 1 | 70.386905 | 315 | 1 |
| 164 | 214 | 315 | 247 | 123 | 133 | 33 | 33 | 107.875 | 315 | 1 | 71.464286 | 315 | 1 |
| 122 | 164 | 214 | 315 | 125 | 123 | 26 | 33 | 109.583333 | 315 | 1 | 72.244048 | 315 | 1 |
| 119 | 122 | 164 | 214 | 102 | 125 | 26 | 26 | 109.458333 | 315 | 1 | 72.815476 | 315 | 1 |
| 89 | 119 | 122 | 164 | 72 | 102 | 18 | 26 | 110.166667 | 315 | 1 | 73.369048 | 315 | 1 |
| 90 | 89 | 119 | 122 | 47 | 72 | 23 | 18 | 110.875 | 315 | 1 | 73.791667 | 315 | 1 |
| 61 | 90 | 89 | 119 | 36 | 47 | 22 | 23 | 112.666667 | 315 | 1 | 74.190476 | 315 | 1 |
| 49 | 61 | 90 | 89 | 49 | 36 | 12 | 22 | 113.708333 | 315 | 1 | 74.422619 | 315 | 1 |

  
  

Watch out however, the first lines have undefined values because their own past is unknown. This depends on how much lag we used:

```python
lagged_df.head(10)
```

shape: (10, 14)

| count | lagged\_count\_1h | lagged\_count\_2h | lagged\_count\_3h | lagged\_count\_1d | lagged\_count\_1d\_1h | lagged\_count\_7d | lagged\_count\_7d\_1h | lagged\_mean\_24h | lagged\_max\_24h | lagged\_min\_24h | lagged\_mean\_7d | lagged\_max\_7d | lagged\_min\_7d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| i64 | i64 | i64 | i64 | i64 | i64 | i64 | i64 | f64 | i64 | i64 | f64 | i64 | i64 |
| 16 | null | null | null | null | null | null | null | null | null | null | null | null | null |
| 40 | 16 | null | null | null | null | null | null | null | null | null | null | null | null |
| 32 | 40 | 16 | null | null | null | null | null | null | null | null | null | null | null |
| 13 | 32 | 40 | 16 | null | null | null | null | null | null | null | null | null | null |
| 1 | 13 | 32 | 40 | null | null | null | null | null | null | null | null | null | null |
| 1 | 1 | 13 | 32 | null | null | null | null | null | null | null | null | null | null |
| 2 | 1 | 1 | 13 | null | null | null | null | null | null | null | null | null | null |
| 3 | 2 | 1 | 1 | null | null | null | null | null | null | null | null | null | null |
| 8 | 3 | 2 | 1 | null | null | null | null | null | null | null | null | null | null |
| 14 | 8 | 3 | 2 | null | null | null | null | null | null | null | null | null | null |

  
  

We can now separate the lagged features in a matrix `X` and the target variable (the counts to predict) in an array of the same first dimension `y`.

```python
lagged_df = lagged_df.drop_nulls()
X = lagged_df.drop("count")
y = lagged_df["count"]
print("X shape: {}\ny shape: {}".format(X.shape, y.shape))
```

```
X shape: (17210, 13)
y shape: (17210,)
```

## Naive evaluation of the next hour bike demand regression

Let’s randomly split our tabularized dataset to train a gradient boosting regression tree (GBRT) model and evaluate it using Mean Absolute Percentage Error (MAPE). If our model is aimed at forecasting (i.e., predicting future data from past data), we should not use training data that are ulterior to the testing data. In time series machine learning the “i.i.d” (independent and identically distributed) assumption does not hold true as the data points are not independent and have a temporal relationship.

```python
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = HistGradientBoostingRegressor().fit(X_train, y_train)
```

Taking a look at the performance of the model.

```python
from sklearn.metrics import mean_absolute_percentage_error

y_pred = model.predict(X_test)
mean_absolute_percentage_error(y_test, y_pred)
```

```
0.3889873516666431
```

## Proper next hour forecasting evaluation

Let’s use a proper evaluation splitting strategies that takes into account the temporal structure of the dataset to evaluate our model’s ability to predict data points in the future (to avoid cheating by reading values from the lagged features in the training set).

```python
from sklearn.model_selection import TimeSeriesSplit

ts_cv = TimeSeriesSplit(
    n_splits=3,  # to keep the notebook fast enough on common laptops
    gap=48,  # 2 days data gap between train and test
    max_train_size=10000,  # keep train sets of comparable sizes
    test_size=3000,  # for 2 or 3 digits of precision in scores
)
all_splits = list(ts_cv.split(X, y))
```

Training the model and evaluating its performance based on MAPE.

```python
train_idx, test_idx = all_splits[0]
X_train, X_test = X[train_idx, :], X[test_idx, :]
y_train, y_test = y[train_idx], y[test_idx]

model = HistGradientBoostingRegressor().fit(X_train, y_train)
y_pred = model.predict(X_test)
mean_absolute_percentage_error(y_test, y_pred)
```

```
0.44300751539296973
```

The generalization error measured via a shuffled trained test split is too optimistic. The generalization via a time-based split is likely to be more representative of the true performance of the regression model. Let’s assess this variability of our error evaluation with proper cross-validation:

```python
from sklearn.model_selection import cross_val_score

cv_mape_scores = -cross_val_score(
    model, X, y, cv=ts_cv, scoring="neg_mean_absolute_percentage_error"
)
cv_mape_scores
```

```
array([0.44300752, 0.27772182, 0.3697178 ])
```

The variability across splits is quite large! In a real life setting it would be advised to use more splits to better assess the variability. Let’s report the mean CV scores and their standard deviation from now on.

```python
print(f"CV MAPE: {cv_mape_scores.mean():.3f} ± {cv_mape_scores.std():.3f}")
```

```
CV MAPE: 0.363 ± 0.068
```

We can compute several combinations of evaluation metrics and loss functions, which are reported a bit below.

```python
from collections import defaultdict

from sklearn.metrics import (
    make_scorer,
    mean_absolute_error,
    mean_pinball_loss,
    root_mean_squared_error,
)
from sklearn.model_selection import cross_validate

def consolidate_scores(cv_results, scores, metric):
    if metric == "MAPE":
        scores[metric].append(f"{value.mean():.2f} ± {value.std():.2f}")
    else:
        scores[metric].append(f"{value.mean():.1f} ± {value.std():.1f}")

    return scores

scoring = {
    "MAPE": make_scorer(mean_absolute_percentage_error),
    "RMSE": make_scorer(root_mean_squared_error),
    "MAE": make_scorer(mean_absolute_error),
    "pinball_loss_05": make_scorer(mean_pinball_loss, alpha=0.05),
    "pinball_loss_50": make_scorer(mean_pinball_loss, alpha=0.50),
    "pinball_loss_95": make_scorer(mean_pinball_loss, alpha=0.95),
}
loss_functions = ["squared_error", "poisson", "absolute_error"]
scores = defaultdict(list)
for loss_func in loss_functions:
    model = HistGradientBoostingRegressor(loss=loss_func)
    cv_results = cross_validate(
        model,
        X,
        y,
        cv=ts_cv,
        scoring=scoring,
        n_jobs=2,
    )
    time = cv_results["fit_time"]
    scores["loss"].append(loss_func)
    scores["fit_time"].append(f"{time.mean():.2f} ± {time.std():.2f} s")

    for key, value in cv_results.items():
        if key.startswith("test_"):
            metric = key.split("test_")[1]
            scores = consolidate_scores(cv_results, scores, metric)
```

## Modeling predictive uncertainty via quantile regression

Instead of modeling the expected value of the distribution of $Y \left|\right. X$ like the least squares and Poisson losses do, one could try to estimate quantiles of the conditional distribution.

$Y \left|\right. X = x_{i}$ is expected to be a random variable for a given data point $x_{i}$ because we expect that the number of rentals cannot be 100% accurately predicted from the features. It can be influenced by other variables not properly captured by the existing lagged features. For instance whether or not it will rain in the next hour cannot be fully anticipated from the past hours bike rental data. This is what we call aleatoric uncertainty.

Quantile regression makes it possible to give a finer description of that distribution without making strong assumptions on its shape.

```python
quantile_list = [0.05, 0.5, 0.95]

for quantile in quantile_list:
    model = HistGradientBoostingRegressor(loss="quantile", quantile=quantile)
    cv_results = cross_validate(
        model,
        X,
        y,
        cv=ts_cv,
        scoring=scoring,
        n_jobs=2,
    )
    time = cv_results["fit_time"]
    scores["fit_time"].append(f"{time.mean():.2f} ± {time.std():.2f} s")

    scores["loss"].append(f"quantile {int(quantile * 100)}")
    for key, value in cv_results.items():
        if key.startswith("test_"):
            metric = key.split("test_")[1]
            scores = consolidate_scores(cv_results, scores, metric)

scores_df = pl.DataFrame(scores)
scores_df
```

shape: (6, 8)

| loss | fit\_time | MAPE | RMSE | MAE | pinball\_loss\_05 | pinball\_loss\_50 | pinball\_loss\_95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| str | str | str | str | str | str | str | str |
| "squared\_error" | "0.22 ± 0.01 s" | "0.36 ± 0.07" | "62.3 ± 3.5" | "39.1 ± 2.3" | "17.7 ± 1.3" | "19.5 ± 1.1" | "21.4 ± 2.4" |
| "poisson" | "0.24 ± 0.01 s" | "0.32 ± 0.07" | "64.2 ± 4.0" | "39.3 ± 2.8" | "16.7 ± 1.5" | "19.7 ± 1.4" | "22.6 ± 3.0" |
| "absolute\_error" | "0.32 ± 0.01 s" | "0.32 ± 0.06" | "64.6 ± 3.8" | "39.9 ± 3.2" | "17.1 ± 1.1" | "19.9 ± 1.6" | "22.7 ± 3.1" |
| "quantile 5" | "0.41 ± 0.01 s" | "0.41 ± 0.01" | "145.6 ± 20.9" | "92.5 ± 16.2" | "5.9 ± 0.9" | "46.2 ± 8.1" | "86.6 ± 15.3" |
| "quantile 50" | "0.44 ± 0.01 s" | "0.32 ± 0.06" | "64.6 ± 3.8" | "39.9 ± 3.2" | "17.1 ± 1.1" | "19.9 ± 1.6" | "22.7 ± 3.1" |
| "quantile 95" | "0.42 ± 0.01 s" | "1.07 ± 0.27" | "99.6 ± 8.7" | "72.0 ± 6.1" | "62.9 ± 7.4" | "36.0 ± 3.1" | "9.1 ± 1.3" |

  
  

Let us take a look at the losses that minimise each metric.

```python
def min_arg(col):
    col_split = pl.col(col).str.split(" ")
    return pl.arg_sort_by(
        col_split.list.get(0).cast(pl.Float64),
        col_split.list.get(2).cast(pl.Float64),
    ).first()

scores_df.select(
    pl.col("loss").get(min_arg(col_name)).alias(col_name)
    for col_name in scores_df.columns
    if col_name != "loss"
)
```

shape: (1, 7)

| fit\_time | MAPE | RMSE | MAE | pinball\_loss\_05 | pinball\_loss\_50 | pinball\_loss\_95 |
| --- | --- | --- | --- | --- | --- | --- |
| str | str | str | str | str | str | str |
| "squared\_error" | "absolute\_error" | "squared\_error" | "squared\_error" | "quantile 5" | "squared\_error" | "quantile 95" |

  
  

Even if the score distributions overlap due to the variance in the dataset, it is true that the average RMSE is lower when `loss="squared_error"`, whereas the average MAPE is lower when `loss="absolute_error"` as expected. That is also the case for the Mean Pinball Loss with the quantiles 5 and 95. The score corresponding to the 50 quantile loss is overlapping with the score obtained by minimizing other loss functions, which is also the case for the MAE.

## A qualitative look at the predictions

We can now visualize the performance of the model with regards to the 5th percentile, median and the 95th percentile:

```python
all_splits = list(ts_cv.split(X, y))
train_idx, test_idx = all_splits[0]

X_train, X_test = X[train_idx, :], X[test_idx, :]
y_train, y_test = y[train_idx], y[test_idx]

max_iter = 50
gbrt_mean_poisson = HistGradientBoostingRegressor(loss="poisson", max_iter=max_iter)
gbrt_mean_poisson.fit(X_train, y_train)
mean_predictions = gbrt_mean_poisson.predict(X_test)

gbrt_median = HistGradientBoostingRegressor(
    loss="quantile", quantile=0.5, max_iter=max_iter
)
gbrt_median.fit(X_train, y_train)
median_predictions = gbrt_median.predict(X_test)

gbrt_percentile_5 = HistGradientBoostingRegressor(
    loss="quantile", quantile=0.05, max_iter=max_iter
)
gbrt_percentile_5.fit(X_train, y_train)
percentile_5_predictions = gbrt_percentile_5.predict(X_test)

gbrt_percentile_95 = HistGradientBoostingRegressor(
    loss="quantile", quantile=0.95, max_iter=max_iter
)
gbrt_percentile_95.fit(X_train, y_train)
percentile_95_predictions = gbrt_percentile_95.predict(X_test)
```

We can now take a look at the predictions made by the regression models:

```python
last_hours = slice(-96, None)
fig, ax = plt.subplots(figsize=(15, 7))
plt.title("Predictions by regression models")
ax.plot(
    y_test[last_hours],
    "x-",
    alpha=0.2,
    label="Actual demand",
    color="black",
)
ax.plot(
    median_predictions[last_hours],
    "^-",
    label="GBRT median",
)
ax.plot(
    mean_predictions[last_hours],
    "x-",
    label="GBRT mean (Poisson)",
)
ax.fill_between(
    np.arange(96),
    percentile_5_predictions[last_hours],
    percentile_95_predictions[last_hours],
    alpha=0.3,
    label="GBRT 90% interval",
)
_ = ax.legend()
```

![[sphx_glr_plot_time_series_lagged_features_001.png|Predictions by regression models]]

Here it’s interesting to notice that the blue area between the 5% and 95% percentile estimators has a width that varies with the time of the day:

- At night, the blue band is much narrower: the pair of models is quite certain that there will be a small number of bike rentals. And furthermore these seem correct in the sense that the actual demand stays in that blue band.
- During the day, the blue band is much wider: the uncertainty grows, probably because of the variability of the weather that can have a very large impact, especially on week-ends.
- We can also see that during week-days, the commute pattern is still visible in the 5% and 95% estimations.
- Finally, it is expected that 10% of the time, the actual demand does not lie between the 5% and 95% percentile estimates. On this test span, the actual demand seems to be higher, especially during the rush hours. It might reveal that our 95% percentile estimator underestimates the demand peaks. This could be be quantitatively confirmed by computing empirical coverage numbers as done in the [calibration of confidence intervals](https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_quantile.html#calibration-section).

Looking at the performance of non-linear regression models vs the best models:

```python
from sklearn.metrics import PredictionErrorDisplay

fig, axes = plt.subplots(ncols=3, figsize=(15, 6), sharey=True)
fig.suptitle("Non-linear regression models")
predictions = [
    median_predictions,
    percentile_5_predictions,
    percentile_95_predictions,
]
labels = [
    "Median",
    "5th percentile",
    "95th percentile",
]
for ax, pred, label in zip(axes, predictions, labels):
    PredictionErrorDisplay.from_predictions(
        y_true=y_test,
        y_pred=pred,
        kind="residual_vs_predicted",
        scatter_kwargs={"alpha": 0.3},
        ax=ax,
    )
    ax.set(xlabel="Predicted demand", ylabel="True demand")
    ax.legend(["Best model", label])

plt.show()
```

![[sphx_glr_plot_time_series_lagged_features_002.png|Non-linear regression models]]

## Conclusion

Through this example we explored time series forecasting using lagged features. We compared a naive regression (using the standardized [`train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html#sklearn.model_selection.train_test_split "sklearn.model_selection.train_test_split")) with a proper time series evaluation strategy using [`TimeSeriesSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html#sklearn.model_selection.TimeSeriesSplit "sklearn.model_selection.TimeSeriesSplit"). We observed that the model trained using [`train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html#sklearn.model_selection.train_test_split "sklearn.model_selection.train_test_split"), having a default value of `shuffle` set to `True` produced an overly optimistic Mean Average Percentage Error (MAPE). The results produced from the time-based split better represent the performance of our time-series regression model. We also analyzed the predictive uncertainty of our model via Quantile Regression. Predictions based on the 5th and 95th percentile using `loss="quantile"` provide us with a quantitative estimate of the uncertainty of the forecasts made by our time series regression model. Uncertainty estimation can also be performed using [MAPIE](https://mapie.readthedocs.io/en/latest/index.html), that provides an implementation based on recent work on conformal prediction methods and estimates both aleatoric and epistemic uncertainty at the same time. Furthermore, functionalities provided by [sktime](https://www.sktime.net/en/latest/users.html) can be used to extend scikit-learn estimators by making use of recursive time series forecasting, that enables dynamic predictions of future values.

**Total running time of the script:** (0 minutes 7.490 seconds)

Related examples

![[sphx_glr_plot_grid_search_refit_callable_thumb.png]]

[Balance model complexity and cross-validated score](https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_refit_callable.html)

Balance model complexity and cross-validated score

![[sphx_glr_plot_gradient_boosting_quantile_thumb.png]]

[Prediction Intervals for Gradient Boosting Regression](https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_quantile.html)

Prediction Intervals for Gradient Boosting Regression

![[sphx_glr_plot_hgbt_regression_thumb.png]]

[Features in Histogram Gradient Boosting Trees](https://scikit-learn.org/stable/auto_examples/ensemble/plot_hgbt_regression.html)

Features in Histogram Gradient Boosting Trees

[Gallery generated by Sphinx-Gallery](https://sphinx-gallery.github.io/)