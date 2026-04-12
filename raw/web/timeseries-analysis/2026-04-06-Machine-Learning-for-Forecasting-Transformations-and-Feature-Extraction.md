---
source_type: web
title: "Machine Learning for Forecasting: Transformations and Feature Extraction"
author:
  - 
  - "[[Vitor Cerqueira]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
created: 2026-04-06
description: "Photo by Adam Śmigielski on Unsplash In this post, you’ll learn to apply supervised learning with time series using Python. This includes two things: transforming time series from a sequence into a tabular format; adding new features based on summary statistics. Introduction Forecasting is one of the most studied problems in data science. The goal […]"
tags:
  - 
  - "clippings"
source_url: "https://towardsdatascience.com/machine-learning-for-forecasting-transformations-and-feature-extraction-bbbea9de0ac2/"
published_at: 2022-11-15
related_concepts: []
---

![[0bbo01Xh_yBeQ0aSf-scaled.jpg|Photo by Adam Śmigielski on Unsplash]]

Photo by Adam Śmigielski on Unsplash

In this post, you’ll learn to apply supervised learning with time series using Python.

This includes two things:

- transforming time series from a sequence into a tabular format;
- adding new features based on summary statistics.

---

## Introduction

Forecasting is one of the most studied problems in data science. The goal is to predict future values of a time series.

Accurate forecasts are invaluable for decision makers. They reduce future uncertainty, thereby improving the planning of operations.

Traditional approaches to forecasting include methods such as ARIMA or exponential smoothing. But, [machine learning regression approaches are increasingly used to solve this problem](https://towardsdatascience.com/machine-learning-for-forecasting-size-matters-b5271ec784dc).

Machine learning approaches frame the task as supervised learning. The goal is to create a model based on historical data. Yet, it’s not clear how one can train a model using a sequence of values as the input.

Turns out, there’s a neat transformation which allows us to do that.

## Time Delay Embedding

A model is trained to derive patterns between observations and the consequences of those observations.

How do we do that with time series?

The value of a time series can be thought as the consequence of the past recent values before it. This value works as the target variable. The past recent values are used as explanatory variables.

Such process reshapes the series from a sequence of values into a tabular format. This transformation is called time delay embedding, and is the key of **auto-regression**.

Here’s a Python function to do it:

Here’s the data set when this function is applied to the sequence from 1 to 9:

![[1*X2J4Vl89zc8qfOwu4onQNw.png|Image by Author]]

Image by Author

Take the first row an example. The goal is to predict the number 4 (column Series(t+1)). The explanatory variables are the past 3 values before it: 3, 2, and 1.

Time delay embedding has a strong theoretical foundation. You can check reference \[1\] for details. Embedding theorems posits that time series are equivalent before and after transformation.

### Complete Example

Let’s code a complete example. We’ll use the sunspots time series. This data set is available in *pmdarima* library. Here’s how it looks:

![[1*KMbCfS4yHO_FPygRDtIpIQ.png|Sunspots time series. Image by author]]

Sunspots time series. Image by author

Below is an example of how to transform the time series, and train an auto-regressive model.

Check the comments for a bit more context in each step.

### Number of Lags and Forecasting Horizon

Transforming the time series requires specifying the number of lags. That is, how many recent past values we should use to predict the next point.

There are a few prescriptions for this. For example, checking partial auto-correlation and determine where it is significant. You can also optimize this parameter using cross-validation.

Another parameter is the forecasting horizon. This is the number of future steps you want to forecast. If this value is 1, the problem is referred to as one-step ahead forecasting. Or, [multi-step ahead forecasting](https://towardsdatascience.com/6-methods-for-multi-step-forecasting-823cbde4127a) otherwise.

It’s worth mentioning that the transformation does not replace other preprocessing steps.

You still need to account for trend and seasonal components, and remove them if needed.

## Feature Extraction

![[Image 9.jpg|Photo by Pratiksha Mohanty on Unsplash]]

Photo by Pratiksha Mohanty on Unsplash

There is a basic assumption behind auto-regression methods. Past lags contain enough information about how the series will evolve.

Yet, you can derive more information from these.

In machine learning, feature engineering is a crucial part of building accurate models. This can be done for forecasting problems as well.

We can summarise recent values using statistics. These statistics enrich the representation of time series. Hopefully, this translates into better forecasting performance.

For example, the average of the past few values can be useful. It gives a smoothed indicator of the level of the series at each point.

Here’s an example. I repeated the code above, but added a feature engineering step (lines 20–22).

In lines 21 and 22 I added the average of the lags as explanatory variables. This leads to a small gain in forecasting performance.

Here’s how feature importance looks like:

![[1*ybL6bOV1TwziXkJgXvWBiQ.png|Image by Author]]

Image by Author

The mean feature is the most important one.

I added a single feature in this example. But, you’re limited only by your imagination.

You can test several other summary statistics and check if they improve the model.

## Takeaways

- Use time delay embedding to transform a time series into a matrix
- Values in time series are modelled based on their past lags (auto-regression)
- Select the number of lags with partial auto-correlation analysis or cross-validation
- Extract more features from past lags using summary statistics

Thanks for reading, and see you in the next story!

### Previous stories you may want to read

> [**12 Things You Should Know About Time Series**](https://towardsdatascience.com/12-things-you-should-know-about-time-series-975a185f4eb2)

### References

\[1\] Takens, Floris. "Detecting strange attractors in turbulence." *Dynamical systems and turbulence, Warwick 1980*. Springer, Berlin, Heidelberg, 1981. 366–381.

\[2\] Bontempi, Gianluca, Souhaib Ben Taieb, and Yann-Aël Le Borgne. "Machine learning strategies for time series forecasting." *European business intelligence summer school*. Springer, Berlin, Heidelberg, 2012.